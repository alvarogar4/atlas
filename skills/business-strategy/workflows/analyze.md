# Workflow: Analyze

**Purpose**: Apply strategic frameworks to understand a situation.

## Process

1. **Understand the question**:
   - What are you trying to understand or decide?
   - What's the scope? (company, product, market, initiative)
   - What's driving this need for analysis?

2. **Find existing knowledge**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files related to '{topic}' strategy in {BRAIN_PATH}/

Search in:
- resources/strategy/ - Past strategic analyses
- areas/ - Related decisions (general and area-scoped)
- projects/ - Active initiatives related to topic
- {PROJECT_PATH}/strategy/ - Project-level strategic analyses and decisions (if project active)

Search for:
- Files containing '{topic}', 'strategy', 'market', 'competitors'
- Files tagged with #strategy or #{topic}

Return:
- File paths grouped by type (analysis, decision, project)
- Dates and status
- Brief relevance summary"
```

3. **Select appropriate framework** from the Framework Selection Guide in `atlas:business-strategy`.

If the right framework isn't obvious from the question, ask the user:

```
Which angle would be most useful?
- {relevant framework}: {brief description}
```

**CHECKPOINT — STOP AND WAIT** for user to confirm framework choice.

4. **Spawn strategist with framework and file paths:**

```
subagent_type: atlas:strategist
prompt: "Strategic analysis for: {topic}

Files to read for additional context:
{file paths from atlas:locate_knowledge}

Framework to apply: {selected framework}

Provide analysis following the framework structure with:
- Current state assessment
- Key insights
- Strategic options
- Recommended direction
- Implementation considerations

If there are too many files or they are too large to read directly, spawn atlas:analyze_knowledge to synthesize them first, then work from that briefing."
```

5. **Save**:

Resolve scope using `SKILL.md` routing, then look up the correct path from `reference/folder-structure.md`.

```bash
mkdir -p {resolved_path}
```

Save using the Strategic Analysis template from `templates/analysis.md`.

6. **Output summary**:

```
Strategic analysis complete: {path}

Framework: {framework used}

Key Insights:
1. {insight 1}
2. {insight 2}
3. {insight 3}

Recommendation: {brief recommendation}

Next: Review full analysis or document a decision about this topic.
```
