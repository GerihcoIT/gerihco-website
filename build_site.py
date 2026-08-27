"""
build_site.py
==============

Generates the six self-contained HTML pages of the Gerihco website from a
single set of shared components defined in this script (design tokens,
CSS, navigation bar, footer, icon library).

WHY A GENERATOR SCRIPT, RATHER THAN SIX HAND-WRITTEN FILES
------------------------------------------------------------
Google Sites' "Full page embed" feature (Insert/Pages > Full page embed >
Embed code) renders each page's HTML inside its own isolated sandboxed
iframe. There is no server-side include mechanism, so each of the six
pages must ship a complete, self-contained copy of the CSS and markup
(this mirrors the approach already used for the original homepage file,
gerihco_homepage_concept_e.html). Maintaining six nearly-identical large
HTML files by hand invites drift between them -- a CSS fix applied to one
page's copy of the navigation bar and forgotten on the other five, for
example. This script keeps exactly one canonical copy of every shared
piece (the CSS, the nav bar, the footer, the icon set) and stamps out the
six output files from it. To change the navigation bar site-wide, edit it
once in this script and re-run it.

The six generated *.html files are the actual deliverables to paste into
Google Sites. This script is supporting tooling, not something Google
Sites needs to see.

USAGE
-----
    python3 build_site.py

Writes index.html, services.html, industries.html, about.html,
insights.html, and contact.html into OUTPUT_DIR.
"""

import os
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = "/mnt/user-data/outputs"

# Canonical page list. The "href" values are placeholders (see the README
# for why these need to be edited once each page has a real Google Sites
# URL) but keeping them as clean, predictable filenames makes them easy to
# find and replace later, and lets every file be previewed by simply
# opening it in a browser before it is pasted into Google Sites.
PAGE_ORDER = ["services", "industries", "about", "careers", "insights", "contact"]
HREF = {
    "home": "index.html",
    "services": "services.html",
    "industries": "industries.html",
    "about": "about.html",
    "careers": "careers.html",
    "insights": "insights.html",
    "contact": "contact.html",
}
LABEL = {
    "services": "Services",
    "industries": "Industries",
    "about": "About",
    "careers": "Careers",
    "insights": "Insights",
    "contact": "Contact",
}

# ---------------------------------------------------------------------------
# Brand asset: the finalized icon-only mark (gerihco_icon.txt), reused as an
# inline SVG favicon via a data: URI. This avoids introducing a binary
# asset / upload step, and keeps the favicon perfectly in sync with the
# approved logo file rather than a separately-exported PNG.
# ---------------------------------------------------------------------------

ICON_MARK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="38.5 9 203 203">'
    '<path d="M70,120 Q140,29 210,120" stroke="#2AA7F7" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M85,120 Q140,48.5 195,120" stroke="#858585" stroke-width="3.5" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M100,120 Q140,68 180,120" stroke="#000000" stroke-width="1.5" '
    'fill="none" stroke-linecap="round"/>'
    '<line x1="140" y1="120" x2="140" y2="175" stroke="#000000" '
    'stroke-width="4" stroke-linecap="round"/>'
    '<path d="M140,175 Q140,192 120,192" stroke="#000000" stroke-width="4" '
    'fill="none" stroke-linecap="round"/>'
    "</svg>"
)
FAVICON_HREF = "data:image/svg+xml," + quote(ICON_MARK_SVG)

# The horizontal lockup, restored to the FINALIZED spec (Helvetica/Arial
# bold, per gerihco_horizontal.txt) rather than the Inter/600 variant that
# was used in the concept_e.html nav bar. That earlier file appears to
# have substituted the page's body typeface for the wordmark by mistake;
# the approved logo source is Helvetica/Arial bold, so the canonical
# source file is what every page's nav bar now uses.
LOGO_SVG = (
    '<svg viewBox="40 9 560 203" width="150" xmlns="http://www.w3.org/2000/svg" '
    'aria-hidden="true" focusable="false">'
    '<path d="M70,120 Q140,29 210,120" stroke="#2AA7F7" stroke-width="6" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M85,120 Q140,48.5 195,120" stroke="#858585" stroke-width="3.5" '
    'fill="none" stroke-linecap="round"/>'
    '<path d="M100,120 Q140,68 180,120" stroke="#000000" stroke-width="1.5" '
    'fill="none" stroke-linecap="round"/>'
    '<line x1="140" y1="120" x2="140" y2="175" stroke="#000000" stroke-width="4" '
    'stroke-linecap="round"/>'
    '<path d="M140,175 Q140,192 120,192" stroke="#000000" stroke-width="4" '
    'fill="none" stroke-linecap="round"/>'
    '<text x="260" y="100" font-family="Helvetica, Arial, sans-serif" '
    'font-size="40" font-weight="700" letter-spacing="3" fill="#000000">GERIHCO</text>'
    '<text x="260" y="128" font-family="Helvetica, Arial, sans-serif" font-size="13" '
    'letter-spacing="2" fill="#858585">MANAGEMENT CONSULTING</text>'
    "</svg>"
)

# ---------------------------------------------------------------------------
# Icon library. All icons are stroke-based, 24x24, and use stroke="currentColor"
# so a single markup fragment can be recolored per context in CSS (the
# original file hardcoded a hex stroke color into each icon, which meant a
# palette change required editing every path). Every icon is decorative and
# paired with adjacent visible text, so each is aria-hidden.
# ---------------------------------------------------------------------------

def _icon(paths, extra=""):
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true" focusable="false"' + extra + ">" + paths + "</svg>"
    )

