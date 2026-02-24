# Workflow: Decision

**Purpose**: Document a major business decision with context and rationale.

## Process

1. **Understand the decision**:
   - What decision needs to be made?
   - What options are being considered?
   - What's the deadline?
   - Who needs to be involved?

2. **Load project context**:

If an active project is set:

- Read `{PROJECT_PATH}/context.md` -- understand what the project is
- Read `{PROJECT_PATH}/strategy/strategy.md` -- understand current strategy
- Read all files in `{PROJECT_PATH}/competitors/` -- understand competitive landscape

3. **Check for relevant analysis**:

Look for existing `*-analysis.md` files in the paths defined by `reference/folder-structure.md`:

- If project-scoped: check project strategy path first, then brain-level resources if something relevant exists
- If area-scoped or general: check brain-level resources

If no analysis exists, offer to create one first.

4. **Document the decision**:

Use the appropriate template from `templates/decision.md`:

- For significant decisions: use the Full Decision Log template
- For smaller decisions: use the Quick Decision template

Consider using supplementary tools from the same file:

- Pre-Mortem Analysis (for high-risk decisions)
- Second-Order Thinking (for decisions with cascading effects)
- Reversibility Assessment (when unsure about commitment level)

5. **Save**:

Resolve scope using `SKILL.md` routing, then look up the correct path from `reference/folder-structure.md`.

```bash
mkdir -p {resolved_directory}
```

6. **Output summary**:

```
Decision documented: {path}

Decision: {chosen option}
Key trade-off: {main trade-off}

Implementation steps identified: {count}
Review date set: {date}
```
