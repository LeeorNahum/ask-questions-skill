"""Run eval sessions, at most N at once.

Usage: python batch.py <jobs-file> [max-concurrent]
Each line of the jobs file holds the arguments of run.py:
  <label> <eval name> <model> <skill-dir or -> [timeout-seconds]
grade.py reads each label as <round>-<eval name>-<old|new|none>-<opus|sol>.
"""
import concurrent.futures, pathlib, subprocess, sys

here = pathlib.Path(__file__).parent
jobs = [l.split() for l in pathlib.Path(sys.argv[1]).read_text().splitlines() if l.strip() and not l.startswith('#')]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 4


def go(job):
    r = subprocess.run([sys.executable, '-B', str(here / 'run.py'), *job], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip()[-300:], flush=True)


with concurrent.futures.ThreadPoolExecutor(n) as pool:
    list(pool.map(go, jobs))
