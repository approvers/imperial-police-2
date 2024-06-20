import select
import subprocess
import sys
from typing import List

from dotenv import load_dotenv

# List of dotenv files to load, in order of priority
# (last one has the highest priority)
DOTENV_FILES: List[str] = [
    "./.example.env",
    "./.local.env",
]


def load_env_vars() -> None:
    for dotenv_file in DOTENV_FILES:
        try:
            print(f"Loading env vars from: {dotenv_file}")
            load_dotenv(dotenv_file)
        except FileNotFoundError:
            print(f"File not found: {dotenv_file}")
            continue


def run_command(cmd: str) -> int:
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if process.stdout is None or process.stderr is None:
        raise ValueError("Failed to capture stdout or stderr")

    stdout, stderr = process.stdout, process.stderr

    while True:
        reads = [stdout.fileno(), stderr.fileno()]
        readable, _, _ = select.select(reads, [], [])

        for r in readable:
            if r == stdout.fileno():
                output = stdout.readline()
                if output:
                    print(output.decode("utf-8").strip())
            if r == stderr.fileno():
                error = stderr.readline()
                if error:
                    print(error.decode("utf-8").strip(), file=sys.stderr)

        if process.poll() is not None:
            break

    # Ensure all remaining output is printed
    while True:
        output = stdout.readline()
        if output:
            print(output.decode("utf-8").strip())
        else:
            break

    while True:
        error = stderr.readline()
        if error:
            print(error.decode("utf-8").strip(), file=sys.stderr)
        else:
            break

    return process.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <command>")
        sys.exit(1)

    load_env_vars()
    command = " ".join(sys.argv[1:])

    exit_code = run_command(command)
    print(f"Command exited with code: {exit_code}")
    sys.exit(exit_code)