ICON_GOVERNMENT = _icon('<path d="M3 21h18M4 21V10l8-6 8 6v11M9 21v-6h6v6"/>')
ICON_FINANCE = _icon('<path d="M4 20V10M10 20V4M16 20v-7M20 20v-3"/>')
ICON_MANUFACTURING = _icon(
    '<path d="M14 7l3-3 3 3-3 3-3-3zM3 21l7-7M12 12l-2 2 3 3 2-2"/>'
)
# Data analytics: a simple axes-and-trend-line glyph.
ICON_DATA = _icon('<path d="M4 4v16h16"/><path d="M7 15l4-5 3 3 5-7"/>')
# AI / machine learning: three connected nodes, evoking a small network
# without referencing any specific product's mark.
ICON_AI = _icon(
    '<circle cx="6" cy="7" r="2"/><circle cx="18" cy="7" r="2"/>'
    '<circle cx="12" cy="18" r="2"/><path d="M7.6 8.4l3.4 8M16.4 8.4l-3.4 8M8 7h8"/>'
)
ICON_SECURITY = _icon('<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/>')
# Management consulting: two nested arcs, a deliberately restrained echo of
# the Gerihco mark itself -- appropriate for this one service in
# particular, since management consulting is the firm's core discipline.
ICON_CONSULTING = _icon(
    '<path d="M4 15c2-6 6-9 8-9s6 3 8 9"/><path d="M7 15c1.5-4 4-6 5-6s3.5 2 5 6"/>'
)
ICON_EMAIL = _icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 6l8 6 8-6"/>')
ICON_PHONE = _icon(
    '<path d="M5 4h4l2 5-2 1a10 10 0 005 5l1-2 5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>'
)
ICON_PIN = _icon('<path d="M12 21s7-7.5 7-12a7 7 0 10-14 0c0 4.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>')

SERVICES = [
    ("data-analytics", "Data Analytics", ICON_DATA,
     "GERIHCO helps organizations transform raw data into actionable "
     "insights that support better business decisions. We provide data "
     "engineering, business intelligence, advanced analytics, and data "
     "governance capabilities that help organizations build reliable data "
     "infrastructure, understand complex information, and use data more "
     "effectively."),
    ("ai-machine-learning", "AI & Machine Learning", ICON_AI,
     "GERIHCO applies artificial intelligence and machine learning to help "
     "organizations automate complex processes, identify patterns, and "
     "make more informed predictions. Our capabilities include predictive "
     "modeling, natural language processing, computer vision, and the "
     "deployment and governance of machine learning systems."),
    ("cybersecurity", "Cybersecurity", ICON_SECURITY,
     "GERIHCO helps organizations protect digital systems, networks, cloud "
     "environments, and sensitive information from evolving cyber threats. "
     "Our cybersecurity capabilities include endpoint protection, identity "
     "and access management, managed detection and response, and "
     "vulnerability assessment."),
    ("management-consulting", "Management Consulting", ICON_CONSULTING,
     "GERIHCO helps leaders address complex operational challenges, "
     "improve organizational performance, and develop strategies for "
     "long-term growth. Our consulting capabilities span corporate "
     "strategy, operations improvement, organizational change, and "
     "technology transformation."),
    ("government-contracting", "Government Contracting", ICON_GOVERNMENT,
     "GERIHCO provides support for organizations pursuing and managing "
     "public-sector opportunities. Our capabilities include bid and "
     "proposal development, regulatory compliance, contract "
     "administration, and support navigating government procurement "
     "requirements."),
    ("financial-analysis", "Financial Analysis", ICON_FINANCE,
     "GERIHCO helps organizations evaluate financial performance, assess "
     "opportunities, and manage economic and financial risk. Our "
     "capabilities include financial planning and analysis, corporate "
     "valuation, investment appraisal, and risk management."),
    ("manufacturing-optimization", "Manufacturing Optimization", ICON_MANUFACTURING,
     "GERIHCO helps manufacturers improve operational efficiency through "
     "data analytics, artificial intelligence, automation, and advanced "
     "management strategies. Our capabilities include predictive "
     "maintenance, process automation, quality and defect tracking, and "
     "supply chain optimization."),
]

TECH_CATEGORIES = [
    ("Cloud & Data", "Amazon Web Services \u00b7 Microsoft Azure \u00b7 Google Cloud"),
    ("Business Intelligence", "Tableau \u00b7 Microsoft Power BI"),
    ("Cybersecurity", "CrowdStrike \u00b7 Palo Alto Networks \u00b7 Microsoft Security"),
    ("Standards & Frameworks", "ISO \u00b7 CMMI \u00b7 cGMP \u00b7 Federal Acquisition Regulation"),
]

INDUSTRIES = [
    ("government", "Government", ICON_GOVERNMENT,
     "GERIHCO helps public-sector organizations address complex "
     "operational, technological, and procurement challenges through "
     "data, technology, and management expertise.",
     ("images/government-01.jpg",
      "The dome of the U.S. Capitol building in monochrome, with the "
      "American flag flying in front of it")),
    ("financial-services", "Financial Services", ICON_FINANCE,
     "GERIHCO helps financial organizations use data, technology, and "
     "analytical methods to improve decision-making, manage risk, and "
     "evaluate business opportunities.",
     None),
    ("manufacturing", "Manufacturing", ICON_MANUFACTURING,
     "GERIHCO helps manufacturers improve operational performance through "
     "analytics, artificial intelligence, automation, and process "
     "optimization.",
     None),
]

AUDIENCE = [
    "Government program managers",
    "Financial executives and program managers",
    "Data and technology program managers",
    "Private research institutions",
]

VALUES = [
    ("Innovative",
     "Placeholder \u2014 one or two sentences on how this value shows up "
     "in the way Gerihco approaches a client's problem."),
    ("Pragmatic",
     "Placeholder \u2014 one or two sentences on how this value shows up "
     "in the way Gerihco scopes and delivers engagements."),
    ("Sophisticated",
     "Placeholder \u2014 one or two sentences on how this value shows up "
     "in the caliber of analysis or staff Gerihco brings to an engagement."),
]

# ---------------------------------------------------------------------------
# Shared CSS. This is the single canonical stylesheet for every page.
# Organized in the same section order as the original homepage file, with
# new sections appended for interior-page components.
# ---------------------------------------------------------------------------

