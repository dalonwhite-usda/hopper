from pathlib import Path


def load_yield_scalars(path: Path) -> dict:
    lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
    out = {}
    i = 0
    while i < len(lines):
        name = lines[i]
        i += 1
        if i >= len(lines):
            raise ValueError("YIELD$.DAT malformed")
        out[name] = float(lines[i])
        i += 1

    base = out.get("No Treatment")
    rel = {k: (v / base) for k, v in out.items()} if base else out
    return {"absolute": out, "relative": rel, "base": base}
