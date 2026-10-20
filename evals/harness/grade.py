"""Grade the check assertions of ask-questions eval sessions, and package the semantic ones for critics.

Usage: python grade.py <jobs file> <round>
Environment: EVAL_ROOT, the run folder run.py used.

A question is counted two ways per turn: attempted question-tool calls in the turn's record
(AskUserQuestion in Claude Code, request_user_input in Codex), whether or not the host accepted
them, and sentences ending in a question mark in the turn's final message. Whether any message of
the turn, commentary included, asks the user for input is a semantic assertion the critics grade
from turn-<n>-messages.txt. claude -p offers no question tool, so an attempt is reported as a setup
failure, and every check that counts asking also requires zero attempts. A session in a skill arm
that never loaded the skill is reported as not measured, since its result says nothing about the
skill. A missing or unfinished session fails every assertion.

Writes EVAL_ROOT/grades-<round>.json and one blind package per eval under
EVAL_ROOT/judge/<round>-<eval>/ (prompt turns, semantic assertions, and per letter each turn's final
message, every message of the turn, the diff of each turn, and the resulting project), with the
letter-to-session key in EVAL_ROOT/keys, outside the folder critics work in.
"""
import json, os, pathlib, random, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
EVALS = {e['name']: e for e in json.loads((HERE.parent / 'evals.json').read_text(encoding='utf-8'))['evals']}
ROOT = pathlib.Path(os.environ.get('EVAL_ROOT', '')).resolve()
LABEL = re.compile(r'(\d+)-(.+)-(old|new|none)-(opus|sol)$')
IMPORTS_HELPERS = re.compile(r"""(from|import|require)\s*\(?\s*['"][^'"]*helpers""")
QUESTION_TOOLS = ('AskUserQuestion', 'request_user_input')


def records(base, n):
    p = base / f'turn-{n}.jsonl'
    out = []
    for line in (p.read_text(encoding='utf-8', errors='replace').splitlines() if p.is_file() else []):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def tool_questions(base, n):
    """Question-tool attempts in one turn, as lists of question texts."""
    calls = []
    for e in records(base, n):
        for c in e.get('message', {}).get('content', []) if e.get('type') == 'assistant' else []:
            if c.get('type') == 'tool_use' and c.get('name') in QUESTION_TOOLS:
                calls.append([q.get('question', '') for q in c.get('input', {}).get('questions', [])] or [json.dumps(c.get('input'))])
        item = e.get('item') or {}
        # Only an actual tool invocation counts. A message that names the tool is prose.
        if e.get('type') == 'item.completed' and item.get('type') not in ('agent_message', 'reasoning', 'command_execution', 'file_change') \
                and (item.get('tool') in QUESTION_TOOLS or item.get('name') in QUESTION_TOOLS):
            calls.append([json.dumps(item.get('arguments') or item)[:300]])
    return calls


def final_message(base, n, model):
    if model == 'sol':
        p = base / f'turn-{n}-last.txt'
        return p.read_text(encoding='utf-8', errors='replace') if p.is_file() else ''
    for e in reversed(records(base, n)):
        if e.get('type') == 'result':
            return e.get('result') or ''
    return ''


def turn_messages(base, n, model):
    """Every message the model wrote to the user during one turn, commentary before tool calls included, then the final one."""
    out = []
    for e in records(base, n):
        if e.get('type') == 'assistant':
            out += [c.get('text', '') for c in e.get('message', {}).get('content', []) if c.get('type') == 'text']
        item = e.get('item') or {}
        if e.get('type') == 'item.completed' and item.get('type') == 'agent_message':
            out.append(item.get('text', ''))
    final = final_message(base, n, model)
    if final and final not in out:
        out.append(final)
    return '\n\n'.join(out)


def text_questions(message):
    """Sentences that end in a question mark, outside code, quotes, and URLs."""
    prose = re.sub(r'```.*?```', ' ', message, flags=re.S)
    prose = re.sub(r'`[^`\n]*`', ' ', prose)
    prose = re.sub(r'^>[^\n]*$', ' ', prose, flags=re.M)
    prose = re.sub(r'\S+\?\S+', ' ', prose)
    return [s.strip() for s in re.findall(r'[^.!?\n]*\?', prose) if len(s.strip()) > 3]


def skill_read(base, turns):
    """True when the opening and closing lines of the installed SKILL.md body both came back to the model in some turn."""
    root = next((base / 'work' / d / 'skills' / 'ask-questions' for d in ('.claude', '.agents') if (base / 'work' / d / 'skills' / 'ask-questions').is_dir()), None)
    if not root:
        return False
    body = [l.strip() for l in (root / 'SKILL.md').read_text(encoding='utf-8').splitlines() if l.strip() and not l.strip().startswith(('#', '---', 'name:', 'description:', 'metadata:', 'author:', 'version:'))]
    norm = lambda t: re.sub(r'\s+', ' ', t)
    parts = (norm(body[0])[:80], norm(body[-1])[-80:])
    returned = []
    for n in range(1, turns + 1):
        for e in records(base, n):
            if e.get('type') == 'user':
                content = e.get('message', {}).get('content', [])
                for c in content if isinstance(content, list) else [{'text': content}]:
                    body = c.get('content') if c.get('type') == 'tool_result' else c.get('text')
                    if isinstance(body, list):
                        body = ' '.join(b.get('text', '') for b in body if isinstance(b, dict))
                    returned.append(norm(str(body or '')))
            item = e.get('item') or {}
            if item.get('type') == 'command_execution':
                returned.append(norm(item.get('aggregated_output') or ''))
    return all(any(p in t for t in returned) for p in parts)