SHARED_STYLE = """
  /* Reset: Google Sites' own theme CSS can leak margin/font defaults into
     the iframe content, so basics are zeroed out here rather than relying
     on the host page to behave. */
  * { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'Inter', Arial, sans-serif;
    color: #1c1f24;
    background: #ffffff;
    line-height: 1.5;
    width: 100%;
  }

  a { text-decoration: none; color: inherit; }
  main { display: block; }
  img, svg { max-width: 100%; }

  /* ---------- Design tokens ----------
     Centralizing the palette here means a future rebrand or dark-mode
     variant only requires editing this block. */
  :root {
    --ink: #0a0c0f;          /* near-black used for dark sections */
    --ink-card: #16191d;     /* slightly lighter card surface on dark bg */
    --paper: #ffffff;
    --paper-muted: #f4f5f6;  /* light plate behind the logo on dark sections */
    --gray-text: #5f5e5a;
    --gray-text-dark: #9aa0a8; /* muted text on dark backgrounds */
    --blue: #2aa7f7;         /* brand light blue, from the logo mark */
    --blue-deep: #185fa5;    /* deeper blue for text/icons on light bg */
    --blue-pale: #85b7eb;    /* pale blue for text/icons on dark bg */
    --border: #e3e4e6;
  }

  .wrap { max-width: 1100px; margin: 0 auto; padding: 0 32px; }

  /* ---------- Accessibility: skip link ----------
     Lets keyboard and screen-reader users jump past the repeated nav on
     every page straight to the page's main content. */
  .skip-link {
    position: absolute;
    left: -9999px;
    top: 0;
    background: var(--blue);
    color: #042c53;
    padding: 10px 16px;
    z-index: 100;
    font-size: 14px;
    font-weight: 600;
    border-radius: 0 0 4px 0;
  }
  .skip-link:focus { left: 0; }

  /* ---------- Focus visibility ----------
     Visible focus outlines for keyboard navigation, independent of
     whatever the host Sites page does. */
  a:focus-visible, button:focus-visible, input:focus-visible,
  textarea:focus-visible, label:focus-visible, [tabindex]:focus-visible {
    outline: 2px solid var(--blue-deep);
    outline-offset: 2px;
  }

  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    * { transition: none !important; animation: none !important; }
  }

  /* ---------- Navigation ----------
     Light plate background so the logo's black strokes stay legible,
     independent of whatever color the section below it uses. */
  header.nav {
    background: var(--paper-muted);
    border-bottom: 1px solid var(--border);
  }
  .nav-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }
  .logo-link { display: inline-flex; order: 0; }
  .nav-links {
    display: flex;
    align-items: center;
    gap: 28px;
    font-size: 14px;
    color: #33363a;
    order: 2;
  }
  .nav-links a:hover { color: var(--blue-deep); }
  .nav-links a[aria-current="page"] { color: var(--blue-deep); font-weight: 600; }
  .nav-links a.nav-cta { color: var(--blue-deep); font-weight: 600; }

  /* Mobile navigation toggle, built with a hidden checkbox and a <label>
     styled as a button (the "checkbox hack") rather than JavaScript.
     Google's iframe-based embed sandboxes (used across Sites and Apps
     Script) are documented to permit allow-scripts, but the exact sandbox
     flags Sites applies to a "Full page embed" are not published. A
     CSS-only toggle removes that dependency entirely, so the mobile menu
     is guaranteed to work regardless of script permissions. */
  .nav-toggle-input { position: absolute; opacity: 0; pointer-events: none; }
  .nav-toggle-label {
    display: none;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    width: 40px;
    height: 40px;
    cursor: pointer;
    order: 1;
    border-radius: 4px;
  }
  .nav-toggle-label span {
    display: block;
    width: 22px;
    height: 2px;
    background: #1c1f24;
    border-radius: 1px;
  }
  .nav-toggle-input:focus-visible ~ .nav-toggle-label {
    outline: 2px solid var(--blue-deep);
    outline-offset: 2px;
  }

  /* ---------- Hero (home page only) ----------
     Dark, full-bleed section; headline is left-justified. The photo is
     layered under a dark gradient (matching --ink) so the white headline
     stays legible regardless of the image's own tonal range; --ink alone
     remains the background-color fallback if the image fails to load.
     Purely decorative/atmospheric, so it is a CSS background-image rather
     than an <img> -- it carries no information the text doesn't already
     provide, so no alt text is needed or appropriate here. */
  section.hero {
    background-color: var(--ink);
    background-image:
      linear-gradient(180deg, rgba(10,12,15,0.45) 0%, rgba(10,12,15,0.92) 100%),
      url('images/hero-01-alt.jpg');
    background-size: cover;
    background-position: center 35%;
    background-repeat: no-repeat;
    color: #ffffff;
    padding: 72px 0 64px;
  }
  .hero h1 {
    font-size: 40px;
    font-weight: 500;
    line-height: 1.3;
    max-width: 640px;
    margin-bottom: 20px;
  }
  .hero p.sub {
    font-size: 17px;
    color: var(--gray-text-dark);
    max-width: 520px;
    margin-bottom: 28px;
  }
  .btn-row { display: flex; gap: 14px; flex-wrap: wrap; }
  .btn-primary, .btn-secondary {
    display: inline-block;
    font-size: 14px;
    font-weight: 500;
    padding: 14px 26px;
    border-radius: 3px;
    border: none;
    font-family: inherit;
    cursor: pointer;
  }
  .btn-primary { background: var(--blue); color: #042c53; }
  .btn-secondary { border: 1px solid #4a4d52; color: #ffffff; background: transparent; }
  .btn-primary:hover { background: #4bb6fa; }
  .btn-secondary:hover { background: #16191d; }

  /* ---------- Page header (interior pages) ----------
     A shorter version of the hero treatment, reused on every non-home
     page so the whole site reads as one consistent system rather than a
     bespoke homepage bolted onto generic interior pages. */
  section.page-header {
    background: var(--ink);
    color: #ffffff;
    padding: 48px 0 40px;
  }
  section.page-header h1 { font-size: 32px; font-weight: 500; margin-bottom: 12px; }
  section.page-header p { font-size: 16px; color: var(--gray-text-dark); max-width: 620px; }

  /* ---------- Who we serve / industry cards ---------- */
  section.serve { background: var(--ink); padding: 0 0 64px; }
  .serve-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  .serve-card {
    background: var(--ink-card);
    border-radius: 10px;
    padding: 28px 20px;
    text-align: center;
  }
  .serve-card svg { width: 28px; height: 28px; color: var(--blue-pale); }
  .serve-card p { font-size: 14px; color: #e6e8eb; margin-top: 12px; }
  a.serve-card { display: block; }
  a.serve-card:hover { background: #1f2329; }

  /* ---------- Statistics ---------- */
  section.stats { background: var(--ink); padding: 0 0 56px; }
  .stats-grid {
    display: flex;
    justify-content: space-between;
    text-align: center;
    flex-wrap: wrap;
    gap: 24px;
  }
  .stats-grid div { flex: 1; min-width: 140px; }
  .stat-num { font-size: 34px; font-weight: 500; color: var(--blue-pale); }
  .stat-label { font-size: 13px; color: var(--gray-text-dark); margin-top: 4px; }

  /* ---------- Placeholder content marker ----------
     Applied to every piece of copy standing in for real client-supplied
     content, so placeholders are visually unmistakable rather than
     reading as finished, verified copy. */
  .placeholder { color: var(--gray-text); font-style: italic; }
  .placeholder-box {
    border: 1px dashed var(--border);
    border-radius: 6px;
    padding: 18px 20px;
    color: var(--gray-text);
    font-style: italic;
    font-size: 14px;
  }

  /* ---------- Services list (home page teaser) ---------- */
  section.services { padding: 64px 0; background: var(--paper); }
  section.services h2 { font-size: 22px; font-weight: 500; margin-bottom: 8px; }
  section.services > .wrap > p { color: var(--gray-text); margin-bottom: 24px; max-width: 560px; }
  .service-list {
    columns: 2;
    column-gap: 48px;
    list-style: none;
    font-size: 15px;
  }
  .service-list li { padding: 12px 0; border-bottom: 1px solid var(--border); break-inside: avoid; }
  .service-list a:hover { color: var(--blue-deep); }
  .view-all { display: inline-block; margin-top: 24px; font-size: 14px; font-weight: 600; color: var(--blue-deep); }

  /* ---------- Service detail cards (services.html) ---------- */
  section.service-detail { padding: 64px 0; background: var(--paper); }
  .service-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 32px 40px;
    margin-top: 32px;
  }
  .service-card { border-top: 2px solid var(--blue); padding-top: 16px; }
  .service-card svg { width: 26px; height: 26px; color: var(--blue-deep); margin-bottom: 10px; }
  .service-card h2 { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
  .service-card p { font-size: 14px; }

  /* ---------- Technology section (bottom of services.html) ---------- */
  section.technology { padding: 56px 0 64px; background: var(--paper-muted); }
  section.technology h2 { font-size: 22px; font-weight: 500; margin-bottom: 8px; }
  section.technology > .wrap > p { color: var(--gray-text); max-width: 620px; margin-bottom: 24px; }
  .tech-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
  .tech-card { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
  .tech-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 8px; color: var(--blue-deep); }
  .tech-card p { font-size: 14px; color: var(--gray-text); }

  /* ---------- Careers page ---------- */
  section.careers-openings { padding: 64px 0 40px; }
  section.careers-openings h2 { font-size: 20px; font-weight: 600; margin-bottom: 12px; }
  section.careers-apply { padding: 0 0 64px; }
  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: var(--paper-muted);
    color: var(--gray-text);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 3px 10px;
    margin-bottom: 10px;
  }
  .job-card { border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-top: 16px; }
  .job-card h3 { font-size: 16px; font-weight: 600; margin: 4px 0 6px; }
  .job-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
  .job-tag {
    font-size: 12px;
    color: var(--gray-text);
    background: var(--paper-muted);
    border-radius: 4px;
    padding: 2px 8px;
  }
  .job-card .apply-link { display: inline-block; margin-top: 10px; font-size: 14px; font-weight: 600; color: var(--blue-deep); }
  .contact-form input[type="file"] { border: 1px dashed var(--border); background: var(--paper-muted); padding: 10px 12px; }

  /* ---------- Industry rows (industries.html) ----------
     Each row leads with a media slot: a real photo where one has been
     supplied and passed the brand-safety check, or a placeholder box of
     the same footprint where none exists yet, so the page reads as one
     consistent grid rather than looking unfinished in just one spot. */
  section.industry-detail { padding: 64px 0; }
  .industry-row {
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 24px;
    padding: 32px 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
  }
  .industry-row:last-of-type { border-bottom: none; }
  .industry-media {
    width: 100%;
    aspect-ratio: 4 / 3;
    border-radius: 8px;
    overflow: hidden;
    background: var(--paper-muted);
  }
  .industry-media img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .industry-media.placeholder-box {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    aspect-ratio: 4 / 3;
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
  }
  .industry-row h2 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  .industry-row .industry-icon { color: var(--blue-deep); display: inline-flex; }
  .industry-row .industry-icon svg { width: 22px; height: 22px; }
  .industry-row p { font-size: 15px; }

  section.audience { padding: 0 0 64px; background: var(--paper); }
  section.audience h2 { font-size: 20px; font-weight: 600; margin-bottom: 16px; }
  .audience-list { list-style: none; }
  .audience-list li { padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 15px; }

  /* ---------- About page ---------- */
  section.about-intro { padding: 64px 0 8px; }
  section.about-intro p { font-size: 17px; color: var(--gray-text); max-width: 640px; margin-bottom: 16px; }
  section.about-values { padding: 40px 0 64px; }
  .values-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 16px; }
  .value-card { background: var(--paper-muted); border: 1px solid var(--border); border-radius: 10px; padding: 24px; }
  .value-card h3 { font-size: 16px; font-weight: 600; margin-bottom: 8px; color: var(--blue-deep); }
  .value-card p { font-size: 14px; }
  section.about-leadership { padding: 0 0 64px; }
  section.about-leadership h2 { font-size: 20px; font-weight: 600; margin-bottom: 16px; }

  /* ---------- Insights page ---------- */
  section.insights-list { padding: 64px 0; }
  .insights-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 24px; }
  .insight-card { border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
  .insight-card .insight-date { font-size: 12px; color: var(--gray-text); text-transform: uppercase; letter-spacing: 1px; }
  .insight-card h2 { font-size: 17px; font-weight: 600; margin: 8px 0; }
  .insight-card p.placeholder { font-size: 14px; }

  /* ---------- Contact page ---------- */
  section.contact-main { padding: 64px 0; }
  .contact-layout { display: grid; grid-template-columns: 1.3fr 1fr; gap: 48px; align-items: start; }
  .contact-form label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 6px; color: #33363a; }
  .contact-form .field { margin-bottom: 18px; }
  .contact-form input, .contact-form textarea {
    width: 100%;
    padding: 11px 12px;
    border: 1px solid var(--border);
    border-radius: 4px;
    font: inherit;
    color: inherit;
    background: #fff;
  }
  .contact-form textarea { resize: vertical; min-height: 120px; }
  .contact-info { background: var(--paper-muted); border-radius: 10px; padding: 28px; }
  .contact-info h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
  .contact-line { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 16px; font-size: 14px; }
  .contact-line svg { width: 18px; height: 18px; color: var(--blue-deep); flex-shrink: 0; margin-top: 2px; }

  /* ---------- Final call to action ---------- */
  section.final-cta { background: var(--paper-muted); padding: 56px 0; text-align: left; }
  section.final-cta h2 { font-size: 26px; font-weight: 500; max-width: 520px; margin-bottom: 20px; }

  /* ---------- Footer ---------- */
  footer { padding: 28px 0 48px; font-size: 13px; color: var(--gray-text); }
  .footer-links { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 14px; }
  .footer-links a:hover { color: var(--blue-deep); }

  /* ---------- Responsive breakpoints ----------
     Two breakpoints are used consistently site-wide:
       1024px - tablet: three-column grids narrow to two columns.
       720px  - mobile: nav collapses to the toggled drawer, all
                multi-column grids and layouts drop to one column, and
                the hero/page-header type scale reduces. */
  @media (max-width: 1024px) {
    .serve-grid { grid-template-columns: repeat(2, 1fr); }
    .values-grid { grid-template-columns: repeat(2, 1fr); }
    .insights-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (max-width: 720px) {
    .nav-toggle-label { display: flex; }
    .nav-links {
      display: none;
      order: 3;
      flex-basis: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 2px;
      padding-top: 12px;
    }
    .nav-toggle-input:checked ~ .nav-links { display: flex; }
    .nav-links a { display: block; width: 100%; padding: 12px 4px; border-top: 1px solid var(--border); }

    .hero h1 { font-size: 30px; }
    section.page-header h1 { font-size: 26px; }

    .serve-grid { grid-template-columns: 1fr; }
    .service-list { columns: 1; }
    .service-grid { grid-template-columns: 1fr; }
    .tech-grid { grid-template-columns: 1fr; }
    .values-grid { grid-template-columns: 1fr; }
    .insights-grid { grid-template-columns: 1fr; }
    .industry-row { grid-template-columns: 1fr; }
    .contact-layout { grid-template-columns: 1fr; }
  }
"""

