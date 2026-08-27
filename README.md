# Gerihco website — deployment notes

# Gerihco website — deployment notes

This package contains a seven-page site expanded from the original
`gerihco_homepage_concept_e.html`. It's deployed as a static site on
**GitHub Pages**, serving the repository's files directly — an earlier
version of this project targeted Google Sites' "Embed code" feature
instead, and some of this document (and a few now-removed pieces of the
HTML itself, like `target="_top"` links) reflected that. This revision
brings both fully in line with a plain GitHub Pages deployment.

## Files

| File               | Page / purpose |
|--------------------|--------------|
| `index.html`       | Home         |
| `services.html`    | Services     |
| `industries.html`  | Industries   |
| `about.html`       | About        |
| `careers.html`     | Careers      |
| `insights.html`    | Insights     |
| `contact.html`     | Contact      |
| `404.html`         | Custom not-found page; GitHub Pages serves this automatically for any unmatched URL |
| `robots.txt`        | Tells search engine crawlers everything is crawlable, and points them at the sitemap |
| `sitemap.xml`        | Lists all seven real pages, for search engines |
| `images/`          | Photography used by the pages above |
| `build_site.py`    | Generator script that produced every file above (see "Maintaining this site" below) |

Each `.html` file is a complete, self-contained document (fonts, CSS, and
markup all inline except for images) and can be opened directly in a
browser to preview it.

## Publishing to GitHub Pages

This is already how the live site works, so there's nothing new to set
up — noted here for reference or in case Pages ever needs re-enabling:

1. Push all the files in this package to the repository (`GerihcoIT/gerihco-website`),
   preserving the flat structure — every `.html` file, `robots.txt`, and
   `sitemap.xml` at the repository root, with `images/` as a real
   subfolder alongside them.
2. In the repo's **Settings → Pages**, set the source to the branch and
   folder these files live in (this repo is already configured and
   serving from `main`).
3. GitHub Pages serves each file at its own filename directly —
   `services.html` really is `.../services.html` on the live site. There
   is no separate publish step, no per-page embed box, and no URL
   remapping to do afterward, unlike the Google Sites workflow this
   project used earlier.

## SEO: already handled directly in the HTML

Because GitHub Pages serves these files as real, standalone pages rather
than through an embedding layer, the `<title>`, `<meta name="description">`,
`<link rel="canonical">`, and Open Graph / Twitter Card tags already
present in each file's `<head>` are exactly what search engines and
link-preview crawlers read — there is no separate settings panel to also
update, the way Google Sites required. Nothing further is needed here
unless the content of a page changes enough that its title or description
should change too (edit the `PAGES` list in `build_site.py` and re-run
it).

`sitemap.xml` lists all seven real pages (not `404.html`, which is
deliberately excluded and marked `noindex`, since a not-found page has no
business in search results). `robots.txt` points crawlers at it.

One gap worth closing when there's branded artwork available for it: no
`og:image` / `twitter:image` is set on any page yet. Social platforms
expect a landscape image around 1200×630 for link previews, and nothing
on the site currently has that aspect ratio — the closest candidates
(`hero-01-alt.jpg`, `government-01.jpg`) are both portrait orientation, so
using either as-is would get cropped in an unflattering way. Once a proper
landscape image exists, add it once in `build_site.py`'s `PAGE_SHELL`
(both meta tags read from a single shared value) rather than per page.

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

The `images/` folder in the repository now has more files than were
originally handed off — additional candidates from `manifest.csv` were
added directly on GitHub. Each was checked the same way as before: opened
and visually inspected for logos, signage, identifiable branding, and
other departures from the brief's own "no staged/branded subjects"
criterion, rather than trusting the manifest's notes at face value.

**Financial Services** — three candidates existed at `financial-01.jpg`,
`-02.jpg`, `-03.jpg`. None of them are actually the photos `manifest.csv`
describes for those filenames; whatever went into the folder doesn't
match the manifest's photographer credits or descriptions row for row.
Judged on their actual content:

- `financial-01.jpg` — **failed.** This is a Manhattan Bridge / Dumbo
  waterfront scene with three people clearly posed in frame. It matches
  the description of an image the original photo shortlist explicitly
  excluded for being under Unsplash's paid **Unsplash+ license** rather
  than the free one the brief requires, and it also violates the
  no-people, no-staged-shot criterion on its own terms.
- `financial-02.jpg` — **failed.** This is a street-level view of the
  Lloyd's of London building (recognizable by its exposed stainless-steel
  pipework) alongside 30 St Mary Axe ("the Gherkin"). No text logo is
  printed anywhere in the frame, but Lloyd's of London is a specific,
  instantly recognizable financial institution — this is the same
  "identifiable real company" problem the brief's Apple Store example was
  meant to rule out, just via architecture instead of a sign.
