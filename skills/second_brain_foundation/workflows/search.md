# Workflow: Search & Recall

## Search

**Purpose**: Quick file discovery by keyword.

### Setup

Execute **Basic Setup** from SKILL.md.

### Process

1. Spawn locate_knowledge for fast file discovery:

```
subagent_type: atlas:core:locate_knowledge
prompt: "Query: {query}

Find all files related to this query in {BRAIN_PATH}/. Search filenames, content, and tags."
```

2. Return locator results directly to user.

If no results: "No notes found for '{query}'. Want me to capture something about this topic?"

---

## Recall

**Purpose**: Deep retrieval with parallel agents for thorough analysis.

### Setup

Execute **Basic Setup** from SKILL.md.

### Process

#### Step 1: Locate relevant files

```
subagent_type: atlas:core:locate_knowledge
prompt: "Query: {topic}

Search the entire brain at {BRAIN_PATH}/ for files related to this topic.

Search strategy:
1. Content search: Files containing '{topic}' keywords
2. Filename search: Files named with topic words
3. Tag search: Files tagged with related terms
4. Related search: Files that reference this topic

Return file paths grouped by:
- Direct matches (highest relevance)
- Tag matches
- Related references
- By PARA category (projects, areas, resources, archives, inbox)

Include modification dates and match counts per category."
```

Wait for locator to complete.

#### Step 2: Analyze found files

```
subagent_type: atlas:core:analyze_knowledge
prompt: "Topic: {topic}

Files to analyze:
{file paths from Step 1}

For each file:
1. Read the full content
2. Extract key insights related to '{topic}'
3. Note explicit links (related: fields) to other files
4. Identify temporal patterns

Return:
- Summary of each file's relevance
- Key insights with source file references
- Connections found between files
- Timeline of how thinking evolved
- Patterns observed"
```

#### Step 3: Synthesize and Present

1. Read the most relevant files (top 3-5) into main context for verification
2. Synthesize findings from the analyzer
3. Present results:
   - Sources analyzed (with file paths)
   - Key insights (with source references)
   - Connections found
   - Patterns observed
   - Knowledge gaps identified