# ---------------------------------------------------------------------------
# Shared markup fragments
# ---------------------------------------------------------------------------

HEAD_LINKS = (
    '<link rel="icon" type="image/svg+xml" href="__FAVICON__">\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600'
    '&display=swap" rel="stylesheet">'
).replace("__FAVICON__", FAVICON_HREF)


def build_nav(active):
    """Return the <header class="nav"> block with the current page marked
    via aria-current, and every internal link set to target="_top" so a
    click navigates the whole browser tab rather than trying to load the
    destination page inside the small embedded iframe (Google's iframe
    sandboxing, used consistently across its embed products, blocks plain
    top-level navigation from inside the frame unless the link target is
    _top or _blank)."""
    links = []
    for key in PAGE_ORDER:
        attrs = ' target="_top"'
        if key == active:
            attrs += ' aria-current="page"'
        if key == "contact":
            attrs += ' class="nav-cta"'
        links.append('<a href="{0}"{1}>{2}</a>'.format(HREF[key], attrs, LABEL[key]))
    nav_links_html = "\n      ".join(links)

    logo_current = ' aria-current="page"' if active == "home" else ""

    return (
        '<a class="skip-link" href="#main">Skip to main content</a>\n'
        '<header class="nav">\n'
        '  <div class="nav-inner">\n'
        '    <a class="logo-link" href="{home}" target="_top"{logo_current} '
        'aria-label="Gerihco \u2014 home">{logo}</a>\n'
        '    <input type="checkbox" id="nav-toggle" class="nav-toggle-input">\n'
        '    <label for="nav-toggle" class="nav-toggle-label" '
        'aria-label="Toggle navigation menu"><span></span><span></span><span></span></label>\n'
        '    <nav class="nav-links" aria-label="Primary">\n'
        "      {nav_links}\n"
        "    </nav>\n"
        "  </div>\n"
        "</header>"
    ).format(home=HREF["home"], logo_current=logo_current, logo=LOGO_SVG, nav_links=nav_links_html)