- `financial-03.jpg` — **passed.** A low-rise city skyline reflected in
  water at dusk; no readable signage, and no landmark distinctive enough
  to name a specific city or institution. **Now in use** on the
  Financial Services row.

**Manufacturing** — three candidates existed at `manufacturing-01.jpg`,
`-02.jpg`, `-03.jpg`:

- `manufacturing-01.jpg` — **failed.** A robotic arm with "DELTA" printed
  on it in a clearly legible logo, filling a large part of the frame —
  this is exactly the image the project's own prior photo research had
  already identified and rejected for this reason.
- `manufacturing-02.jpg` — **failed**, for two independent reasons: a
  "FANUC" logo is legible on the arm's joint housing, and there are
  multiple people visible in the background, which the brief's criteria
  also rule out.
- `manufacturing-03.jpg` — **passed.** A steel mill interior with molten
  metal and rising steam; no people, no signage. **Now in use** on the
  Manufacturing row.

**Government** — an additional `government-02.jpg` (the U.S. Supreme
Court building) was also added to the folder. It passes the same check
(a government building isn't a company, so there's no brand-association
concern), but there was no placeholder left to fill — `government-01.jpg`
already covers that row. It's sitting in the repository unused; worth
keeping in mind if a second government-sector image is ever wanted (the
About page, for instance, has no photography at all yet).

**A separate, unrelated bug worth fixing regardless of the above:**
`financial-02.jpg`, `manufacturing-01.jpg`, `manufacturing-02.jpg`, and
`government-02.jpg` are all saved as **AVIF-format image data with a
`.jpg` file extension** (confirmed by reading the file's actual header
bytes, not just its name) — GitHub Pages serves them with a
`Content-Type: image/jpeg` header regardless, which browsers are told to
trust exactly (`X-Content-Type-Options: nosniff` is set), so these
specific files are likely to fail to render at all if referenced in an
`<img>` tag, independent of whether their content passes the brand
check. `financial-01.jpg`, `financial-03.jpg`, and the two files already
confirmed live (`hero-01-alt.jpg`, `government-01.jpg`) are genuine JPEGs
and unaffected. Since three of the four mismatched files failed the brand
check anyway, the only live impact today is that `government-02.jpg`
would need to be re-exported as a real JPEG before it could actually be
used. Whatever tool produced these — likely a batch converter or
"download as" step that defaulted to AVIF — is worth checking if more
images get added this way.

`financial-03.jpg` and `manufacturing-03.jpg` were resized to a 1920px
long edge and recompressed (quality 82) before being placed in this
package's `images/` folder, both to keep page weight reasonable and, for
`manufacturing-03.jpg`, to fix the AVIF/JPEG mismatch by re-encoding it
properly in the process.

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
- **Google Sites artifacts removed, now that the site is on GitHub
  Pages.** Every `target="_top"` attribute is gone (it only ever mattered
  for escaping a Sites iframe), and the per-page header comment and this
  document no longer describe the old "Full page embed" workflow.
- **CSS moved out of every individual page and into one shared
  `styles.css`.** Each page used to carry a full inline copy of the same
  ~17KB of CSS, a direct consequence of Sites' isolated per-page iframes
  having no shared include mechanism. GitHub Pages has no such
  restriction, so this was pure waste once the constraint was gone — a
  visitor now downloads the stylesheet once and it's cached for every
  other page on the site, and every page's file size dropped by more
  than half.
- **`404.html`, `robots.txt`, and `sitemap.xml` added.** None of these
  were possible in a meaningful way under the Sites embed model (there
  was no real file tree to add a root-level 404 page or robots file to);
  GitHub Pages serves all three automatically once they exist at the
  repository root.
- **Canonical URLs and Open Graph / Twitter Card tags added** to every
  page's `<head>`, so shared links get a real preview instead of
  whatever a platform's crawler can improvise, and search engines are
  told the one authoritative URL for each page.

## Maintaining this site

`build_site.py` is the script that generated every file above. CSS now
lives in one place (`styles.css`, linked from every page) rather than
being duplicated inside each HTML file — that duplication was a
necessary consequence of Google Sites' isolated per-page iframes, which
had no shared include mechanism; it's gone now that GitHub Pages serves
these as ordinary files that can just link to a common stylesheet. The
navigation bar, footer, and icon set are still assembled from one
canonical copy in the script (page *content* still legitimately differs
page to page, so that part was never duplicated), and the same rule
applies: to make a site-wide change — a new nav item, a color, a new
page — edit `build_site.py` and re-run it:

```bash
python3 build_site.py
```

This regenerates every HTML file, `styles.css`, `robots.txt`, and
`sitemap.xml` into the same directory the script is run from.
Page-specific content (the paragraphs, service list, etc.) is defined in
this script too, in clearly labeled Python data structures near the top
of the file.
