from pathlib import Path
from ghipm.data_io.forage_in import load_forage_in
from ghipm.data_io.yield_dat import load_yield_scalars
from ghipm.data_io.weather import load_monthly_tmean_C

def test_forage_in(tmp_path: Path):
    p = tmp_path / "FORAGE.IN"
    p.write_text("90.0 wdpsc\n37.0 wtmax\n28.0 wtopt\n10.0 wtmin\n60.0 cdpsc\n37.0 ctmax\n28.0 ctopt\n7.0 ctmin\n60.0 fdpsc\n37.0 ftmax\n28.0 ftopt\n7.0 ftmin\n")
    fp = load_forage_in(p)
    assert fp.wdpsc == 90.0 and fp.ftopt == 28.0

def test_yield_dat(tmp_path: Path):
    p = tmp_path / "YIELD$.DAT"
    p.write_text("No Treatment\n374\nAcephate\n458\n")
    yd = load_yield_scalars(p)
    assert yd["base"] == 374
    assert abs(yd["relative"]["Acephate"] - (458/374)) < 1e-9

def test_weather(tmp_path: Path):
    p = tmp_path / "CURRENT.WTR"
    p.write_text("1  50.0  40.0  0.00 200.0\n2  60.0  45.0  0.00 250.0\n")
    m = load_monthly_tmean_C(p, column3_is_tavgF=True)
