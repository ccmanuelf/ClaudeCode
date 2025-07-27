#!/usr/bin/env python3
"""
ClaudeCode Documentation Integration Script
==========================================

Automates the integration of existing project documentation into ClaudeCode
project structure. Analyzes, processes, and organizes various document formats
to create AI-friendly context and actionable specifications.

Usage:
    python integrate_documentation.py --project-root "/path/to/project" --docs-source "/path/to/docs"
    python integrate_documentation.py --analyze-only --docs-source "/path/to/docs"
    python integrate_documentation.py --interactive

Features:
    - Multi-format document processing (PDF, DOCX, MD, HTML)
    - Automatic categorization and organization
    - Requirements extraction and analysis
    - AI context generation
    - Gap analysis and recommendations
    - Integration with ClaudeCode workflows
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import mimetypes
import re

# Optional imports for document processing
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

try:
    from bs4 import BeautifulSoup
    HTML_SUPPORT = True
except ImportError:
    HTML_SUPPORT = False


class DocumentProcessor:
    """Processes various document formats and extracts content."""

    def __init__(self, supported_formats: List[str] = None):
        """Initialize processor with supported formats."""
        self.supported_formats = supported_formats or ['pdf', 'docx', 'md', 'html', 'txt']
        self.processed_count = 0
        self.error_count = 0

    def can_process(self, file_path: Path) -> bool:
        """Check if file can be processed based on extension."""
        return file_path.suffix.lower().lstrip('.') in self.supported_formats

    def process_document(self, file_path: Path) -> Dict[str, Any]:
        """Process a document and extract its content."""
        try:
            file_ext = file_path.suffix.lower()
            content = ""
            metadata = {
                'file': str(file_path),
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'format': file_ext.lstrip('.')
            }

            if file_ext == '.pdf':
                content = self._process_pdf(file_path)
            elif file_ext == '.docx':
                content = self._process_docx(file_path)
            elif file_ext in ['.md', '.markdown']:
                content = self._process_markdown(file_path)
            elif file_ext in ['.html', '.htm']:
                content = self._process_html(file_path)
            else:  # .txt and other text files
                content = self._process_text(file_path)

            self.processed_count += 1

            return {
                'metadata': metadata,
                'content': content,
                'word_count': len(content.split()),
                'char_count': len(content)
            }

        except Exception as e:
            self.error_count += 1
            return {
                'metadata': {'file': str(file_path)},
                'error': str(e),
                'content': ""
            }

    def _process_markdown(self, file_path: Path) -> str:
        """Process markdown files."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _process_text(self, file_path: Path) -> str:
        """Process plain text files."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def _process_pdf(self, file_path: Path) -> str:
        """Process PDF files using PyPDF2."""
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 not available for PDF processing")

        content = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return content

    def _process_docx(self, file_path: Path) -> str:
        """Process DOCX files using python-docx."""
        if not DOCX_SUPPORT:
            raise ImportError("python-docx not available for DOCX processing")

        doc = Document(file_path)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content

    def _process_html(self, file_path: Path) -> str:
        """Process HTML files using BeautifulSoup."""
        if not HTML_SUPPORT:
            raise ImportError("BeautifulSoup not available for HTML processing")

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            return soup.get_text()


class DocumentCategorizer:
    """Categorizes documents based on content and filename patterns."""

    def __init__(self):
        """Initialize categorizer with pattern definitions."""
        self.categories = {
            'requirements': {
                'patterns': [
                    r'requirement[s]?',
                    r'spec[s]?',
                    r'functional',
                    r'non-functional',
                    r'user.stor[yi]',
                    r'acceptance.criteria',
                    r'business.rule[s]?'
                ],
                'keywords': [
                    'shall', 'must', 'should', 'requirement', 'functional',
                    'non-functional', 'user story', 'acceptance criteria',
                    'business rule', 'constraint', 'assumption'
                ]
            },
            'specifications': {
                'patterns': [
                    r'design',
                    r'architecture',
                    r'technical.spec',
                    r'system.design',
                    r'detailed.design'
                ],
                'keywords': [
                    'architecture', 'design', 'technical specification',
                    'system design', 'component', 'interface', 'algorithm',
                    'data structure', 'class diagram', 'sequence diagram'
                ]
            },
            'guides': {
                'patterns': [
                    r'guide',
                    r'manual',
                    r'tutorial',
                    r'how.to',
                    r'walkthrough',
                    r'readme'
                ],
                'keywords': [
                    'guide', 'manual', 'tutorial', 'how to', 'walkthrough',
                    'getting started', 'quick start', 'installation',
                    'configuration', 'setup'
                ]
            },
            'api_docs': {
                'patterns': [
                    r'api',
                    r'endpoint[s]?',
                    r'rest',
                    r'swagger',
                    r'openapi'
                ],
                'keywords': [
                    'api', 'endpoint', 'rest', 'http', 'request', 'response',
                    'swagger', 'openapi', 'json', 'xml', 'parameter'
                ]
            },
            'architecture': {
                'patterns': [
                    r'architecture',
                    r'system.overview',
                    r'high.level',
                    r'component[s]?',
                    r'deployment'
                ],
                'keywords': [
                    'architecture', 'system overview', 'high level',
                    'component', 'deployment', 'infrastructure',
                    'scalability', 'performance', 'security'
                ]
            }
        }

    def categorize_document(self, document: Dict[str, Any]) -> str:
        """Categorize a document based on filename and content."""
        if 'error' in document:
            return 'other'

        file_path = document['metadata']['file']
        content = document['content'].lower()
        filename = Path(file_path).name.lower()

        scores = {}

        for category, patterns in self.categories.items():
            score = 0

            # Check filename patterns
            for pattern in patterns['patterns']:
                if re.search(pattern, filename, re.IGNORECASE):
                    score += 10

            # Check content keywords
            for keyword in patterns['keywords']:
                if keyword.lower() in content:
                    score += content.count(keyword.lower())

            scores[category] = score

        # Return category with highest score, or 'other' if no matches
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return 'other'


class RequirementsExtractor:
    """Extracts and structures requirements from documents."""

    def __init__(self):
        """Initialize requirements extractor."""
        self.requirement_patterns = [
            r'(?:shall|must|should|will)\s+(.{10,200})',
            r'(?:requirement|req)\s*\d*[:\-]\s*(.{10,200})',
            r'(?:user story|story)[:\-]\s*(.{10,200})',
            r'(?:acceptance criteria|ac)[:\-]\s*(.{10,200})',
            r'(?:business rule|rule)[:\-]\s*(.{10,200})'
        ]

        self.priority_indicators = {
            'high': ['critical', 'essential', 'must have', 'mandatory'],
            'medium': ['important', 'should have', 'recommended'],
            'low': ['nice to have', 'optional', 'could have']
        }

    def extract_requirements(self, documents: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract requirements from a list of documents."""
        requirements_by_category = {}

        for doc in documents:
            if 'error' in doc:
                continue

            category = doc.get('category', 'other')
            if category not in requirements_by_category:
                requirements_by_category[category] = []

            content = doc['content']
            extracted = self._extract_from_content(content, doc['metadata']['file'])
            requirements_by_category[category].extend(extracted)

        return requirements_by_category

    def _extract_from_content(self, content: str, source_file: str) -> List[Dict[str, Any]]:
        """Extract requirements from content text."""
        requirements = []

        for pattern in self.requirement_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)

            for match in matches:
                req_text = match.group(1).strip()

                # Clean up the requirement text
                req_text = re.sub(r'\s+', ' ', req_text)
                req_text = req_text.rstrip('.,;:')

                if len(req_text) < 10:  # Skip very short matches
                    continue

                priority = self._determine_priority(req_text)

                requirement = {
                    'id': hashlib.md5(req_text.encode()).hexdigest()[:8],
                    'text': req_text,
                    'source': source_file,
                    'priority': priority,
                    'category': self._categorize_requirement(req_text),
                    'extracted_at': datetime.now().isoformat()
                }

                requirements.append(requirement)

        return requirements

    def _determine_priority(self, text: str) -> str:
        """Determine priority based on text content."""
        text_lower = text.lower()

        for priority, indicators in self.priority_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return priority

        return 'medium'  # default priority

    def _categorize_requirement(self, text: str) -> str:
        """Categorize individual requirements."""
        text_lower = text.lower()

        if any(word in text_lower for word in ['performance', 'speed', 'latency', 'response time']):
            return 'performance'
        elif any(word in text_lower for word in ['security', 'authentication', 'authorization', 'encrypt']):
            return 'security'
        elif any(word in text_lower for word in ['interface', 'ui', 'user interface', 'display']):
            return 'interface'
        elif any(word in text_lower for word in ['data', 'database', 'storage', 'persist']):
            return 'data'
        else:
            return 'functional'


