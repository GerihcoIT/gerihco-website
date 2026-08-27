# Gerihco website — deployment notes

This package contains a six-page site expanded from the original
`gerihco_homepage_concept_e.html`, built for deployment to Google Sites via
the **Full page embed** feature. Read this in full before publishing —
two of the steps below (link targets, SEO settings) are things Google
Sites will not do for you automatically.

## Files

| File               | Page         |
|--------------------|--------------|
| `index.html`       | Home         |
| `services.html`    | Services     |
| `industries.html`  | Industries   |
| `about.html`       | About        |
| `careers.html`     | Careers      |
| `insights.html`    | Insights     |
| `contact.html`     | Contact      |
| `images/`          | Photography used by the pages above |
| `build_site.py`    | Generator script that produced the six files above (see "Maintaining this site" below) |

Each `.html` file is a complete, self-contained document (fonts, CSS, and
markup all inline) and can be opened directly in a browser to preview it
before it goes anywhere near Google Sites.

## Publishing each page

For **each** of the six pages:

1. In the Sites editor: **Pages → Add → Full page embed**.
2. Name the page (this determines its position in the Sites left-hand
   navigation, if you choose to show one).
3. Choose **Embed code**, paste the entire contents of the corresponding
   `.html` file, click **Next**, then **Insert**.
4. Publish.

"Full page embed" is used rather than a boxed `Insert → Embed`, so each
page fills the browser tab the way a normal web page would, rather than
sitting inside a fixed-height box within a Sites layout.

## Required step: fix the internal links

Every internal link in these files (nav bar, footer, buttons, the "who we
serve" cards, the services list) points to a placeholder filename —
`index.html`, `services.html`, `industries.html`, `about.html`,
`insights.html`, `contact.html`. These are **not** real Google Sites URLs;
Sites assigns its own path to each page once it is created and published
(Sites does not use `.html` extensions).

Once all six pages are published, note each one's actual published URL
and do a find-and-replace across all six files for each placeholder
filename, then re-paste the updated embed code into each page. If you're
comfortable at a terminal, this is a one-line fix per file, for example:

```bash
# Repeat for each of the six placeholder filenames, using the real
# published URL Google Sites assigned to each page.
sed -i 's|href="services.html|href="https://sites.google.com/.../services|g' *.html
```

Every internal link also carries `target="_top"`. This is intentional and
should stay: Google's iframe-based embed sandboxing (used consistently
across its embed products) blocks a plain link from navigating the parent
browser tab from inside the embedded frame, so without `target="_top"`
clicking a nav link would try — and fail — to load the destination page
inside the small embedded iframe instead of replacing the page.

## Required step: SEO title and description

Because each page's content is delivered through an embedded iframe,
Google Search does not necessarily read the `<title>` and
`<meta name="description">` tags inside the embed the way it would for a
normal page — the primary signal for Google Sites pages is each page's
own **Page settings** (the pencil/settings icon on the page in the Sites
editor → Page title and description fields). The tags inside each HTML
file are still included as good practice and for portability, but treat
the table below as the authoritative text to paste into each page's Sites
settings:

| Page       | Sites page title                         | Sites page description |
|------------|-------------------------------------------|--------------------------|
| Home       | Gerihco \| Management Consulting           | Gerihco is a management consulting firm delivering data, technology, and strategy services to government, financial services, and manufacturing institutions. |
| Services   | Services \| Gerihco Management Consulting  | An overview of Gerihco's management consulting services, including data analytics, AI and machine learning, cybersecurity, and more. |
| Industries | Industries We Serve \| Gerihco             | Gerihco serves government, financial services, and manufacturing institutions with long-term, sustainable consulting solutions. |
| About      | About Us \| Gerihco Management Consulting  | Gerihco is a national management consulting firm offering long-term, sustainable solutions to complex institutional problems. |
| Careers    | Careers \| Gerihco Management Consulting   | Learn about career opportunities at Gerihco and how to submit your resume for consideration. |
| Insights   | Insights \| Gerihco                        | Perspectives from Gerihco on the challenges facing government, financial services, and manufacturing institutions. |
| Contact    | Contact \| Gerihco Management Consulting   | Get in touch with Gerihco to discuss a management consulting engagement for your organization. |

