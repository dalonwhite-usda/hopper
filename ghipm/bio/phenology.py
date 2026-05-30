def active_fraction(dpsc_percent: float) -> float:
    """Convert seasonal activity percent to unit fraction."""
    return max(0.0, min(1.0, float(dpsc_percent) / 100.0))


def active_fraction(days_in_window: int, days_in_month: int = 30) -> float:
    return min(1.0, max(0.0, days_in_month / max(1, days_in_window)))
