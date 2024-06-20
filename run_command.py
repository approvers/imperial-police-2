import subprocess
import sys

from dotenv import load_dotenv

# List of dotenv files to load, in order of priority (last one has the highest priority)
DOTENV_FILES = [
    "./.example.env",
    "./.local.env",
]


def load_env_vars():
    for dotenv_file in DOTENV_FILES:
        try:
            print(f"Loading env vars from: {dotenv_file}")
            load_dotenv(dotenv_file)
        except FileNotFoundError:
            print(f"File not found: {dotenv_file}")
            continue


def run_command(cmd: str):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        error = process.stderr.readline()

        if output:
            print(output.decode("utf-8").strip())
        if error:
            print(error.decode("utf-8").strip(), file=sys.stderr)

        if not output and not error and process.poll() is not None:
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