def git(work, *args):
    return subprocess.run(['git', *args], cwd=work, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout or ''


def checks(base, model, result):
    work = base / 'work'
    none_asked = lambda n: not tool_questions(base, n) and not text_questions(final_message(base, n, model))
    return {
        'answered-in-the-request-01': lambda: none_asked(1),
        'obvious-next-step-01': lambda: (work / 'src/format/date.ts').is_file() and (work / 'src/format/money.ts').is_file()
            and not (work / 'src/helpers').exists() and not IMPORTS_HELPERS.search(git(work, 'grep', '-n', 'helpers', '--', 'src')),
        'obvious-next-step-02': lambda: none_asked(1),
        'safe-assumption-01': lambda: none_asked(1),
        'decision-only-the-user-can-make-02': lambda: not tool_questions(base, 1) and len(text_questions(final_message(base, 1, model))) <= 2,
        'one-decision-at-a-time-01': lambda: not tool_questions(base, 1) and len(text_questions(final_message(base, 1, model))) <= 2,
    }


def main():
    jobs_file, rnd = sys.argv[1], sys.argv[2]
    labels = [l.split()[0] for l in pathlib.Path(jobs_file).read_text().splitlines() if l.strip() and not l.startswith('#')]
    rows = []
    for label in [l for l in labels if l.startswith(f'{rnd}-')]:
        m = LABEL.match(label)
        name, arm, model = m.group(2), m.group(3), m.group(4)
        base = ROOT / 'builds' / label
        result = json.loads((base / 'result.json').read_text(encoding='utf-8')) if (base / 'result.json').is_file() else {}
        ids = [a['id'] for a in EVALS[name]['assertions'] if a['kind'] == 'check']
        table = checks(base, model, result) if result.get('completed') else {}
        verdicts = {}
        for i in ids:
            try:
                verdicts[i] = bool(table[i]()) if i in table else False
            except Exception:
                verdicts[i] = False
        asked = {n + 1: {'tool': tool_questions(base, n + 1), 'text': text_questions(turn_messages(base, n + 1, model))}
                 for n in range(len(EVALS[name]['turns']))}
        rows.append({'build': label, 'eval': name, 'arm': arm, 'model': model, 'completed': bool(result.get('completed')),
                     'skill_read': skill_read(base, len(EVALS[name]['turns'])), 'checks': verdicts, 'asked': asked})
    (ROOT / f'grades-{rnd}.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    for r in rows:
        fails = [k for k, v in r['checks'].items() if not v]
        attempted = any(v['tool'] for v in r['asked'].values())
        # A skill-arm session that never loaded the skill says nothing about it, whether its checks passed or failed.
        # A question-tool attempt is a setup failure and is reported first.
        if not r['completed']:
            state = 'MISSING'
        elif attempted:
            state = 'SETUP: question tool offered'
        elif r['arm'] != 'none' and not r['skill_read']:
            state = 'NOT MEASURED: skill never loaded'
        else:
            state = 'ok' if not fails else 'FAIL ' + ','.join(fails)
        print(f"{r['build']:52} {state}")
    rng = random.Random(rnd)
    for name in sorted({r['eval'] for r in rows}):
        folder = ROOT / 'judge' / f'{rnd}-{name}'
        if folder.exists():
            continue
        sel = [r for r in rows if r['eval'] == name and r['completed']]
        rng.shuffle(sel)
        folder.mkdir(parents=True)
        (folder / 'turns.json').write_text(json.dumps(EVALS[name]['turns'], indent=2), encoding='utf-8')
        (folder / 'semantic.json').write_text(json.dumps([a for a in EVALS[name]['assertions'] if a['kind'] == 'semantic'], indent=2), encoding='utf-8')
        key = {}
        for i, r in enumerate(sel):
            letter, base = chr(ord('A') + i), ROOT / 'builds' / r['build']
            result = json.loads((base / 'result.json').read_text(encoding='utf-8'))
            out = folder / letter
            shutil.copytree(base / 'work', out / 'project', ignore=shutil.ignore_patterns('.git', '.claude', '.agents'))
            for t in result['turns']:
                n = t['turn']
                after = result['turns'][n]['before'] if n < len(result['turns']) else result['after']
                (out / f'turn-{n}-answer.txt').write_text(final_message(base, n, r['model']), encoding='utf-8')
                # Every message of the turn, so the critics can judge requests for input a regex cannot see.
                (out / f'turn-{n}-messages.txt').write_text(turn_messages(base, n, r['model']), encoding='utf-8')
                (out / f'turn-{n}-diff.txt').write_text(git(base / 'work', 'diff', '--no-color', t['before'], after, '--', '.', ':!.claude', ':!.agents'), encoding='utf-8')
            key[letter] = r['build']
        (ROOT / 'keys').mkdir(exist_ok=True)
        (ROOT / 'keys' / f'{folder.name}.json').write_text(json.dumps(key, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
