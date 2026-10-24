# Competitor Template

Template for competitor profile definitions.

## Slugification

```bash
SLUG=$(echo "{name}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
```

## Competitor Profile Template

**Path**: `{PROJECT_PATH}/competitors/{competitor-slug}.md`

```yaml
---
project: {project_name}
captured: {ISO timestamp}
type: competitor
competitor: {competitor-name}
domains: [{competitor.com}, {other domains they own or host customers on}]
status: active
---

# Competitor: {Competitor Name}

## Overview
- **Website**: {URL}
- **Core Offering**: {Product/service}
- **Target Market**: {Who they serve}

## Positioning
{How they position themselves}

## Strengths
1. {Strength 1}
2. {Strength 2}
3. {Strength 3}

## Weaknesses
1. {Weakness 1}
2. {Weakness 2}
3. {Weakness 3}

## Our Differentiation
{How we differentiate from them}

> [!tip] Opportunities
> {Gaps in their offering we can exploit, or weaknesses we can position against.}

## Notes
{Additional observations}
```