FOOTER = (
    "<footer>\n"
    '  <div class="wrap">\n'
    '    <nav aria-label="Footer" class="footer-links">\n'
    '      <a href="{home}" target="_top">Home</a>\n'
    '      <a href="{services}" target="_top">Services</a>\n'
    '      <a href="{industries}" target="_top">Industries</a>\n'
    '      <a href="{about}" target="_top">About</a>\n'
    '      <a href="{careers}" target="_top">Careers</a>\n'
    '      <a href="{insights}" target="_top">Insights</a>\n'
    '      <a href="{contact}" target="_top">Contact</a>\n'
    "    </nav>\n"
    "    <p>\u00a9 Gerihco. Management consulting for institutions that cannot "
    "afford to fail.</p>\n"
    "  </div>\n"
    "</footer>"
).format(**HREF)

PAGE_SHELL = """<!--
  GERIHCO website \u2014 __PAGE_LABEL__ page.
  Generated by build_site.py; edit the shared components there (not this
  file directly) if the change should apply to every page.

  HOW TO PUT THIS ON GOOGLE SITES:
  1. In the Sites editor, use Pages > Add > Full page embed, name the page,
     then choose Embed code and paste this file's contents in full.
  2. "Full page embed" is used (rather than a boxed Insert > Embed) so this
     page fills the browser tab like a normal page, instead of sitting in a
     fixed-height box inside a Sites layout.
  3. This file is self-contained (fonts load via the Google Fonts link
     below; no other external files are required) so it renders the same
     regardless of what else exists on the Sites account.
  4. The navigation and footer links below point to "index.html",
     "services.html", etc. as placeholders. Once each page is published in
     Google Sites, replace these hrefs with the real published URLs -- see
     README.md for the full list to update.
  5. Every internal link uses target="_top". Google's iframe-based embed
     sandboxing blocks a plain link from navigating the parent tab; _top
     tells the browser to navigate the whole tab instead of trying (and
     failing) to load the destination inside this small iframe.
-->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESCRIPTION__">
__HEAD_LINKS__

<style>
__STYLE__
</style>

__NAV__

__CONTENT__

__FOOTER__
"""


