from collections import defaultdict
from pathlib import Path


def _doy_to_month(doy: int) -> int:
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    cum = 0
    for m, md in enumerate(month_days, start=1):
        cum += md
        if doy <= cum:
            return m
    return 12


def load_monthly_tmean_C(path: Path, column3_is_tavgF: bool = True) -> dict:
    sum_c = defaultdict(float)
    cnt = defaultdict(int)
    with path.open() as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            parts = raw.split()
            if len(parts) < 3:
                continue
            try:
                doy = int(float(parts[0]))
                tmax_f = float(parts[1])
                t3_f = float(parts[2])
            except ValueError:
                continue

            tavg_f = t3_f if column3_is_tavgF else (tmax_f + t3_f) / 2.0
            tavg_c = (tavg_f - 32.0) * (5.0 / 9.0)
            m = _doy_to_month(doy)
            sum_c[m] += tavg_c
            cnt[m] += 1

    names = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    }
    return {names[m]: (sum_c[m] / cnt[m] if cnt[m] else 0.0) for m in range(1, 13)}