class DocumentationIntegrator:
    """Main class for integrating documentation into ClaudeCode project structure."""

    def __init__(self, project_root: Path, docs_output_dir: Path = None):
        """Initialize the documentation integrator."""
        self.project_root = Path(project_root)
        self.docs_dir = docs_output_dir or (self.project_root / 'docs')
        self.specs_dir = self.project_root / 'specs'

        self.processor = None
        self.categorizer = DocumentCategorizer()
        self.requirements_extractor = RequirementsExtractor()

        self.processed_documents = []
        self.extracted_requirements = {}

    def integrate_documentation(self, docs_source_dir: Path,
                              supported_formats: List[str] = None,
                              analyze_only: bool = False) -> Dict[str, Any]:
        """Main method to integrate documentation."""
        try:
            print("🔍 Discovering documents...")
            self.processor = DocumentProcessor(supported_formats)

            # Create directory structure
            if not analyze_only:
                self._create_directory_structure()

            # Discover and process documents
            self._discover_documents(docs_source_dir)

            # Categorize documents
            self._categorize_and_organize_documents(analyze_only)

            # Extract requirements
            print("📋 Extracting requirements...")
            self._extract_requirements()

            if not analyze_only:
                # Create specifications
                print("📝 Creating specifications...")
                self._create_specifications()

                # Generate AI context
                print("🤖 Generating AI context...")
                self._generate_ai_context()

                # Update project configuration
                print("⚙️ Updating project configuration...")
                self._update_project_configuration()

            # Generate report
            report = self._generate_integration_report()
            report['success'] = True

            return report

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processed_documents': len(self.processed_documents),
                'timestamp': datetime.now().isoformat()
            }

    def _create_directory_structure(self):
        """Create the necessary directory structure for documentation."""
        directories = [
            self.docs_dir,
            self.docs_dir / 'requirements',
            self.docs_dir / 'guides',
            self.docs_dir / 'api',
            self.docs_dir / 'architecture',
            self.docs_dir / 'specifications',
            self.docs_dir / 'original',
            self.specs_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        print(f"📁 Created directory structure in {self.docs_dir}")

    def _discover_documents(self, source_dir: Path):
        """Discover and process all documents in source directory."""
        supported_extensions = [f".{fmt}" for fmt in self.processor.supported_formats]

        for file_path in source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                print(f"  Processing: {file_path.name}")
                document = self.processor.process_document(file_path)
                self.processed_documents.append(document)

    def _categorize_and_organize_documents(self, analyze_only: bool):
        """Categorize documents and organize them in appropriate directories."""
        print("🏷️ Categorizing documents...")

        for doc in self.processed_documents:
            if 'error' not in doc:
                category = self.categorizer.categorize_document(doc)
                doc['category'] = category

                if not analyze_only:
                    # Create markdown version and organize
                    self._create_markdown_version(doc, category)

    def _create_markdown_version(self, document: Dict[str, Any], category: str):
        """Create a markdown version of the document in the appropriate category directory."""
        source_file = Path(document['metadata']['file'])

        # Determine target directory based on category
        category_dirs = {
            'requirements': self.docs_dir / 'requirements',
            'specifications': self.docs_dir / 'specifications',
            'guides': self.docs_dir / 'guides',
            'api_docs': self.docs_dir / 'api',
            'architecture': self.docs_dir / 'architecture',
            'other': self.docs_dir / 'original'
        }

        target_dir = category_dirs.get(category, self.docs_dir / 'original')
        target_file = target_dir / f"{source_file.stem}.md"

        # Create markdown content
        content = f"""# {source_file.name}

**Source:** {source_file}
**Category:** {category}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Word Count:** {document['word_count']}

---

{document['content']}
"""

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def _extract_requirements(self):
        """Extract requirements from all processed documents."""
        self.extracted_requirements = self.requirements_extractor.extract_requirements(
            self.processed_documents
        )

        # Save extracted requirements
        requirements_file = self.docs_dir / 'requirements' / 'extracted_requirements.json'
        with open(requirements_file, 'w') as f:
            json.dump(self.extracted_requirements, f, indent=2)

    def _create_specifications(self):
        """Create specification documents based on extracted requirements."""
        for category, requirements in self.extracted_requirements.items():
            if requirements:  # Only create specs for categories with requirements
                feature_name = self._extract_feature_name(category, requirements)
                spec_content = self._generate_specification_content(feature_name, requirements)

                spec_file = self.specs_dir / f"{feature_name}_spec.md"
                with open(spec_file, 'w') as f:
                    f.write(spec_content)

    def _extract_feature_name(self, category: str, requirements: List[Dict]) -> str:
        """Extract a meaningful feature name from category and requirements."""
        if category != 'other':
            return category.replace('_', '-')

        # Try to extract from first few requirements
        common_words = []
        for req in requirements[:3]:
            words = req['text'].lower().split()[:5]  # First 5 words
            common_words.extend([w for w in words if len(w) > 3 and w.isalpha()])

        if common_words:
            return f"{common_words[0]}-feature"
        else:
            return "general-feature"

    def _generate_specification_content(self, feature_name: str, requirements: List[Dict]) -> str:
        """Generate specification content from requirements."""
        high_priority = [r for r in requirements if r['priority'] == 'high']
        medium_priority = [r for r in requirements if r['priority'] == 'medium']
        low_priority = [r for r in requirements if r['priority'] == 'low']

        content = f"""# {feature_name.replace('-', ' ').title()} Specification

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Requirements:** {len(requirements)}

## Overview

This specification is automatically generated from extracted requirements related to {feature_name}.

## Requirements

### High Priority
"""

        for req in high_priority:
            content += f"""
**REQ-{req['id']}** ({req['category']})
{req['text']}
*Source: {Path(req['source']).name}*
"""

        content += "\n### Medium Priority\n"
        for req in medium_priority:
            content += f"""
**REQ-{req['id']}** ({req['category']})
{req['text']}
*Source: {Path(req['source']).name}*
"""

        content += "\n### Low Priority\n"
        for req in low_priority:
            content += f"""
**REQ-{req['id']}** ({req['category']})
{req['text']}
*Source: {Path(req['source']).name}*
"""

        content += f"""

## Implementation Notes

- Review and validate all extracted requirements
- Prioritize implementation based on business value
- Consider dependencies between requirements
- Establish acceptance criteria for each requirement

## Next Steps

1. Technical feasibility analysis
2. Effort estimation
3. Implementation planning
4. Stakeholder review and approval

---
*This specification was automatically generated from documentation analysis.*
"""

        return content

    def _generate_ai_context(self):
        """Generate AI-friendly context documentation."""
        context_content = f"""# ClaudeCode Project Context

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Overview

This project has integrated documentation from external sources containing {len(self.processed_documents)} documents across multiple categories.

## Documentation Structure

- **Requirements:** {self.docs_dir / 'requirements'}
- **Specifications:** {self.docs_dir / 'specifications'}
- **Guides:** {self.docs_dir / 'guides'}
- **API Documentation:** {self.docs_dir / 'api'}
- **Architecture:** {self.docs_dir / 'architecture'}

## Extracted Requirements Summary

"""

        total_requirements = sum(len(reqs) for reqs in self.extracted_requirements.values())
        context_content += f"**Total Requirements Extracted:** {total_requirements}\n\n"

        for category, requirements in self.extracted_requirements.items():
            if requirements:
                context_content += f"### {category.replace('_', ' ').title()}\n"
                context_content += f"- Count: {len(requirements)}\n"

                high_count = len([r for r in requirements if r['priority'] == 'high'])
                medium_count = len([r for r in requirements if r['priority'] == 'medium'])
                low_count = len([r for r in requirements if r['priority'] == 'low'])

                context_content += f"- High Priority: {high_count}\n"
                context_content += f"- Medium Priority: {medium_count}\n"
                context_content += f"- Low Priority: {low_count}\n\n"

        context_content += """
## AI Assistant Guidelines

When working with this project:

1. Reference extracted requirements in `docs/requirements/extracted_requirements.json`
2. Check existing specifications in `specs/` directory
3. Consider categorized documentation in `docs/` subdirectories
4. Prioritize high-priority requirements for implementation
5. Validate requirements against original sources when needed

## Key Files

- `docs/requirements/extracted_requirements.json` - All extracted requirements
- `specs/*_spec.md` - Generated feature specifications
- `docs/*/` - Categorized documentation by type

"""

        context_file = self.project_root / 'claude.md'
        with open(context_file, 'w') as f:
            f.write(context_content)

    def _update_project_configuration(self):
        """Update project configuration files with integration information."""
        # Update claude.md
        claude_md_path = self.project_root / 'claude.md'
        if claude_md_path.exists():
            self._update_claude_md(claude_md_path)

        # Update plan.md
        plan_md_path = self.project_root / 'plan.md'
        if plan_md_path.exists():
            self._update_plan_md(plan_md_path)

        # Update todo.md
        todo_md_path = self.project_root / 'todo.md'
        if todo_md_path.exists():
            self._update_todo_md(todo_md_path)

    def _update_claude_md(self, claude_md_path: Path):
        """Update claude.md with documentation integration information."""
        with open(claude_md_path, 'a') as f:
            f.write(f"""

## 📚 Documentation Integration

**Integration Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Integrated Documentation
- **Total Documents:** {len(self.processed_documents)}
- **Successfully Processed:** {len([d for d in self.processed_documents if 'error' not in d])}
- **Processing Errors:** {len([d for d in self.processed_documents if 'error' in d])}

### Requirements Extraction
- **Total Requirements:** {sum(len(reqs) for reqs in self.extracted_requirements.values())}
- **Categories:** {len(self.extracted_requirements)}

### Key Integration Outputs
- Categorized documentation in `docs/` directory
- Extracted requirements in `docs/requirements/extracted_requirements.json`
- Generated specifications in `specs/` directory

*Use this information to understand project scope and requirements when providing assistance.*

""")

    def _update_plan_md(self, plan_md_path: Path):
        """Update plan.md with documentation-derived planning information."""
        with open(plan_md_path, 'a') as f:
            f.write(f"""

## 📋 Documentation Integration Results

### Requirements Analysis
Based on integrated documentation, the following requirements have been identified:

""")

            for category, requirements in self.extracted_requirements.items():
                if requirements:
                    high_priority = [r for r in requirements if r['priority'] == 'high']
                    if high_priority:
                        f.write(f"""
#### {category.replace('_', ' ').title()} - High Priority
""")
                        for req in high_priority[:5]:  # Show top 5
                            f.write(f"- {req['text'][:100]}...\n")

            f.write(f"""

### Next Steps
1. Review extracted requirements for accuracy and completeness
2. Prioritize features based on business value and technical feasibility
3. Create detailed technical specifications for priority items
4. Update development timeline based on identified scope

*Full requirements available in `docs/requirements/extracted_requirements.json`*

""")

    def _update_todo_md(self, todo_md_path: Path):
        """Update todo.md with documentation integration tasks."""
        with open(todo_md_path, 'a') as f:
            f.write(f"""

## 📚 Documentation Integration Tasks

### Immediate Actions
- [ ] Review integrated documentation in docs/ directory
- [ ] Validate extracted requirements in docs/requirements/extracted_requirements.json
- [ ] Review generated specifications in specs/ directory
- [ ] Update project context based on new information

### Documentation Maintenance
- [ ] Establish documentation update process
- [ ] Create documentation review schedule
- [ ] Set up change management for requirements
- [ ] Define stakeholder approval workflow

### Development Planning
- [ ] Prioritize features based on integrated requirements
- [ ] Create technical specifications for priority features
- [ ] Update development timeline based on scope
- [ ] Identify risks and dependencies from documentation

*Integration completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

""")

    def _generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration report."""
        return {
            'integration_timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'summary': {
                'total_documents': len(self.processed_documents),
                'successful_processing': len([d for d in self.processed_documents if 'error' not in d]),
                'processing_errors': len([d for d in self.processed_documents if 'error' in d]),
                'categories_found': len(set(self.categorizer.categorize_document(d) for d in self.processed_documents if 'error' not in d)),
                'requirements_extracted': sum(len(reqs) for reqs in self.extracted_requirements.values()),
                'specifications_created': len(list(self.specs_dir.glob("*_spec.md"))) if self.specs_dir.exists() else 0
            },
            'document_categories': {
                cat: len([d for d in self.processed_documents if 'error' not in d and self.categorizer.categorize_document(d) == cat])
                for cat in ['requirements', 'specifications', 'guides', 'api_docs', 'architecture', 'other']
            },
            'processing_errors': [
                {
                    'file': d.get('metadata', {}).get('file', 'unknown'),
                    'error': d.get('error', 'unknown error')
                }
                for d in self.processed_documents if 'error' in d
            ],
            'extracted_requirements_by_category': self.extracted_requirements,
            'integration_paths': {
                'docs_directory': str(self.docs_dir),
                'specs_directory': str(self.specs_dir),
                'requirements_file': str(self.docs_dir / 'requirements' / 'extracted_requirements.json')
            }
        }


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="ClaudeCode Documentation Integration Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Integrate documentation from a source directory
  python integrate_documentation.py --project-root /path/to/project --docs-source /path/to/docs

  # Analyze documentation only (no integration)
  python integrate_documentation.py --analyze-only --docs-source /path/to/docs

  # Interactive mode
  python integrate_documentation.py --interactive

  # Specify custom output directory
  python integrate_documentation.py --project-root /path/to/project --docs-source /path/to/docs --output-dir /custom/output
        """
    )

    parser.add_argument(
        '--project-root',
        type=Path,
        help='Root directory of the ClaudeCode project (default: current directory)',
        default=Path.cwd()
    )

    parser.add_argument(
        '--docs-source',
        type=Path,
        help='Source directory containing documentation to integrate'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Custom output directory for integrated documentation (default: project-root/docs)'
    )

    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze documentation without integrating into project structure'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode with prompts for user input'
    )

    parser.add_argument(
        '--formats',
        nargs='+',
        choices=['pdf', 'docx', 'md', 'html', 'txt'],
        default=['pdf', 'docx', 'md', 'html', 'txt'],
        help='Document formats to process'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate integration report only (requires previous integration)'
    )

    return parser


