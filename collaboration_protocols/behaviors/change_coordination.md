---
id: change_coordination
category: behavior
priority: 60
version: 1.0
description: >
  Defines Spark’s protocol for coordinating changes across modules, files, and systems.
  Focuses on multi-file awareness, dependency scanning, update sequencing,
  and completeness verification.
---

## Multi-File Awareness Rules

- Always scan the full module/component/project directory before making changes  
- Check for inter-file references: variables, outputs, resources may be reused elsewhere  
- Use file search (`grep`, ripgrep, etc.) before modifying anything critical  
- When modifying a resource:
  - List where it's used  
  - Validate reference integrity  
- Respect module boundaries and encapsulation contracts

## Change Planning Workflow

1. Identify scope  
   - All impacted files  
   - Direct and indirect dependencies  
2. Search references  
   - `grep` for resource names, variable names, module outputs  
   - Scan config manifests and workflow YAMLs  
3. Update systematically  
   - Follow dependency order  
   - Avoid forward references or assumptions  
4. Verify completeness  
   - Rerun search post-change  
   - Confirm nothing was missed

## Common Coordination Errors

- Missing `depends_on` declarations  
- Updating config without downstream changes  
- Forgetting to patch documentation and examples  
- Assuming implicit variable propagation  
- Breaking modular contracts (e.g., renamed inputs/outputs)

## Golden Rule

> 📚 Read before writing. Search before changing.

## Coordination Etiquette

- Annotate coordinated changes with anchor comments:  
  ```hcl
  # AIDEV-NOTE: Updated this output as part of multi-file refactor
  ```  
- Flag edge cases, manual overrides, and migration risks explicitly  
- Confirm expected behavior post-update using real or mock data

## Safeguards

- When modifying file A, scan files B-Z for its name or content usage  
- Track change log entries as tasks where applicable  
- If unsure:
  > “🧠 This change may affect other modules—should I scan and list related files before committing?”

## Planning Tip

> Small changes ripple wide. Scan, annotate, test, and ask before assuming coordination is complete.
