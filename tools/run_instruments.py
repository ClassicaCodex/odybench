"""
The lean run's instrument record (LEAN.md, "Instrument checks kept").

Runs every unit test and every script's --selftest, plus I1 (validate_ephem),
and writes results/instrument/summary.json with INSTR = true only if all of
them pass. verdict.py reads INSTR from that file.

I1's full output prints quantities of the target's sky (DESIGN 7.1, the sealed
list), so it is written to results/instrument/i1_full.sealed.txt and only its
"N/M passed" line is read here.

Usage:  py tools/run_instruments.py
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "instrument"

TESTS = sorted(p.name for p in (ROOT / "tests").glob("test_*.py"))
SELFTESTS = ["attain.py", "rates.py", "reproduce.py", "heldout.py", "deltat.py",
             "almagest.py"]          # verdict.py is covered by tests/test_lean_verdict.py


def run(name, cmd, sealed=False, timeout=3600):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    t0 = time.time()
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=timeout)
    out = (p.stdout or "") + (p.stderr or "")
    path = OUT / (name.replace("/", "_") + (".sealed.txt" if sealed else ".out.txt"))
    path.write_text(out, encoding="utf-8")
    rec = {"name": name, "cmd": " ".join(cmd), "exit": p.returncode,
           "seconds": round(time.time() - t0, 1), "output": str(path.relative_to(ROOT))}
    if sealed:
        m = re.findall(r"^(\d+)/(\d+) passed", out, re.M)
        rec["summary"] = f"{m[-1][0]}/{m[-1][1]} passed" if m else "no summary line"
        rec["ok"] = bool(m) and m[-1][0] == m[-1][1] and p.returncode == 0
    else:
        rec["ok"] = p.returncode == 0
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] if out.strip() else []
        rec["summary"] = tail[0][:200] if tail else ""
    print(f"[{'PASS' if rec['ok'] else 'FAIL'}] {name}  ({rec['seconds']} s)  {rec['summary']}")
    return rec


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    checks = [run("I1 validate_ephem", [py, "tools/validate_ephem.py"], sealed=True)]
    for t in TESTS:
        checks.append(run(f"tests/{t}", [py, f"tests/{t}"]))
    for s in SELFTESTS:
        if (ROOT / s).exists():
            checks.append(run(f"{s} --selftest", [py, s, "--selftest"]))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()
    summary = {"INSTR": all(c["ok"] for c in checks), "n_checks": len(checks),
               "n_failed": sum(not c["ok"] for c in checks), "git_head": head,
               "checks": checks}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"\nINSTR = {summary['INSTR']}  ({summary['n_checks'] - summary['n_failed']}/{summary['n_checks']} passed)")
    return 0 if summary["INSTR"] else 1


if __name__ == "__main__":
    sys.exit(main())