Note also that Google Sites does not index embedded-code content in its
own *internal* site search box — a separate, minor limitation from public
Google Search indexing above.

## Content still marked as placeholder

Search any file for the word "Placeholder" to find every spot that needs
real content before launch. At a glance:

- **Home — proof-point statistics.** The three numbers under "who we
  serve" are blank. The original draft of this section had specific
  invented figures (e.g., "120+ programs delivered," "$400M," "18 yrs");
  those have been removed rather than carried forward, since they were
  not grounded in any of the source documents and would read as false
  claims if published as-is.
- **Services page — one description per service.** Each of the seven
  service sections needs a real paragraph.
- **Industries page — one description per industry.**
- **About page — the three "Our approach" value statements, and the
  Leadership section**, which currently has no team content at all (no
  names, titles, or bios have been invented).
- **Insights page — entirely placeholder.** No real articles exist yet;
  three placeholder cards illustrate the intended layout.
- **Careers page — no real job postings exist.** The "Open positions"
  section states plainly that none are currently listed, rather than
  inventing plausible-looking roles. One example card is included,
  clearly labeled "Example format," purely as a reference for the
  structure to duplicate once real postings exist — it should be removed
  before publishing if no roles are open.
- **Contact page — email, phone, and mailing address**, and the
  submission backend for the form (see below).

## Contact form and job application form: no backend yet

Both `contact.html` and `careers.html` contain forms with no `action`
attribute; submitting either currently does nothing useful. The Careers
page's resume-upload field is a real `<input type="file">`, but a static
site — Google Sites embed or GitHub Pages alike — has no server of its
own to receive or store an uploaded file; a browser can't send a file
anywhere without something on the other end to accept it. Before
publishing, either:

- Point the form at a service built for job applications (an applicant
  tracking system such as Greenhouse or Lever, or a form backend that
  explicitly supports file attachments — plain form-to-email services
  often do not), or
- Rely on the plain-email fallback already included next to the form
  ("Prefer email?"), which works today with no additional setup once a
  real careers email address is filled in, or
- Replace the section with Google Sites' own built-in "Contact Us"
  element, if still deploying there instead of GitHub Pages.

The general contact form has the same limitation and the same options —
see the note that was already here for it.

## Photography

Two of the ten candidates listed in `manifest.csv` were actually supplied
as image files (`hero01alt.jpg`, `government01.jpg`); the other eight
manifest rows are licensed candidates that were researched and vetted but
never uploaded, so they aren't on the site.

**Brand-safety check.** Both supplied images were inspected for visible
company logos, signage, or other brand marks before use — the same
"unbranded subjects" criterion the shortlist reasoning document applied
when it excluded an Apple Store photo earlier in this project.

- `images/hero-01-alt.jpg` (Alex Lvrs, via Unsplash) — an architectural
  detail shot of pipes and glazing. No text, signage, or logo of any kind
  is visible. **Passed.**
- `images/government-01.jpg` (Sebastian Schuster, via Unsplash) — the
  U.S. Capitol dome. No company branding is present (it depicts a
  government building, not a private company, so this check doesn't
  really apply to it the way it would to a corporate subject).
  **Passed.**

Both are in use: the hero alt photo as the home page's hero background
(behind a dark gradient for text contrast), and the government photo in
the Industries page's Government row.

**Two caveats worth flagging, distinct from the logo check:**

1. **Resolution.** The shortlist reasoning document set a 1920px-long-edge
   floor for any image used as a large, full-bleed element. Both supplied
   files fall short of that (`hero-01-alt.jpg` is 896×1344; `government-01.jpg`
   is 952×1288) — dimensions apparently weren't preserved on upload. They
   are usable as included, but will look softer than ideal on a large
   desktop hero on a high-resolution display. Re-supplying at full
   resolution before launch would be worth doing.
