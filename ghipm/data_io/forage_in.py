from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class ForageParams:
    wdpsc: float
    wtmax: float
    wtopt: float
    wtmin: float
    cdpsc: float
    ctmax: float
    ctopt: float
    ctmin: float
    fdpsc: float
    ftmax: float
    ftopt: float
    ftmin: float


KEYS = {
    "wdpsc": "wdpsc",
    "wtmax": "wtmax",
    "wtopt": "wtopt",
    "wtmin": "wtmin",
    "cdpsc": "cdpsc",
    "ctmax": "ctmax",
    "ctopt": "ctopt",
    "ctmin": "ctmin",
    "fdpsc": "fdpsc",
    "ftmax": "ftmax",
    "ftopt": "ftopt",
    "ftmin": "ftmin",
}


def load_forage_in(path: Path) -> ForageParams:
    vals = {}
    pat = re.compile(r"^\s*([-\d\.Ee\+]+)\s+([A-Za-z]+)")
    for line in path.read_text().splitlines():
        m = pat.match(line)
        if not m:
            continue
        val, key = float(m.group(1)), m.group(2).lower()
        if key in KEYS:
            vals[KEYS[key]] = val

    missing = [k for k in KEYS.values() if k not in vals]
    if missing:
        raise ValueError(f"FORAGE.IN missing keys: {missing}")
    return ForageParams(**vals)
