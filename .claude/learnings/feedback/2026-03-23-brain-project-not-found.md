---
date: "2026-03-23 10:12:40"
sha: "72f8151"
category: "missing-context"
status: pending
observed-workflows:
  subagents: ["atlas:content_reviewer"]
  skills: ["atlas:second_brain", "atlas:humanizer", "atlas:marketing_content"]
  commands: []
---

# Agent fails to locate project data within the brain

## Observation

User asked to "pull obsession brain." Agent searched the filesystem broadly (find, ls across /Users/alvaro/Workspace) and found /Users/alvaro/Workspace/obsessionDB-brain/ (an unrelated local folder) instead of recognizing that the ObsessionDB project lives inside the atlas brain at /Users/alvaro/Workspace/claude-setup/atlas-brain/projects/obsessiondb/. The agent treated "obsession brain" as a separate repository rather than a project within the active brain.

## Context

Working on personal brand content (speed vs velocity LinkedIn/Twitter drafts). The atlas:second_brain skill was loaded and the brain path was known. User asked to pull all brains, agent pulled atlas-brain successfully, then failed to locate the obsessiondb project when asked about it separately.

## Analysis

The agent had the brain path configured (ATLAS_BRAIN_PATH) and the second_brain skill loaded, which defines the PARA folder structure with projects/ as a top-level directory. Despite this, when the user said "obsession brain," the agent searched the filesystem instead of checking {BRAIN_PATH}/projects/ first. The root cause is missing context: the agent doesn't know that "obsession brain" refers to a project within the atlas brain, not a separate git repository. The second_brain skill's project entity management should have been the first lookup path.
