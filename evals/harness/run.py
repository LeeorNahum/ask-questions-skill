"""Run one clean-room, possibly multi-turn session of an ask-questions eval.

Usage: python run.py <label> <eval name> <model> <skill-dir or -> [timeout-seconds-per-turn]
  model:  opus | sol
Environment: EVAL_ROOT, a run folder outside the home folder and every Git repository.

Builds EVAL_ROOT/builds/<label>/work from ../fixtures/base plus the eval's fixture overlay, as a
fresh Git repository. Sends the eval's first turn as a new session, then resumes that same session
for each later turn, so the conversation history carries over. Each turn's record is kept apart as
turn-<n>.jsonl (and turn-<n>-last.txt for Codex), and result.json records the session id, each
turn's exit, and the commit before each turn, so an assertion can grade one turn.

Runs are headless: nobody answers a question. The environment passed to the CLI is an allowlist,
so nothing the maintainer has exported reaches the session.
"""
import atexit, json, os, pathlib, re, shutil, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
EVALS = HERE.parent / 'evals.json'
FIXTURES = HERE.parent / 'fixtures'
HOME = pathlib.Path.home()
ROOT = pathlib.Path(os.environ.get('EVAL_ROOT', '')).resolve()
MODELS = {'opus': 'opus', 'sol': 'gpt-6.1-sol'}
EFFORT = 'medium'
MAINTAINER_ONLY = shutil.ignore_patterns('.git', 'evals', 'README.md', 'AGENTS.md', 'node_modules')
GIT = ['git', '-c', 'user.name=eval', '-c', 'user.email=eval@example.invalid', '-c', 'core.autocrlf=false']
ENV_ALLOW = {'PATH', 'PATHEXT', 'SYSTEMROOT', 'SYSTEMDRIVE', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP', 'TMPDIR', 'HOME',
             'USERPROFILE', 'HOMEDRIVE', 'HOMEPATH', 'APPDATA', 'LOCALAPPDATA', 'PROGRAMDATA', 'PROGRAMFILES',
             'PROGRAMFILES(X86)', 'COMMONPROGRAMFILES', 'NUMBER_OF_PROCESSORS', 'PROCESSOR_ARCHITECTURE', 'OS',
             'USERNAME', 'LANG', 'LC_ALL', 'TERM', 'SHELL'}


def guard():
    if not os.environ.get('EVAL_ROOT'):
        sys.exit('Set EVAL_ROOT to a run folder outside the home folder and every Git repository.')
    if ROOT == HOME or HOME in ROOT.parents:
        sys.exit(f'{ROOT} is inside the home folder.')
    ROOT.mkdir(parents=True, exist_ok=True)
    if subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, capture_output=True).returncode == 0:
        sys.exit(f'{ROOT} is inside a Git repository.')
    for folder in [ROOT, *ROOT.parents]:
        found = [n for n in ('.claude', '.agents', 'CLAUDE.md', 'AGENTS.md') if (folder / n).exists()]
        if found:
            sys.exit(f'{folder} holds {", ".join(found)}, which a session would discover.')


def finished(record, model):
    """True when the turn's terminal event is a success: a non-error result for Claude Code, a completed turn and no failure for Codex."""
    evs = []
    for line in record.read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            evs.append(json.loads(line))
        except ValueError:
            pass
    if model == 'sol':
        terminal = [e for e in evs if e.get('type') in ('turn.completed', 'turn.failed')]
        return bool(terminal) and terminal[-1].get('type') == 'turn.completed'
    results = [e for e in evs if e.get('type') == 'result']
    return bool(results) and results[-1].get('subtype') == 'success' and not results[-1].get('is_error')


def skill_name(skill_dir):
    for line in (skill_dir / 'SKILL.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('name:'):
            return line.split(':', 1)[1].strip().strip('"')
    sys.exit('SKILL.md has no name')


def build_fixture(fixture, work):
    shutil.copytree(FIXTURES / 'base', work)
    if fixture != 'base':
        shutil.copytree(FIXTURES / fixture, work, dirs_exist_ok=True)
    subprocess.run([*GIT, 'init', '-q'], cwd=work, check=True)
    subprocess.run([*GIT, 'add', '-A'], cwd=work, check=True)
    subprocess.run([*GIT, 'commit', '-qm', 'fixture'], cwd=work, check=True)


def head(work):
    subprocess.run([*GIT, 'add', '-A'], cwd=work, check=True)
    subprocess.run([*GIT, 'commit', '-qm', 'turn', '--allow-empty'], cwd=work, check=True)
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=work, capture_output=True, text=True).stdout.strip()


