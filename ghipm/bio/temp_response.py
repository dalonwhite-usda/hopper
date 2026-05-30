def triangular_temp_factor(temp_c: float, t_min: float, t_opt: float, t_max: float) -> float:
    """Piecewise-linear triangular response in [0, 1]."""
    if t_max <= t_min:
        return 0.0
    if temp_c <= t_min or temp_c >= t_max:
        return 0.0
    if temp_c == t_opt:
        return 1.0
    if temp_c < t_opt:
        return (temp_c - t_min) / (t_opt - t_min) if t_opt > t_min else 0.0
    return (t_max - temp_c) / (t_max - t_opt) if t_max > t_opt else 0.0


def triangular_temp_factor(T, Tmin, Topt, Tmax) -> float:
    if T <= Tmin or T >= Tmax:
        return 0.0
    if T <= Topt:
        return (T - Tmin) / (Topt - Tmin)
    return (Tmax - T) / (Tmax - Topt)