def validate_dependencies():
    """Validate that required dependencies are available."""
    missing_deps = []

    if not PDF_SUPPORT:
        missing_deps.append("PyPDF2 (for PDF processing)")

    if not DOCX_SUPPORT:
        missing_deps.append("python-docx (for DOCX processing)")

    if not HTML_SUPPORT:
        missing_deps.append("beautifulsoup4 (for HTML processing)")

    if missing_deps:
        print("⚠️  Optional dependencies missing:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with: pip install PyPDF2 python-docx beautifulsoup4")
        print("Note: Script will continue but may skip some document formats.\n")


def interactive_mode() -> Dict[str, Any]:
    """Run interactive mode to gather user inputs."""
    print("🔄 Interactive Documentation Integration Setup")
    print("=" * 50)

    # Get project root
    default_root = Path.cwd()
    project_root_input = input(f"Project root directory [{default_root}]: ").strip()
    project_root = Path(project_root_input) if project_root_input else default_root

    # Get docs source
    while True:
        docs_source_input = input("Documentation source directory: ").strip()
        if docs_source_input and Path(docs_source_input).exists():
            docs_source = Path(docs_source_input)
            break
        print("❌ Please provide a valid existing directory path")

    # Get output directory
    default_output = project_root / 'docs'
    output_input = input(f"Output directory [{default_output}]: ").strip()
    output_dir = Path(output_input) if output_input else default_output

    # Get formats
    print("\nAvailable formats: pdf, docx, md, html, txt")
    formats_input = input("Formats to process [all]: ").strip()
    if formats_input:
        formats = [f.strip() for f in formats_input.split(',')]
    else:
        formats = ['pdf', 'docx', 'md', 'html', 'txt']

    # Analyze only option
    analyze_only = input("Analyze only (no integration)? [y/N]: ").strip().lower() == 'y'

    # Verbose output
    verbose = input("Enable verbose output? [y/N]: ").strip().lower() == 'y'

    return {
        'project_root': project_root,
        'docs_source': docs_source,
        'output_dir': output_dir,
        'formats': formats,
        'analyze_only': analyze_only,
        'verbose': verbose
    }