def render_page(key, title, description, content_html):
    label = "Home" if key == "home" else LABEL[key]
    html = PAGE_SHELL
    html = html.replace("__PAGE_LABEL__", label)
    html = html.replace("__TITLE__", title)
    html = html.replace("__DESCRIPTION__", description)
    html = html.replace("__HEAD_LINKS__", HEAD_LINKS)
    html = html.replace("__STYLE__", SHARED_STYLE)
    html = html.replace("__NAV__", build_nav(key))
    html = html.replace("__CONTENT__", content_html)
    html = html.replace("__FOOTER__", FOOTER)
    return html


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------

def service_teaser_list():
    items = "\n      ".join(
        '<li><a href="{href}#{anchor}" target="_top">{label}</a></li>'.format(
            href=HREF["services"], anchor=anchor, label=label
        )
        for anchor, label, _icon_html, _desc in SERVICES
    )
    return (
        '<section class="services" id="services">\n'
        '  <div class="wrap">\n'
        "    <h2>What we do</h2>\n"
        "    <p>An overview of Gerihco's service lines; see the "
        '<a href="{services}" target="_top">Services</a> page for more on each.</p>\n'
        '    <ul class="service-list">\n'
        "      {items}\n"
        "    </ul>\n"
        '    <a class="view-all" href="{services}" target="_top">View all capabilities \u2192</a>\n'
        "  </div>\n"
        "</section>"
    ).format(services=HREF["services"], items=items)


