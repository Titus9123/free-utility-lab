"""Goal 11 quality gates for Free Utility Lab asset/support-page readiness."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_ASSETS = [
    ROOT / "budgetreset" / "index.html",
    ROOT / "mealplansheet" / "index.html",
    ROOT / "movebudget" / "index.html",
    ROOT / "aistackcost" / "index.html",
]
SUPPORT_PAGES = [
    p for p in ROOT.glob("*/*/index.html")
    if p.parts[-3] in {"budgetreset", "mealplansheet", "movebudget", "aistackcost"}
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_main_asset_styles_stay_inside_head_before_body():
    for path in MAIN_ASSETS:
        html = read(path)
        head_close = html.lower().find("</head>")
        body_open = html.lower().find("<body")
        assert head_close != -1 and body_open != -1, path
        between = html[head_close:body_open]
        assert "<link" not in between.lower(), f"link tag after </head> in {path}"
        assert "<style" not in between.lower(), f"style tag after </head> in {path}"
        modern_css = html.lower().find("asset-lab-modern.css")
        if modern_css != -1:
            assert modern_css < head_close, f"modern CSS outside head in {path}"


def test_support_pages_have_minimum_organic_readiness():
    assert len(SUPPORT_PAGES) >= 60
    for path in SUPPORT_PAGES:
        html = read(path)
        lower = html.lower()
        assert "<title>" in lower, f"missing title: {path}"
        assert 'name="description"' in lower, f"missing meta description: {path}"
        assert 'rel="canonical"' in lower, f"missing canonical: {path}"
        assert "application/ld+json" in lower, f"missing schema: {path}"
        assert "no signup" in lower or "free" in lower, f"missing free/no-signup trust copy: {path}"
        cluster = path.parts[-3]
        asset_names = {"budgetreset", "mealplansheet", "movebudget", "aistackcost"}
        assert f'href="/free-utility-lab/{cluster}/"' in lower, f"missing internal link to main asset: {path}"
        assert (
            "open free tool" in lower
            or "free tool" in lower
            or "main tool" in lower
            or any(name in lower for name in asset_names)
        ), f"missing internal tool CTA: {path}"
        assert "support_page_click" in html or "free-utility-lab-measurement-bridge.js" in html, f"missing support-page tracking readiness: {path}"


def test_goal11_does_not_cutover_domain_or_enable_live_ads():
    all_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in ROOT.rglob("*.html"))
    assert "adsbygoogle" not in all_text
    assert "googlesyndication" not in all_text
    assert not (ROOT / "CNAME").exists()
    assert "https://titus9123.github.io/free-utility-lab/" in all_text
