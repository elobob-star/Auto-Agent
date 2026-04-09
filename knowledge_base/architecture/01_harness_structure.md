---
date: 2024-04-09
topic: harness_structure
status: active
description: Details about the split between the Harbor adapter and the core agent logic.
---

## Harbor Adapter vs. Core Agent
The harness is split into `harness/adapter.py` and `harness/core/`.
`adapter.py` handles the boundary with the Harbor evaluation framework and should not be modified unless the evaluation format changes.
`core/` contains the actual agent logic, tools, and prompts. This is the primary area for iteration and experimentation.