def main():
    """Main entry point for the documentation integration script."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    print("⚡️ ClaudeCode Documentation Integration")
    print("=" * 40)

    # Validate dependencies
    validate_dependencies()

    try:
        # Handle interactive mode
        if args.interactive:
            config = interactive_mode()
            args.project_root = config['project_root']
            args.docs_source = config['docs_source']
            args.output_dir = config.get('output_dir')
            args.formats = config['formats']
            args.analyze_only = config['analyze_only']
            args.verbose = config['verbose']

        # Validate required argument for non-interactive mode
        if not args.interactive and not args.docs_source:
            print("❌ --docs-source is required (or use --interactive mode)")
            sys.exit(1)

        # Validate inputs
        if not args.docs_source.exists():
            print(f"❌ Documentation source directory does not exist: {args.docs_source}")
            sys.exit(1)

        if not args.project_root.exists():
            print(f"❌ Project root directory does not exist: {args.project_root}")
            sys.exit(1)

        # Set up output directory
        output_dir = args.output_dir if args.output_dir else args.project_root / 'docs'

        print(f"📁 Project Root: {args.project_root}")
        print(f"📚 Documentation Source: {args.docs_source}")
        print(f"📤 Output Directory: {output_dir}")
        print(f"🔧 Processing Formats: {', '.join(args.formats)}")

        if args.analyze_only:
            print("🔍 Mode: Analysis Only")
        else:
            print("🔄 Mode: Full Integration")

        print("\n" + "=" * 40)

        # Initialize integrator
        integrator = DocumentationIntegrator(
            project_root=args.project_root,
            docs_output_dir=output_dir
        )

        if args.report_only:
            # Generate report only
            print("📊 Generating integration report...")
            report = integrator._generate_integration_report()

            report_path = output_dir / 'integration_report.json'
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            print(f"✅ Integration report saved to: {report_path}")

        else:
            # Run full integration
            print("🚀 Starting documentation integration...")

            result = integrator.integrate_documentation(
                docs_source_dir=args.docs_source,
                supported_formats=args.formats,
                analyze_only=args.analyze_only
            )

            if result['success']:
                print("\n✅ Documentation integration completed successfully!")
                print(f"📊 Processed {result['summary']['total_documents']} documents")
                print(f"📝 Extracted {result['summary']['requirements_extracted']} requirements")
                print(f"📋 Created {result['summary']['specifications_created']} specifications")

                if args.verbose:
                    print("\n📈 Detailed Results:")
                    print(json.dumps(result, indent=2))

                # Save integration report
                report_path = output_dir / 'integration_report.json'
                with open(report_path, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"📄 Full report saved to: {report_path}")

            else:
                print(f"\n❌ Integration failed: {result.get('error', 'Unknown error')}")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n⏸️  Integration interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