2. **Color grading.** The manifest's note on the hero alt image flagged a
   green/purple color cast that needed correcting before use against the
   site's dark theme. A moderate desaturation (via Pillow, `Color`
   enhance factor 0.72) was applied as a first pass when the file was
   copied into `images/`. This is a reasonable approximation, not a
   substitute for an actual edit in a photo tool if a more precise match
   is wanted.

**No image failed the brand-safety check this round** — there was
nothing to hold back or replace with a placeholder. The Financial
Services and Manufacturing rows on the Industries page show a styled
placeholder instead, but that's because no file exists for those sectors
yet, not because anything was rejected. If you supply
`financial-01.jpg` / `manufacturing-01.jpg` (or any other row from
`manifest.csv`) as actual files later, I can run the same check on them,
place them at `images/<proposed_filename>` to match the manifest's own
naming, and wire them into the corresponding row.

One structural note: this `images/` folder approach depends on GitHub
Pages serving the HTML and image files together as a normal file tree.
It will not work if this ever goes back to a Google Sites "Embed code"
box, since that method only accepts a text blob with no place to attach
accompanying files — photos would need to be re-inlined as data URIs or
hosted externally in that scenario.

## Design decisions and changes from the original file

- **Logo wordmark corrected.** The nav bar in the original
  `gerihco_homepage_concept_e.html` rendered "GERIHCO" in Inter at weight
  600, but the finalized, approved logo (`gerihco_horizontal.txt`) uses
  Helvetica/Arial bold. Every page now uses the finalized asset.
- **Service list reconciled with the source document.** The original
  homepage's "What we do" list included "Regulatory compliance" and "Risk
  management," which do not appear in the provided Business Services
  document. Both have been dropped so the site does not assert service
  lines beyond what was confirmed; the list is now the same seven items
  everywhere it appears (home teaser and Services page).
- **Non-functional "Search" label removed** from the nav bar and replaced
  with a working mobile-menu toggle, since a visible, non-interactive
  element that looks clickable is a real (if small) accessibility and
  usability problem.
- **Mobile navigation resolved as a CSS-only drawer** (a hidden checkbox
  plus a styled `<label>`, no JavaScript). This was an open decision
  noted from the prior session. A pure-CSS mechanism was chosen over a
  JavaScript-driven one because the exact sandbox permissions Google
  Sites applies to a "Full page embed" are not published; removing the
  dependency on scripts being permitted removes an entire class of
  failure.
- **Icons recolored via `currentColor`** instead of a hardcoded hex value
  baked into each icon's markup, so a future palette change is a
  one-line CSS edit rather than a find-and-replace across every icon.
- **A skip-link, visible focus outlines, and a `prefers-reduced-motion`
  rule were added** — none of these were in the original file. They cost
  nothing visually for most visitors and are close to a minimum bar for
  an accessible site.
- **Every block of copy without a confirmed source is visibly marked as
  a placeholder** (italic, gray, usually bracketed), rather than written
  to sound finished. This was a deliberate trade-off: it makes the site
  look visibly unfinished in these spots, which is preferable to
  polished-sounding copy that could be mistaken for a real, vetted claim
  about the company.

## Maintaining this site

`build_site.py` is the script that generated the six HTML files. Because
Google Sites gives each embedded page an isolated iframe with no shared
include mechanism, every page has to carry its own full copy of the CSS
and navigation markup — hand-editing six near-identical files invites
them to drift out of sync. The script keeps one canonical copy of the
shared pieces (design tokens, CSS, nav bar, footer, icon set) and stamps
out the six files from it. To make a site-wide change (e.g., adding a
seventh nav item, or changing a color), edit `build_site.py` and re-run:

```bash
python3 build_site.py
```

This regenerates all six files into the same directory the script is run
from. Page-specific content (the paragraphs, service list, etc.) is also
defined in this script, in clearly labeled Python data structures near
the top of the file.
