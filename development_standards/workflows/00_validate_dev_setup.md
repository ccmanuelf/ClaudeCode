---
id: validate_dev_setup
category: workflow
priority: 10
version: 1.0
description: >
  Pre-execution task to verify that the local development environment
  meets the project's language, tooling, and dependency requirements.
---

## Purpose

Verify that the developer’s local environment is correctly configured before beginning any feature work. Ensuring the right runtimes, package managers, and dependencies are in place prevents downstream errors and wasted cycles.

## Clarifying Questions

- Which programming language(s) and version(s) should be validated?  
- What package manager(s) are required (for example, npm, pip, Maven)?  
- Are there system-level dependencies we must check (for example, Docker, PostgreSQL, Redis)?  
- Do you follow any specific style guides or linting configurations (for example, ESLint, Pylint, Prettier)?

## Validation Steps

1. Check language runtime version  
   - Example: `node --version` or `python --version`  
   - Confirm the output matches the expected major/minor version.  

2. Verify package manager installation  
   - Example: `npm --version`, `pip --version`, or `mvn --version`  
   - Ensure the command runs without error and meets the required version.  

3. Confirm project dependencies are installed  
   - Node.js: run `npm ci` and expect exit code 0  
   - Java/Maven: run `mvn dependency:resolve` and expect a successful build  
   - AI CLI Tools: verify your AI tool is accessible (e.g., `claude --version`, `gemini --help`)

4. Run baseline tests or lint checks  
   - Node.js: `npm test -- --watchAll=false`  
   - Python: `pytest --maxfail=1 --disable-warnings -q`  
   - Java/Maven: `mvn test -q`  

## Outcome

- On success: proceed to `workflows/01_generate_prd.md` for PRD generation.  
- On failure: capture error messages, notify the user of required fixes, and halt further steps until resolved.  
