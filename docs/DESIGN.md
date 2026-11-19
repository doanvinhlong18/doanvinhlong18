# A Metrics-style engineering profile

The reference is [lowlighter's actual profile](https://github.com/lowlighter), with its narrow infographic columns and isometric contribution calendar. The local source at `D:\Work\metrics` was inspected at revision `366f8b9dfe3a59656c67d5dcad9950f59c9bc96d`, especially the Classic template, isocalendar plugin, language plugin, and action configuration. The reference repository was read only.

The redesign replaces the large cinematic hero and long portfolio sections with a compact nameplate, two balanced infographic columns, one row of project links, and an expandable text profile. Each public repository has equal weight. The interface takes its rhythm from lowlighter; the biography, colors, public data, and engineering content belong to Doan Vinh Long.

## Layout

- `profile-header.svg` is a restrained identity strip. Its mobile counterpart recomposes the same identity for a narrow screen.
- `metrics/github.svg` contains public-repository context, a 26-week isometric contribution landscape, and a programming-language distribution.
- `metrics/engineering.svg` contains the backend identity, four engineering interests, learning areas, and principles.
- The two infographic images float left/right at 390px, matching the pattern in lowlighter's README. At narrow widths, GitHub's image max-width rule shrinks each image to the available width and they wrap onto successive rows. The transparent 1px spacer clears both columns before the following native text.
- The introduction, project links, contact, and expandable engineering profile remain native Markdown / supported HTML. The complete engineering content remains available if an image fails.

The images have a fixed dark surface in both GitHub themes. This avoids depending on the operating system's color-scheme setting to match GitHub's independently selected theme. Native text follows GitHub's selected theme.

## Visual tokens

| Token | Value |
| --- | --- |
| Background | `#0D1117` |
| Surface | `#101722` |
| Border | `#28364A` |
| Text | `#E6EDF3` |
| Supporting text | `#9BAEC4` |
| Blue | `#79B8FF` |
| Purple | `#B4A2FF` |
| Cyan | `#56D4DD` |

The typography uses Segoe UI / Arial with a monospace identity label. Small line icons, fine dividers, limited color, and consistent spacing replace badge walls and large decorations. The isometric calendar provides depth without needing a raster image or real-time 3D. It is vector geometry, not a rendered WebGL scene. No animation is used.

## Data and two rendering paths

The checked-in overview is rendered locally by `scripts/render_profile.py` using real public data from `assets/metrics-data.json`. This is a custom bootstrap renderer, **not a claim that the native Metrics engine has already run**. The isometric projection is adapted from the MIT-licensed isocalendar source; the license and attribution are in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

`refresh_metrics.py` gets the public repository list, each repository's actual GitHub language-byte totals, and GitHub's public contribution calendar. It joins each calendar cell to its actual count tooltip; it never estimates counts from intensity levels. The height of an isometric column is proportional to its source count relative to the largest displayed day. Empty days remain low floor tiles. Only a complete, validated fetch is written. A failed fetch keeps the previous snapshot.

Language percentages use bytes in owned, non-fork public repositories. The included denominator excludes Jupyter Notebook, HTML, CSS, SCSS, Less, Jinja, Dockerfile, Batchfile, and Handlebars. The five largest remaining languages are shown separately, with the rest grouped as Other. This exclusion is disclosed in the image and README. Bytes are not time spent, authorship, professional proficiency, or a career ranking.

The optional native `lowlighter/metrics` step is already wired into the workflow. With `METRICS_TOKEN` configured, it generates the left infographic using Classic + isocalendar + languages at the pinned revision. Its output is validated before replacing the bootstrap file. On failure, the freshly generated public-data version remains. The right infographic and responsive header stay consistent. The native engine may show a slightly different date window or grouping because its aggregation algorithm differs from the bootstrap renderer.

The native Classic renderer uses a self-contained SVG `foreignObject` with embedded XHTML/CSS. This is the format used by lowlighter's public profile; it is not arbitrary HTML in the README. Verification allows this format only for `assets/metrics/github.svg`, rejects scripts and remote image/font references, and retains the simple local renderer as a fallback. The other assets contain plain SVG geometry and text.

## Maintenance

```powershell
python scripts/build_assets.py              # offline rebuild from saved data
python scripts/refresh_metrics.py           # read-only public-data fetch + rebuild
python scripts/verify_profile.py            # local validation
python scripts/verify_profile.py --online   # additionally check public URLs
```

These scripts use only Python's standard library. No Node packages, Docker, API key, or Metrics checkout is required for the local bootstrap profile. Docker and a scopeless GitHub personal access token are used only by the optional native Metrics action on GitHub's Ubuntu runner.

The account's name, 2+ years of experience, and enterprise background remain owner-provided. Repository data does not independently establish employment or production deployment. No email, LinkedIn, external achievements, sponsors, private-repository details, or personal data from lowlighter were invented or copied.
