# Art Frame TV — marketing site

Static landing page, guides and privacy policy for `getframetv.com`. No build step: plain
HTML/CSS/JS, deployable to Firebase Hosting, GitHub Pages or any static host.

**This repo is the website only.** The Android app lives in a separate repository (`TVFrame`,
package `team.dsa.artframetv`). Paths below that start `app/` or `store/` refer to that repo.

| File | What it is |
| :--- | :--- |
| `index.html` | Landing page |
| `privacy.html` | Privacy policy — the URL the Play Console listing points at |
| `styles.css` | One stylesheet for both pages |
| `main.js` | The hero television: presets, crossfade, material lists |
| `images/` | `social-1200x630.png` (OG card) and `icon-180.png` (apple-touch-icon) |
| `firebase.json` | Hosting config with `cleanUrls`, CSP and cache headers |

## Brand

Colours come from the ArtFrame TV brand pack (`android_res/values/colors.xml`) and are declared
once on `:root` in `styles.css`:

| Token | Hex | Brand name | Use |
| :--- | :--- | :--- | :--- |
| `--navy` | `#1C2D42` | `artframe_navy` | Primary UI / background |
| `--ink` | `#121820` | `artframe_dark_background` | App surface background |
| `--gold` | `#D4AF37` | `artframe_gold` | Focus outlines, accents, logo |
| `--bronze` | `#8C6239` | `artframe_accent_bronze` | Frame borders, secondary text |
| `--text` | `#FFFFFF` | `artframe_white` | Primary text |

Two deliberate departures, both documented inline in `styles.css`:

* `--bronze-lt` (`#C89A62`) carries small secondary text. Bronze at full strength is 3.25:1 on
  `--ink` — fine for borders and decoration, under the 4.5:1 body-text floor. `#8C6239` is still
  used for borders and the gallery-strip frames, which is the brand's stated use for it.
* `--mat-paper` (`#F5F2EA`) is **not** brand chrome. It is Warm Cotton White conservation mat
  board, as the app renders it, and must not follow the brand palette if that palette changes.
  The same applies to every swatch in the Materials section and inside the hero television —
  those are product truth, taken from `MatteColor.kt` and `FrameMoulding.kt`.

The logo mark in the nav and `favicon.svg` are redrawn from the brand pack's `logo_vector.svg`:
navy ground, double gold rule, four gold corner accents.

## The hero television

The TV on the wall is not an image — it is the app's own framing engine rebuilt in CSS, so
what a visitor sees is what the product actually renders. The frame geometry is driven by
custom properties that `main.js` sets per preset:

| Property | From |
| :--- | :--- |
| `--moulding-w` | `FrameSettings.frameWidthDp`, as a % of a 960dp-wide TV panel |
| `--moulding-a` / `--moulding-b` | `FrameMoulding.primaryColor` / `secondaryColor` |
| `--matte-c`, `--matte-m` | `MatteColor`, `FrameSettings.matteMarginDp` |
| `--bw` | `bottomWeighted` → 1.18, the gallery convention |
| `--bevel-hi` / `--bevel-sh` | `BevelCoreColor` |
| `--depth` | `matteDepthShadowAlpha` |
| `--ar` | `Artwork.aspectRatio`, so the mat opening is cut to the print |

Percentage padding resolves against the screen's width, which gives the mat the same
relationship to the panel that dp has on a real 16:9 TV, at every viewport size.

**When the app's presets, mouldings or mat colours change, update the tables at the top of
`main.js` to match.** They are transcribed by hand from the app repo — nothing enforces this, so
it is the one thing that can quietly drift:

* `app/src/main/java/team/dsa/artframetv/model/FrameSettings.kt`
* `app/src/main/java/team/dsa/artframetv/model/FrameMoulding.kt`
* `app/src/main/java/team/dsa/artframetv/model/MatteColor.kt`
* `app/src/main/java/team/dsa/artframetv/model/BevelCoreColor.kt`
* `app/src/main/java/team/dsa/artframetv/data/ArtworkRepository.kt`
* `app/src/main/java/team/dsa/artframetv/ui/TvSettingsOverlay.kt` — the mat-thickness and
  frame-width scales

## Before publishing

0. **Domain is live, and indexable.** `getframetv.com` is served by GitHub Pages (`CNAME` in this
   repo, DNS at Namecheap), which sends no `X-Robots-Tag`. The `noindex, nofollow` header in
   `firebase.json` only affects the Firebase test deploy at `artframetv.web.app`, which is
   deliberately kept out of search because every canonical points at `getframetv.com`. Confirm with
   `curl -sI https://getframetv.com/ | grep -i robots` returning nothing.
1. **Privacy policy §2** has a placeholder for the registered postal address. Fill it in — a
   controller address is required under GDPR Art. 13, and Play's data-safety review checks the
   policy is complete.
2. **A German `Impressum`** is a separate legal requirement for a UG's website (§5 DDG). It is
   not part of this policy page; add it as `imprint.html` and link it from the footer.
3. **Two call-to-action buttons** read "Get it on Google Play" and link to
   `play.google.com/store/apps/details?id=team.dsa.artframetv` (one in `index.html`'s hero, one in the closing section).
4. **Social card.** `images/social-1200x630.png` and `images/icon-180.png` are generated in the
   app repo by `store/generate/build.py`, alongside the Play assets, so the OG card and the store
   listing share one lockup. Re-running that script writes into this repo — point its
   `<out-site>` argument at `<this repo>/images`.
5. **`.well-known/assetlinks.json`** if you want Play Install Referrer or app links from the site.

## Local preview

```bash
python3 -m http.server 4178 --directory site
```

## Deploy

The phone sign-in relay (`relay/` in the app repo, served at the same domain) is a separate
Firebase Hosting site with a much stricter, `noindex` config — do not merge the two. Add this as
its own hosting target:

```bash
firebase deploy --only hosting --project artframe-tv
```

The CSP in `firebase.json` allows exactly what the pages use: Google Fonts, plus images from
`upload.wikimedia.org` and `images.unsplash.com`. Adding a script, font or image host means
adding it there too, or it will be blocked in production but work fine locally.
