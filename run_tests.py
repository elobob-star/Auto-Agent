#!/usr/bin/env python3
import argparse
import subprocess
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Run benchmark tests with verbosity controls for context conservation.")
    parser.add_argument("--mode", choices=["summary", "verbose", "failed-only"], default="summary",
                        help="Amount of information to print. Defaults to summary.")
    parser.add_argument("--tasks", type=str, help="Specific tasks to run, comma separated. (e.g., 'task1,task2')")
    parser.add_argument("--concurrency", type=int, default=4, help="Number of concurrent tasks to run.")
    return parser.parse_args()

def main():
    args = parse_args()

    print(f"Running tests in {args.mode} mode...")

    cmd = ["uv", "run", "harbor", "run", "-p", "tasks/", "--agent-import-path", "harness:AutoAgent", "-o", "jobs", "--job-name", "latest", "-n", str(args.concurrency)]

    if args.tasks:
        for t in args.tasks.split(","):
            cmd.extend(["--task-name", t.strip()])

    # For now, this is a mock wrapper that just calls the real underlying tool and prints the output.
    # In a full implementation, this script would read Harbor's JSON outputs and format them
    # intelligently based on the chosen mode to save tokens.

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Parse the output
        if args.mode == "summary":
            # Just show the final lines or summary statistics
            lines = result.stdout.splitlines()
            print("\n".join(lines[-20:]))
            if result.stderr:
                print("Errors occurred:")
                print("\n".join(result.stderr.splitlines()[-10:]))
        elif args.mode == "verbose":
            print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
        else:
            # failed-only logic
            print("Output parsing for failed-only mode will be implemented. Showing summary for now.")
            print(result.stdout[-1000:])

    except Exception as e:
        print(f"Error running tests: {e}")

if __name__ == "__main__":
    main()
