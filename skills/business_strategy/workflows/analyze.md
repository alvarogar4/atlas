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
- areas/decisions/ - Related decisions
- projects/ - Active initiatives related to topic

Search for:
- Files containing '{topic}', 'strategy', 'market', 'competitors'
- Files tagged with #strategy or #{topic}

Return:
- File paths grouped by type (analysis, decision, project)
- Dates and status
- Brief relevance summary"
```

3. **Select appropriate framework** from the Framework Selection Guide in `atlas:business_strategy`.

4. **Spawn strategist with file paths:**

```
subagent_type: atlas:strategist
prompt: "Strategic analysis for: {topic}

Files to read for context:
{file paths from atlas:locate_knowledge}

Framework to apply: {selected framework}

Read the files above, then provide analysis following the framework structure with:
- Current state assessment
- Key insights
- Strategic options
- Recommended direction
- Implementation considerations

If there are too many files or they are too large to read directly, spawn atlas:analyze_knowledge to synthesize them first, then work from that briefing."
```

5. **Save analysis**:

```bash
mkdir -p {BRAIN_PATH}/resources/strategy/{topic}/
```

Save to: `{BRAIN_PATH}/resources/strategy/{topic}/analysis.md`

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
