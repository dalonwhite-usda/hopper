from dataclasses import dataclass


@dataclass
class Treatment:
    name: str
    cost_per_acre: float
    mortality_pct: float
    forage_scalar_abs: float
    eggs_per_yd2: float = 0.0


def build_treatments(yield_abs: dict) -> list:
    return [
        Treatment("No Treatment", cost_per_acre=0.00, mortality_pct=0.0, forage_scalar_abs=yield_abs["No Treatment"], eggs_per_yd2=0.0),
        Treatment("Acephate", cost_per_acre=2.47, mortality_pct=91.0, forage_scalar_abs=yield_abs["Acephate"], eggs_per_yd2=5.7),
        Treatment("Carbaryl Bait", cost_per_acre=4.50, mortality_pct=73.0, forage_scalar_abs=yield_abs["Carbaryl Bait"], eggs_per_yd2=10.5),
        Treatment("Carbaryl Spray", cost_per_acre=3.50, mortality_pct=92.0, forage_scalar_abs=yield_abs["Carbaryl Spray"], eggs_per_yd2=9.1),
        Treatment("Malathion", cost_per_acre=2.25, mortality_pct=90.0, forage_scalar_abs=yield_abs["Malathion"], eggs_per_yd2=5.4),
        Treatment("Nosema Bait", cost_per_acre=4.75, mortality_pct=50.0, forage_scalar_abs=yield_abs["Nosema Bait"], eggs_per_yd2=20.2),
    ]