def home_content():
    serve_cards = "\n      ".join(
        '<a class="serve-card" href="{industries}#{anchor}" target="_top">\n'
        "        {icon}\n"
        "        <p>{label}</p>\n"
        "      </a>".format(industries=HREF["industries"], anchor=anchor, icon=icon, label=label)
        for anchor, label, icon, _desc, _image in INDUSTRIES
    )

    return (
        '<main id="main">\n'
        '<section class="hero">\n'
        '  <div class="wrap">\n'
        "    <h1>We turn institutional complexity into measurable results</h1>\n"
        '    <p class="sub">Data, technology, and strategy for the government, '
        "financial, and manufacturing institutions that cannot afford to fail.</p>\n"
        '    <div class="btn-row">\n'
        '      <a class="btn-primary" href="{contact}" target="_top">Start a conversation</a>\n'
        '      <a class="btn-secondary" href="{services}" target="_top">Our capabilities</a>\n'
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="serve" id="industries" aria-label="Industries we serve">\n'
        '  <div class="wrap">\n'
        '    <div class="serve-grid">\n'
        "      {serve_cards}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="stats" aria-label="Proof points">\n'
        '  <div class="wrap">\n'
        '    <div class="stats-grid">\n'
        '      <div><div class="stat-num placeholder">[ ]</div>'
        '<div class="stat-label placeholder">[Placeholder \u2014 e.g. programs delivered]</div></div>\n'
        '      <div><div class="stat-num placeholder">[ ]</div>'
        '<div class="stat-label placeholder">[Placeholder \u2014 e.g. cost avoidance identified]</div></div>\n'
        '      <div><div class="stat-num placeholder">[ ]</div>'
        '<div class="stat-label placeholder">[Placeholder \u2014 e.g. years serving institutional clients]</div></div>\n'
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        "{service_teaser}\n"
        '<section class="final-cta" id="contact">\n'
        '  <div class="wrap">\n'
        "    <h2>Ready to talk through a complex problem?</h2>\n"
        '    <a class="btn-primary" style="background:#042C53;color:#ffffff" '
        'href="{contact}" target="_top">Contact Gerihco</a>\n'
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(
        contact=HREF["contact"],
        services=HREF["services"],
        serve_cards=serve_cards,
        service_teaser=service_teaser_list(),
    )


def services_content():
    cards = "\n      ".join(
        '<article class="service-card" id="{anchor}">\n'
        "        {icon}\n"
        "        <h2>{label}</h2>\n"
        "        <p>{desc}</p>\n"
        "      </article>".format(anchor=anchor, icon=icon, label=label, desc=desc)
        for anchor, label, icon, desc in SERVICES
    )
    tech_cards = "\n      ".join(
        '<div class="tech-card">\n'
        "        <h3>{title}</h3>\n"
        "        <p>{items}</p>\n"
        "      </div>".format(title=title, items=items)
        for title, items in TECH_CATEGORIES
    )
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Services</h1>\n"
        "    <p>GERIHCO helps organizations solve complex challenges "
        "through data, technology, strategy, and operational expertise. "
        "Our services combine technical capabilities with practical "
        "business and organizational insight to help clients make better "
        "decisions, manage risk, and improve performance.</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="service-detail">\n'
        '  <div class="wrap">\n'
        '    <div class="service-grid">\n'
        "      {cards}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="technology" id="technology">\n'
        '  <div class="wrap">\n'
        "    <h2>Technology</h2>\n"
        "    <p>GERIHCO works across modern technology platforms and tools "
        "to develop solutions that align with each organization's existing "
        "environment and requirements.</p>\n"
        '    <div class="tech-grid">\n'
        "      {tech_cards}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="final-cta" id="contact-cta">\n'
        '  <div class="wrap">\n'
        "    <h2>Ready to talk through a complex problem?</h2>\n"
        '    <a class="btn-primary" style="background:#042C53;color:#ffffff" '
        'href="{contact}" target="_top">Contact Gerihco</a>\n'
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(cards=cards, tech_cards=tech_cards, contact=HREF["contact"])


def industries_content():
    def _media(anchor, label, image):
        if image is not None:
            src, alt = image
            return '<div class="industry-media"><img src="{src}" alt="{alt}" loading="lazy"></div>'.format(
                src=src, alt=alt
            )
        return (
            '<div class="industry-media placeholder-box">[Placeholder \u2014 '
            "{label} sector photograph pending; see manifest.csv for "
            "licensed candidates.]</div>"
        ).format(label=label)

    rows = "\n      ".join(
        '<div class="industry-row" id="{anchor}">\n'
        "        {media}\n"
        "        <div>\n"
        '          <h2><span class="industry-icon">{icon}</span>{label}</h2>\n'
        "          <p>{desc}</p>\n"
        "        </div>\n"
        "      </div>".format(
            anchor=anchor, media=_media(anchor, label, image), icon=icon, label=label, desc=desc
        )
        for anchor, label, icon, desc, image in INDUSTRIES
    )
    audience_items = "\n      ".join("<li>{0}</li>".format(a) for a in AUDIENCE)
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Industries</h1>\n"
        "    <p>GERIHCO works with organizations facing complex technical, "
        "operational, and strategic challenges across highly regulated and "
        "data-intensive industries.</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="industry-detail">\n'
        '  <div class="wrap">\n'
        "      {rows}\n"
        "  </div>\n"
        "</section>\n"
        '<section class="audience">\n'
        '  <div class="wrap">\n'
        "    <h2>Who we work with</h2>\n"
        '    <ul class="audience-list">\n'
        "      {audience_items}\n"
        "    </ul>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="final-cta" id="contact-cta">\n'
        '  <div class="wrap">\n'
        "    <h2>Ready to talk through a complex problem?</h2>\n"
        '    <a class="btn-primary" style="background:#042C53;color:#ffffff" '
        'href="{contact}" target="_top">Contact Gerihco</a>\n'
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(rows=rows, audience_items=audience_items, contact=HREF["contact"])


def about_content():
    values_html = "\n      ".join(
        '<div class="value-card">\n'
        "        <h3>{title}</h3>\n"
        '        <p class="placeholder">[{desc}]</p>\n'
        "      </div>".format(title=title, desc=desc)
        for title, desc in VALUES
    )
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>About Gerihco</h1>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="about-intro">\n'
        '  <div class="wrap">\n'
        "    <p>Gerihco is a management consulting firm offering long-term, "
        "sustainable solutions to modern problems.</p>\n"
        "    <p>Gerihco operates at a national scope, serving institutional "
        "clients across the country.</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="about-values">\n'
        '  <div class="wrap">\n'
        "    <h2>Our approach</h2>\n"
        '    <div class="values-grid">\n'
        "      {values}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="about-leadership">\n'
        '  <div class="wrap">\n'
        "    <h2>Leadership</h2>\n"
        '    <p class="placeholder-box">[Placeholder \u2014 leadership team '
        "profiles to be added.]</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="final-cta" id="contact-cta">\n'
        '  <div class="wrap">\n'
        "    <h2>Ready to talk through a complex problem?</h2>\n"
        '    <a class="btn-primary" style="background:#042C53;color:#ffffff" '
        'href="{contact}" target="_top">Contact Gerihco</a>\n'
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(values=values_html, contact=HREF["contact"])


def insights_content():
    card = (
        '<article class="insight-card">\n'
        '        <div class="insight-date placeholder">[Month Year]</div>\n'
        "        <h2>[Placeholder insight title]</h2>\n"
        '        <p class="placeholder">[Placeholder one-line summary of this piece.]</p>\n'
        "      </article>"
    )
    cards = "\n      ".join([card, card, card])
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Insights</h1>\n"
        '    <p class="placeholder">[Placeholder \u2014 introductory framing '
        "for Gerihco's thought leadership content.]</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="insights-list">\n'
        '  <div class="wrap">\n'
        '    <div class="insights-grid">\n'
        "      {cards}\n"
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(cards=cards)


def contact_content():
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Contact Gerihco</h1>\n"
        "    <p>Ready to talk through a complex problem?</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="contact-main">\n'
        '  <div class="wrap contact-layout">\n'
        '    <form class="contact-form" aria-label="Contact form">\n'
        '      <div class="field">\n'
        '        <label for="name">Name</label>\n'
        '        <input type="text" id="name" name="name" autocomplete="name" required>\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="organization">Organization</label>\n'
        '        <input type="text" id="organization" name="organization" autocomplete="organization">\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="email">Email</label>\n'
        '        <input type="email" id="email" name="email" autocomplete="email" required>\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="message">Message</label>\n'
        '        <textarea id="message" name="message" required></textarea>\n'
        "      </div>\n"
        '      <p class="placeholder-box" style="margin-bottom:18px;">[Placeholder \u2014 '
        "this form is not yet connected to a submission service. Connect it "
        "to a form backend (for example Formspree or a Google Form) before "
        "publishing, or replace this section with Google Sites' built-in "
        "Contact Us element.]</p>\n"
        '      <button type="submit" class="btn-primary" '
        'style="background:#042C53;color:#ffffff">Send message</button>\n'
        "    </form>\n"
        '    <aside class="contact-info">\n'
        "      <h2>Other ways to reach us</h2>\n"
        '      <div class="contact-line">{icon_email}<span class="placeholder">'
        "[Placeholder \u2014 contact email address]</span></div>\n"
        '      <div class="contact-line">{icon_phone}<span class="placeholder">'
        "[Placeholder \u2014 phone number]</span></div>\n"
        '      <div class="contact-line">{icon_pin}<span class="placeholder">'
        "[Placeholder \u2014 mailing address]</span></div>\n"
        "    </aside>\n"
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(icon_email=ICON_EMAIL, icon_phone=ICON_PHONE, icon_pin=ICON_PIN)


def careers_content():
    """Careers page.

    Two deliberate content decisions here, both worth flagging to
    whoever reviews this before publishing:

    1. No fabricated job listings. Since no real openings were supplied,
       the "Open positions" section states plainly that none are
       currently listed, rather than inventing plausible-looking roles --
       a fake job posting is a materially worse placeholder than most,
       since a real applicant could act on it. A single clearly-labeled
       example card is included underneath purely as a formatting
       reference for whoever adds the first real posting.
    2. The resume upload field is a genuine <input type="file">, but a
       static site (Google Sites embed or GitHub Pages alike) has no
       server to receive that file. This mirrors the contact form's
       "no backend yet" situation, and is called out the same way, with
       an additional plain-email fallback that works today without any
       extra infrastructure.
    """
    return (
        '<main id="main">\n'
        '<section class="page-header">\n'
        '  <div class="wrap">\n'
        "    <h1>Careers</h1>\n"
        '    <p class="placeholder">[Placeholder \u2014 a short introduction '
        "to why to join Gerihco: culture, growth opportunities, or mission "
        "framing to be supplied by the client.]</p>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="careers-openings">\n'
        '  <div class="wrap">\n'
        "    <h2>Open positions</h2>\n"
        "    <p>There are no open positions listed at this time. Check "
        "back soon, or submit your resume below for future consideration."
        "</p>\n"
        "    <!-- Example only: remove this card once real postings exist, "
        "or duplicate its structure per real opening. -->\n"
        '    <div class="job-card">\n'
        '      <span class="badge">Example format</span>\n'
        "      <h3>[Placeholder job title]</h3>\n"
        '      <div class="job-tags">\n'
        '        <span class="job-tag">[Placeholder location]</span>\n'
        '        <span class="job-tag">[Placeholder employment type]</span>\n'
        "      </div>\n"
        '      <p class="placeholder">[Placeholder \u2014 one or two '
        "sentence job summary.]</p>\n"
        '      <a class="apply-link" href="#apply">Apply for this position \u2192</a>\n'
        "    </div>\n"
        "  </div>\n"
        "</section>\n"
        '<section class="careers-apply" id="apply">\n'
        '  <div class="wrap contact-layout">\n'
        '    <form class="contact-form" aria-label="Job application form">\n'
        '      <div class="field">\n'
        '        <label for="applicant-name">Name</label>\n'
        '        <input type="text" id="applicant-name" name="name" autocomplete="name" required>\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="applicant-email">Email</label>\n'
        '        <input type="email" id="applicant-email" name="email" autocomplete="email" required>\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="applicant-position">Position of interest</label>\n'
        '        <input type="text" id="applicant-position" name="position">\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="applicant-resume">Resume (PDF or Word document)</label>\n'
        '        <input type="file" id="applicant-resume" name="resume" '
        'accept=".pdf,.doc,.docx">\n'
        "      </div>\n"
        '      <div class="field">\n'
        '        <label for="applicant-message">Message (optional)</label>\n'
        '        <textarea id="applicant-message" name="message"></textarea>\n'
        "      </div>\n"
        '      <p class="placeholder-box" style="margin-bottom:18px;">[Placeholder '
        "\u2014 this form, including the resume upload field, is not yet "
        "connected to a submission backend. A static site cannot receive "
        "or store an uploaded file on its own; connect this to a service "
        "built for job applications (an applicant tracking system, or a "
        "form backend that explicitly supports file attachments) before "
        "publishing.]</p>\n"
        '      <button type="submit" class="btn-primary" '
        'style="background:#042C53;color:#ffffff">Submit application</button>\n'
        "    </form>\n"
        '    <aside class="contact-info">\n'
        "      <h2>Prefer email?</h2>\n"
        '      <div class="contact-line">{icon_email}<span class="placeholder">'
        "[Placeholder \u2014 careers email address] \u2014 attach your resume "
        "directly.</span></div>\n"
        "    </aside>\n"
        "  </div>\n"
        "</section>\n"
        "</main>"
    ).format(icon_email=ICON_EMAIL)


# ---------------------------------------------------------------------------
# Page registry: (key, <title>, meta description, content function)
# Titles and descriptions are grounded in the provided Company Identity,
# Business Services, and Target audience documents -- no service claims,
# statistics, or credentials are introduced here.
# ---------------------------------------------------------------------------

PAGES = [
    ("home", "Gerihco | Management Consulting",
     "Gerihco is a management consulting firm delivering data, technology, "
     "and strategy services to government, financial services, and "
     "manufacturing institutions.",
     home_content),
    ("services", "Services | Gerihco Management Consulting",
     "An overview of Gerihco's management consulting services, including "
     "data analytics, AI and machine learning, cybersecurity, and more.",
     services_content),
    ("industries", "Industries We Serve | Gerihco",
     "Gerihco serves government, financial services, and manufacturing "
     "institutions with long-term, sustainable consulting solutions.",
     industries_content),
    ("about", "About Us | Gerihco Management Consulting",
     "Gerihco is a national management consulting firm offering long-term, "
     "sustainable solutions to complex institutional problems.",
     about_content),
    ("careers", "Careers | Gerihco Management Consulting",
     "Learn about career opportunities at Gerihco and how to submit your "
     "resume for consideration.",
     careers_content),
    ("insights", "Insights | Gerihco",
     "Perspectives from Gerihco on the challenges facing government, "
     "financial services, and manufacturing institutions.",
     insights_content),
    ("contact", "Contact | Gerihco Management Consulting",
     "Get in touch with Gerihco to discuss a management consulting "
     "engagement for your organization.",
     contact_content),
]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for key, title, description, content_fn in PAGES:
        html = render_page(key, title, description, content_fn())
        out_path = os.path.join(OUTPUT_DIR, HREF[key])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", out_path, "({} bytes)".format(len(html)))


if __name__ == "__main__":
    main()
