---
date: 2024-04-09
topic: vision_and_goals
status: active
description: The long-term vision for the autoagent project and Jules session utilization.
---

# Vision and Goals

## The Goal
To adapt the Auto-Agent framework to push for maximum autonomy, maximizing iterations and recursive development per session.

## Core Directives
1. **Separation of Concerns**: The harness being tested (`harness/`) is separated from the meta-agent logic. The meta-agent logic is executed by a Jules session following instructions from `AGENTS.md`.
2. **Context Conservation**: Context rot is the enemy of long iterations. We use intelligent map tools, `run_tests.py --summary`, and structured logging to minimize the tokens consumed during an iteration loop.
3. **Continuous Knowledge Building**: The `knowledge_base/` serves as a persistent memory across sessions. Sessions must document their findings using a markdown + YAML frontmatter format.
4. **Principled Prompts**: System prompts should be built on universally true principles (e.g., "Work hard", "Plan hard", "Verify output") that apply regardless of context.
