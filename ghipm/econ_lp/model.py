import pyomo.environ as pyo


def build_model(months, data, treatment):
    m = pyo.ConcreteModel()
    m.M = pyo.Set(initialize=months)

    # Herd
    m.cows = pyo.Param(initialize=data["herd"]["brood_cows"], within=pyo.NonNegativeReals)
    m.req_lb_per_cow_month = pyo.Param(initialize=data["herd"]["req_lb_per_cow_month"])

    # Treated block & pre-treatment monthly forage (lbs/acre)
    m.treated_acres = pyo.Param(initialize=data["block"]["acres"])
    m.forage_lbs_per_acre = pyo.Param(m.M, initialize=data["forage"]["monthly_lbs_per_acre"])

    # Hay
    m.hay_buy_cost_per_ton = pyo.Param(initialize=data["hay"]["buy_cost_per_ton"])
    m.hay_inventory_lbs = pyo.Param(initialize=data["hay"]["inventory_lbs"])
    m.hay_use = pyo.Var(m.M, domain=pyo.NonNegativeReals)
    m.hay_buy_ton = pyo.Var(m.M, domain=pyo.NonNegativeReals)

    # Leases
    allowed = set(data["lease"]["allowed_months"])
    m.lease_AUM_to_lbs = pyo.Param(initialize=data["lease"]["lb_per_AUM"])
    m.blm_total_AUM = pyo.Param(initialize=data["lease"]["blm_total_AUM"])
    m.state_total_AUM = pyo.Param(initialize=data["lease"]["state_total_AUM"])
    m.lease_price_per_AUM = pyo.Param(initialize=data["lease"]["price_per_AUM"])
    m.blm_use_AUM = pyo.Var(m.M, domain=pyo.NonNegativeReals)
    m.state_use_AUM = pyo.Var(m.M, domain=pyo.NonNegativeReals)

    # Rescale base forage to treatment annual absolute yield
    sum_base = sum(pyo.value(m.forage_lbs_per_acre[mm]) for mm in m.M)
    scale = (treatment.forage_scalar_abs / sum_base) if sum_base else 1.0
    natural_forage = {mm: pyo.value(m.treated_acres * m.forage_lbs_per_acre[mm] * scale) for mm in months}
    m.natural_forage_lbs = pyo.Param(m.M, initialize=natural_forage)

    # Constraints
    m.HayInvBal = pyo.Constraint(expr=sum(m.hay_use[mm] for mm in m.M) <= m.hay_inventory_lbs)
    m.BLMCap = pyo.Constraint(expr=sum(m.blm_use_AUM[mm] for mm in m.M if mm in allowed) <= m.blm_total_AUM)
    m.StateCap = pyo.Constraint(expr=sum(m.state_use_AUM[mm] for mm in m.M if mm in allowed) <= m.state_total_AUM)

    def bal_rule(_model, mm):
        herd_need = m.cows * m.req_lb_per_cow_month
        leased_lbs = m.lease_AUM_to_lbs * (
            (m.blm_use_AUM[mm] if mm in allowed else 0.0) + (m.state_use_AUM[mm] if mm in allowed else 0.0)
        )
        return herd_need <= m.natural_forage_lbs[mm] + m.hay_use[mm] + leased_lbs + m.hay_buy_ton[mm] * 2000.0

    m.MonthlyBal = pyo.Constraint(m.M, rule=bal_rule)

    # Objective (Return = - costs; revenue terms can be added later)
    feed_costs = sum(m.hay_buy_cost_per_ton * m.hay_buy_ton[mm] for mm in m.M)
    lease_costs = m.lease_price_per_AUM * (
        sum(m.blm_use_AUM[mm] for mm in allowed) + sum(m.state_use_AUM[mm] for mm in allowed)
    )
    treatment_cost = treatment.cost_per_acre * m.treated_acres

    m.OBJ = pyo.Objective(expr=-feed_costs - lease_costs - treatment_cost, sense=pyo.maximize)
    return m
