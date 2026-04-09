# AutoAgent Meta-Session Loop Instructions

Welcome to the AutoAgent engineering session. Your job is to iteratively improve the agent harness located in `harness/`.

## Modes of Operation
Depending on what you are asked to do at the start of the session, assume one of these modes:

### 1. Experiment Mode (Default)
Your goal is to run a loop (10-50 iterations) to improve the benchmark score.
**The Loop:**
1. Run the benchmark: `./run_tests.py --mode summary`
2. Analyze the summary. If you need more details on a failure, run `./run_tests.py --mode verbose --tasks <failed_task>`
3. Formulate a hypothesis to fix failures or improve architecture.
4. Edit the codebase in `harness/core/`. Do NOT modify `harness/adapter.py`.
5. Update `results.tsv` with the outcome.
6. If the run succeeds or yields a useful lesson, log it in the appropriate `knowledge_base/` folder.
7. Repeat. Do NOT stop after one iteration. Keep iterating until you hit your loop limit or are explicitly stopped by the user.

### 2. Maintenance Mode
Your goal is to ensure the repository context is clean and accurate.
1. Traverse the directories.
2. Ensure every folder has an updated `INDEX.md` describing its contents.
3. Clean up formatting in the `knowledge_base/`.

## Universal Principles
- **Context Conservation**: Never read massive log outputs unless necessary. Use summary flags.
- **Plan Hard**: Always articulate your hypothesis before changing code.
- **Verify Output**: Never assume your fix worked. Check the logs.
- **No Overfitting**: Ensure your changes improve general agent capabilities, not just hardcoded solutions to specific tests.

Read `program.md` to understand the North Star goal.
