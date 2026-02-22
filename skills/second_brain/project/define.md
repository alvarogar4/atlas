# Project Definition Wizards

Interactive workflows for defining project assets. All follow the same pattern:

1. Check if file exists → offer to overwrite
2. Ask questions via AskUserQuestion
3. Fill template from `reference/project-templates.md`
4. Save to the appropriate path

---

## Action: project-context

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Check if `{PROJECT_PATH}/context.md` exists → ask to overwrite

### Questions (ask one at a time)

1. "What is this project/business?" (one sentence)
2. "What problem does it solve?"
3. "Who is the target audience?" (brief)
4. "What makes it unique?" (key differentiator)
5. "What's the primary goal?" (revenue, growth, awareness)
6. "What's the current stage?" (idea, MVP, growth, mature)
7. "Any constraints?" (technical, budget, timeline)

### Execution

- Generate context.md using Context Template
- Generate a 2-3 sentence elevator pitch for the Summary
- Write to `{PROJECT_PATH}/context.md`
- Update README.md Overview section with the summary

### Output

```
Project context defined: {PROJECT_PATH}/context.md

Summary:
- Business: [one sentence]
- Audience: [brief]
- Differentiator: [key point]
- Stage: [current]

Next: Want to define the project strategy?
```

---

## Action: project-strategy

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Create `{PROJECT_PATH}/strategy/` directory
- Check if strategy.md exists → ask what to update or overwrite

### Questions

1. "Vision (where do you want to be in 2-3 years)?"
2. "Mission (how do you create value)?"
3. "Primary goal (the #1 thing you're trying to achieve)?"
4. "Supporting goals (2-3 additional objectives)?"
5. "Primary target segment?"
6. "Key differentiation?"
7. "This quarter's focus initiatives?"
8. "Success metrics?"

### Execution

- Generate strategy.md using Strategy Template
- Write to `{PROJECT_PATH}/strategy/strategy.md`

### Output

```
Strategy defined: {PROJECT_PATH}/strategy/strategy.md

Vision: {summary}
Primary Goal: {goal}

Next: Want to document competitors or define brand voice?
```

---

## Action: project-brand

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Read context.md to inform questions (suggest creating it first if missing)
- Check if brand-voice.md exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/` directory

### Questions

1. "What 3-5 adjectives describe your brand personality?"
2. "What tone should content have?" (formal, casual, technical, friendly)
3. "Any words/phrases to always use?"
4. "Any words/phrases to never use?"
5. "Example brand you admire?" (style reference)

### Execution

- Generate brand-voice.md using Brand Voice Template
- Derive key messages from context + personality
- Write to `{PROJECT_PATH}/marketing/brand-voice.md`

### Output

```
Brand voice defined: {PROJECT_PATH}/marketing/brand-voice.md

Personality: [adjectives]
Tone: [description]

Next: Want to define the visual identity?
```

---

## Action: project-visuals

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Check if visual-identity.md exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/` directory

### Questions

1. "What is your primary brand color?" (hex or name)
2. "What is your secondary brand color?"
3. "What visual style?" (modern, classic, playful, minimal, bold)
4. "What mood/feeling?" (energetic, calm, professional, creative)
5. "Any design references or inspirations?"

### Execution

- Derive extended color palette from primary color (use `atlas:marketing_visuals` patterns)
- Generate visual-identity.md using Visual Identity Template
- Write to `{PROJECT_PATH}/marketing/visual-identity.md`

### Output

```
Visual identity defined: {PROJECT_PATH}/marketing/visual-identity.md

Primary: {hex}
Secondary: {hex}
Style: {aesthetic} | Mood: {mood}
```

---

## Action: project-audience

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Read context.md to inform persona creation
- If name not provided, ask for it
- Slugify the name
- Check if persona file exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/audiences/` directory

### Questions

1. "Give this persona a name" (e.g., "Technical Tim")
2. "Demographics?" (age, role, industry)
3. "What are their goals?"
4. "What are their pain points?"
5. "How do they make decisions?"
6. "Where do they hang out online?"

### Execution

- Generate persona file using Audience Persona Template
- Write to `{PROJECT_PATH}/marketing/audiences/{slug}.md`

### Output

```
Audience persona created: {PROJECT_PATH}/marketing/audiences/{slug}.md

Name: [name]
Role: [summary]
Key pain point: [primary]
```

---

## Action: project-competitors

### Setup

Execute **Project** config from SKILL.md.

### Pre-checks

- Read context.md for comparison context
- If name not provided, ask for it
- Slugify the name
- Check if competitor file exists → ask to overwrite
- Create `{PROJECT_PATH}/competitors/` directory

### Questions

1. "What is the competitor's name?"
2. "What is their website?"
3. "What are their key strengths?"
4. "What are their weaknesses?"
5. "How do they position themselves?"
6. "What's their pricing model?"
7. "How do we differentiate from them?"

### Execution

- Optionally fetch website for additional context
- Generate competitor file using Competitor Profile Template
- Write to `{PROJECT_PATH}/competitors/{slug}.md`

### Output

```
Competitor documented: {PROJECT_PATH}/competitors/{slug}.md

Competitor: [name]
Strengths: [key points]
Our differentiation: [how we're different]
```
