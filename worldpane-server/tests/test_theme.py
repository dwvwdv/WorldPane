"""Offbeat theme guards (docs/ui-conventions.md).

``static/offbeat.css`` is the only place a color is written; the pages use its semantic tokens.
A hex or ``rgb()`` literal in a page means the page picked a color itself, which is how the old
light/dark variable sets drifted apart.
"""

from __future__ import annotations

import re
from importlib import resources

import pytest

from worldpane_server.demo import page_document
from worldpane_server.theme import OFFBEAT_PLACEHOLDER, offbeat_css, with_offbeat

PAGES = ["dashboard.html", "demo.html"]

NORD = {
    "2E3440", "3B4252", "434C5E", "4C566A",  # polar night
    "D8DEE9", "E5E9F0", "ECEFF4",            # snow storm
    "8FBCBB", "88C0D0", "81A1C1", "5E81AC",  # frost
    "BF616A", "D08770", "EBCB8B", "A3BE8C", "B48EAD",  # aurora
}

# Offbeat tokens v1 的衍生值：為了讓文字在 polar0／polar1／polar2 三層都 ≥ 4.5:1、控制項外框 ≥ 3:1 而加。
# 只收設計系統裡有的值，頁面或這個檔案自己調出來的顏色一樣會被擋下。
OFFBEAT_DERIVED = {
    "B8BDC8",  # dim-ink
    "93C6D4",  # frost-ink
    "F4ABB2", "B0CB98", "F3AE95", "D9B2D3",  # red／green／orange／purple ink（深色）
    "838EA6",  # control-dark
    "A54049", "8F3A42",  # danger fill／hover
}

# scrim 是唯一的黑色半透明：它調暗頁面，不是陰影。
SCRIM_RGB = (0, 0, 0)

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB = re.compile(r"rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)")


def _static(name: str) -> str:
    return resources.files("worldpane_server").joinpath(f"static/{name}").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", PAGES)
def test_pages_write_no_colors(name):
    source = _static(name)
    assert not HEX.findall(source), f"{name}: use an offbeat.css token instead of a hex color"
    assert not RGB.findall(source), f"{name}: use an offbeat.css token instead of rgb()"
    assert "--nord-" not in source, f"{name}: pages use semantic tokens, not the raw Nord palette"


@pytest.mark.parametrize("name", PAGES)
def test_pages_inline_the_theme_once(name):
    source = _static(name)
    assert source.count(OFFBEAT_PLACEHOLDER) == 1
    assert source.index("<style>") < source.index(OFFBEAT_PLACEHOLDER) < source.index("</style>")
    page = with_offbeat(source)
    assert OFFBEAT_PLACEHOLDER not in page
    assert offbeat_css() in page


def test_aurora_red_is_never_text():
    # #BF616A on the polar1 panel is 2.46:1; error messages and danger buttons must stay readable.
    for name, source in [("offbeat.css", offbeat_css())] + [(p, _static(p)) for p in PAGES]:
        assert not re.search(r"(?<![-\w])color:\s*var\(--danger\)", source), name


def test_offbeat_colors_come_from_the_design_system():
    css = offbeat_css()
    hexes = {h.upper() for h in HEX.findall(css)}
    assert hexes == NORD | OFFBEAT_DERIVED
    nord_rgb = {tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in NORD}
    for rgb in RGB.findall(css):
        assert tuple(map(int, rgb)) in nord_rgb | {SCRIM_RGB}, f"rgb{rgb} is not a Nord color"


def test_shadows_are_solid():
    # 偏移陰影是 Nord 色票的實色塊：--shadow* 不能是半透明的 rgb()。
    css = offbeat_css()
    for name, value in re.findall(r"(--shadow[\w-]*):\s*([^;]+);", css):
        assert "rgb" not in value, f"{name}: offset shadows are solid Nord colors"


def test_web_is_square():
    # Offbeat 的 Web 介面一律直角（radius 0）；裝置畫面裡的窗是模擬螢幕內容，不算介面外框。
    assert re.search(r"--radius:\s*0;", offbeat_css())


def test_served_pages_carry_the_theme(client):
    for path in ("/demo", "/dashboard"):
        body = client.get(path).text
        assert "--nord-polar0" in body and OFFBEAT_PLACEHOLDER not in body, path


def test_standalone_demo_carries_the_theme():
    html = page_document(None)
    assert "--nord-polar0" in html and OFFBEAT_PLACEHOLDER not in html
