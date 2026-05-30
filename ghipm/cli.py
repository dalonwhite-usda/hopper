import argparse
from pathlib import Path

import pyomo.environ as pyo

from ghipm.bio.forage_model import monthly_forage_lbs_per_acre
from ghipm.data_io.forage_in import load_forage_in
from ghipm.data_io.weather import load_monthly_tmean_C
from ghipm.data_io.yield_dat import load_yield_scalars
from ghipm.econ_lp.model import build_model
from ghipm.econ_lp.scenarios import build_treatments


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True, help="Folder with legacy files")
    ap.add_argument("--solver", type=str, default="glpk", help="glpk|cbc|gurobi|cplex|appsi_highs")
    args = ap.parse_args()

    forage_params = load_forage_in(args.root / "FORAGE.IN")
    tmean_c = load_monthly_tmean_C(args.root / "CURRENT.WTR", column3_is_tavgF=True)
    yield_info = load_yield_scalars(args.root / "YIELD$.DAT")
    treatments = build_treatments(yield_info["absolute"])
    base_monthly = monthly_forage_lbs_per_acre(tmean_c, forage_params, annual_abs_lbs=yield_info["base"])

    treated_acres = 16044
    brood_cows = 480
    req_lb_per_cow_month = 780.0
    hay_buy_cost_per_ton = 80.0
    grass_hay_inventory_lbs = 300 * 1.5 * 2000.0
    allowed_months = ["MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    blm_total_aum = 723
    state_total_aum = 138
    price_per_aum = 1.92
    lb_per_aum = 780.0

    data = {
        "herd": {"brood_cows": brood_cows, "req_lb_per_cow_month": req_lb_per_cow_month},
        "block": {"acres": treated_acres},
        "forage": {"monthly_lbs_per_acre": base_monthly},
        "hay": {"buy_cost_per_ton": hay_buy_cost_per_ton, "inventory_lbs": grass_hay_inventory_lbs},
        "lease": {
            "allowed_months": allowed_months,
            "blm_total_AUM": blm_total_aum,
            "state_total_AUM": state_total_aum,
            "price_per_AUM": price_per_aum,
            "lb_per_AUM": lb_per_aum,
        },
    }

    opt = pyo.SolverFactory(args.solver)
    baseline_tr = next(t for t in treatments if t.name == "No Treatment")
    baseline_model = build_model(months=list(base_monthly.keys()), data=data, treatment=baseline_tr)
    res = opt.solve(baseline_model, tee=False)
    baseline_model.solutions.load_from(res)
    ret0 = float(baseline_model.OBJ())

    print("\nTreatment           Yield(lbs/ac)    Cost($)     Return Delta($)    B/C")
    print("-----------------------------------------------------------------------")
    for tr in treatments:
        model = build_model(months=list(base_monthly.keys()), data=data, treatment=tr)
        res = opt.solve(model, tee=False)
        model.solutions.load_from(res)
        ret = float(model.OBJ())
        delta = ret - ret0
        cost_total = tr.cost_per_acre * treated_acres
        bc_ratio = (delta / cost_total) if cost_total > 0 else 0.0
        print(f"{tr.name:18s} {tr.forage_scalar_abs:12.0f} {cost_total:12,.0f} {delta:12,.0f}  {bc_ratio:>5.2f}")


if __name__ == "__main__":
    main()
