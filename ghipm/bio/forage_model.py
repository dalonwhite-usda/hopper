from typing import Dict

from .phenology import active_fraction
from .temp_response import triangular_temp_factor


def monthly_forage_weights(tmean_by_month: Dict[str, float], params) -> Dict[str, float]:
    w = {}
    for m, temp_c in tmean_by_month.items():
        warm = triangular_temp_factor(temp_c, params.wtmin, params.wtopt, params.wtmax) * active_fraction(params.wdpsc)
        cool = triangular_temp_factor(temp_c, params.ctmin, params.ctopt, params.ctmax) * active_fraction(params.cdpsc)
        forb = triangular_temp_factor(temp_c, params.ftmin, params.ftopt, params.ftmax) * active_fraction(params.fdpsc)
        w[m] = max(0.0, (0.5 * warm + 0.35 * cool + 0.15 * forb))
    return w


def monthly_forage_lbs_per_acre(tmean_by_month: Dict[str, float], params, annual_abs_lbs: float) -> Dict[str, float]:
    w = monthly_forage_weights(tmean_by_month, params)
    total = sum(w.values()) or 1.0
    return {m: (annual_abs_lbs * (w[m] / total)) for m in w}
