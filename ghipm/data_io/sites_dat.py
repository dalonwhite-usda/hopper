from dataclasses import dataclass, field
import pathlib
from typing import Listfrom pathlib import Path

@dataclass
class SiteBlock:
    site: str
    lat: float
    lon: float
    rows: List[List[float]] = field(default_factory=list)

def load_sites_dat(path: Path) -> List[SiteBlock]:
    SITE_NAME = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")
    FLOATS    = re.compile(r"^\s*([-\d\.E+]+\s+)+[-\d\.E+]\s*$")
    lines = path.read_text().splitlines()
    i, n = 0, len(lines)
    blocks: List[SiteBlock] = []
    while i < n:
        line = lines[i].strip()
        if SITE_NAME.match(line):
            site = line
            i += 1
            latlon = [float(x) for x in lines[i].split()]
            if len(latlon) != 2: raise ValueError(f"{site}: expected lat lon")
            block = SiteBlock(site=site, lat=latlon[0], lon=latlon[1]); i += 1
            while i < n and not SITE_NAME.match(lines[i].strip()):
                if FLOATS.match(lines[i]):
                    block.rows.append([float(x) for x in lines[i].split()])
                i += 1
            blocks.append(block)
        else:
            i += 1
    if not blocks: raise ValueError("No site blocks found")
    return blocks
import re