def session_id(record, model):
    text = record.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'"session_id":\s*"([^"]+)"' if model == 'opus' else r'"thread_id":\s*"([^"]+)"', text)
    return m.group(1) if m else None


def main():
    guard()
    label, name, model = sys.argv[1:4]
    skill_dir = pathlib.Path(sys.argv[4]).resolve() if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 900
    spec = next((e for e in json.loads(EVALS.read_text(encoding='utf-8'))['evals'] if e['name'] == name), None)
    if not spec:
        sys.exit(f'no eval named {name}')
    base = ROOT / 'builds' / label
    if base.exists():
        sys.exit(f'{base} exists')
    work, cfg = base / 'work', base / 'cfg'
    base.mkdir(parents=True)
    build_fixture(spec['fixture'], work)
    cfg.mkdir()
    # The copied credentials leave with the process, even when a turn raises.
    atexit.register(lambda: [(cfg / s).unlink(missing_ok=True) for s in ('.credentials.json', 'auth.json')])
    env = {k: v for k, v in os.environ.items() if k.upper() in ENV_ALLOW}
    if model == 'opus':
        shutil.copyfile(HOME / '.claude/.credentials.json', cfg / '.credentials.json')
        if skill_dir:
            shutil.copytree(skill_dir, work / '.claude/skills' / skill_name(skill_dir), ignore=MAINTAINER_ONLY)
        env.update(CLAUDE_CONFIG_DIR=str(cfg), CLAUDE_CODE_DISABLE_AUTO_MEMORY='1', DISABLE_AUTOUPDATER='1', DISABLE_TELEMETRY='1')
    elif model == 'sol':
        shutil.copyfile(HOME / '.codex/auth.json', cfg / 'auth.json')
        if skill_dir:
            shutil.copytree(skill_dir, work / '.agents/skills' / skill_name(skill_dir), ignore=MAINTAINER_ONLY)
        env.update(CODEX_HOME=str(cfg))
    else:
        sys.exit('model must be opus or sol')
    turns, sid = [], None
    for n, prompt in enumerate(spec['turns'], 1):
        if not skill_dir:
            # The none arm has no skill to load, so the request to load it would only confuse the session.
            prompt = prompt.replace('Load the ask-questions skill and follow it for this work. ', '')
        before = head(work)
        record = base / f'turn-{n}.jsonl'
        if model == 'opus':
            args = [shutil.which('claude'), '-p', '--dangerously-skip-permissions', '--model', MODELS['opus'], '--effort', EFFORT,
                    '--strict-mcp-config', '--no-chrome', '--output-format', 'stream-json', '--verbose']
            args += ['--resume', sid, prompt] if sid else [prompt]
        else:
            last = str(base / f'turn-{n}-last.txt')
            common = ['--skip-git-repo-check', '--dangerously-bypass-approvals-and-sandbox', '--ignore-rules', '-m', MODELS['sol'],
                      '-c', f'model_reasoning_effort="{EFFORT}"', '--json', '-o', last]
            args = [shutil.which('codex'), 'exec', 'resume', sid, *common, prompt] if sid else [shutil.which('codex'), 'exec', *common, '-C', str(work), prompt]
        start = time.time()
        with open(record, 'w', encoding='utf-8') as out, open(base / f'turn-{n}-stderr.txt', 'w', encoding='utf-8') as err:
            p = subprocess.Popen(args, cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
            while p.poll() is None and time.time() - start < timeout:
                time.sleep(5)
            timed_out = p.poll() is None
            if timed_out:
                subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True) if os.name == 'nt' else p.kill()
                p.wait()
        sid = sid or session_id(record, model)
        done = finished(record, model) and not timed_out and p.returncode == 0
        turns.append({'turn': n, 'before': before, 'exit': p.returncode, 'timed_out': timed_out, 'completed': done,
                      'seconds': round(time.time() - start, 1)})
        if not done or not sid:
            break
    cli = subprocess.run([shutil.which('claude' if model == 'opus' else 'codex'), '--version'], capture_output=True, text=True).stdout.strip()
    result = {'label': label, 'eval': name, 'model': model, 'requested_model': MODELS[model], 'cli': cli, 'session_id': sid, 'turns': turns, 'after': head(work),
              'completed': len(turns) == len(spec['turns']) and all(t['completed'] for t in turns)}
    (base / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
