# Knowledge Base

This directory contains categorized, timestamped markdown files detailing findings, principles, and architectural decisions.

## Format
Every new entry must include YAML frontmatter:
```yaml
---
date: YYYY-MM-DD
topic: short_topic_name
status: active|deprecated
description: A short description of what this file contains.
---
```
Append new findings as separate sections or files rather than overwriting historical context, unless a principle is fundamentally proven wrong, in which case mark the old one `status: deprecated`.
