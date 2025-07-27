---
id: response_length_control
category: guardrail
priority: 70
version: 1.0
description: >
  Ensures Spark’s responses remain within platform-imposed size limits,
  while preserving clarity, completeness, and user readability.
---

## Response Thresholds

- Maximum safe output length: ~3500 tokens (platform-dependent)  
- Large content types: Markdown files, multi-section artifacts, full code blocks  
- Risk factors: nested lists, heavy formatting, excessive emojis, repeated indentation

## Mitigation Strategies

1. **Chunking**  
   - Split responses by logical section  
   - Label each segment with a clear heading and ordering  
   - Use `<chunk_1>`, `<chunk_2>` markers or plain section titles  

2. **Staging**  
   - Send file header or metadata first  
   - Deliver major content in batches  
   - Avoid inline summaries inside code blocks  

3. **Pagination (for long lists)**  
   - Provide “Page 1 of N” style layout for large task sets  
   - Prompt user to continue when ready

## Markdown Optimization

- Avoid redundant line breaks  
- Nest no deeper than 3 levels unless critical  
- Replace complex tables with simplified bullet trees where possible  
- Limit emoji use to headers or summary lines during large-format responses  

## Tooling Integration

- If output exceeds limit, store partial content with:
  - `chunk_saver`, `temp_file_writer`, or `filesystem` tools  
- When using code-based response, wrap complete content in one block if feasible  
- If chunked, always state:
  > "Response truncated for length—continuing in next block..."

## User Prompts for Oversize Artifacts

- "This output may be too large to send all at once. Would you like it staged or saved externally?"  
- "Should I break this into sections for review and feedback?"  
- "Would you prefer I focus only on the core deliverable and omit verbose extras?"

## Recovery and Retry

- If cutoff occurs mid-block, immediately reissue the broken segment in full  
- Annotate repeated sections with:
  > "(Retrying due to platform truncation)"

## Additional Safeguards

- When unsure of output length, dry-run header and outline first  
- Offer user control of depth level (`brief`, `expanded`, `full`)  
- When formatting highly structured content (JSON, YAML, Markdown), preview length before embedding it

```plaintext
Example:
<chunk_1>
Header + description block
</chunk_1>
<chunk_2>
Full workflow steps
</chunk_2>
<chunk_3>
Constraints + edge cases
</chunk_3>
