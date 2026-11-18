# Design and maintenance

The profile is an engineering identity first. Four projects have equal weight in one compact table; no repository is positioned as a flagship. This follows the owner's clarification that the overall interface and visual harmony matter more than highlighting a particular repository.

## Visual system

| Token | Value | Purpose |
| --- | --- | --- |
| Background | `#080B14` | Hero and image panels |
| Surface | `#111827` | Raised planes and glass-like layers |
| Primary | `#6366F1` | Infrastructure edges and identity accent |
| Secondary | `#06B6D4` | Connections and data flow |
| Accent | `#A78BFA` | Small highlights |
| Text | `#E5E7EB` | Primary image text |
| Muted | `#A7B3C8` | Supporting image text |

The hero uses hand-built isometric vector geometry: server towers, suspended database cylinders, service nodes, and routed connections. Gradients simulate material and lighting; this is an isometric SVG illustration, **not a true 3D render**. Image generation was unavailable, so there are no generated raster assets or image API dependencies.

Native Markdown carries the biography, toolkit, project details, and principles. This keeps important information selectable, accessible, and readable in GitHub's light and dark themes. The illustration panels keep their own dark background in either theme. Native GitHub tables supply the four focus cards, wrapping their text at narrow widths.

Typography inside images uses a local system stack (`Segoe UI`, Arial, sans-serif), with monospace for small labels. No remote fonts, tracking pixels, badge services, or remote image dependencies are used. All marks in `assets/icons/` are original category pictograms, not third-party brand logos.

## Responsive behavior and motion

The hero, principles, activity panel, and signature use `<picture>` with a mobile source at 600px. GitHub supports this image pattern; all content has a regular `<img>` fallback. Mobile artwork is recomposed rather than shrinking the desktop canvas. Native text provides the complete content if images are unavailable.

`hero.svg` and `hero-mobile.svg` are static by design. The separate `hero-animated.svg` adds restrained data-flow motion, floating geometry, and gradient movement, with a `prefers-reduced-motion` rule. It is an optional enhancement and is **not embedded in the README**: GitHub's image proxy, browser, and reduced-motion behavior can differ. The checked-in static hero remains the default and fallback. Neither version contains scripts, external references, `foreignObject`, WebGL, or interactive HTML.

## Regenerate artwork

Python 3.10+ is sufficient; the build and activity scripts use only the standard library.

```powershell
python scripts/build_assets.py
python scripts/refresh_activity.py
python scripts/verify_profile.py
python scripts/verify_profile.py --online
```

`build_assets.py` is the editable source for the hero, category icons, principles, dividers, and signature. It does not fetch data or change the README. The optional animated hero is generated from the same geometry.

`refresh_activity.py` fetches GitHub's public contribution HTML and stores only dates and intensity levels in `assets/activity-data.json`. It does not infer commit counts, contribution totals, streaks, or proficiency. A failed fetch or unexpected source format leaves the existing assets untouched. The snapshot explicitly shows its fetch date and source date range. Mobile uses the latest 13 weeks; desktop uses 26 weeks. Source parsing is a dependency on GitHub's HTML markup and may need maintenance if GitHub changes it.

The `refresh-activity.yml` workflow runs weekly and on manual dispatch. Its checkout action is pinned to a verified commit. It updates only the three activity assets on the repository's default branch, with job-scoped `contents: write`. It does not deploy or change repository visibility. Protected branches may reject its push; in that case run the script locally and submit the changes through a pull request. GitHub can disable scheduled workflows in inactive public repositories; manual dispatch and the checked-in snapshot still work.

To use the optional animation outside the README, reference `assets/hero-animated.svg` directly. If experimenting with it in the README, retain `hero.svg` and `hero-mobile.svg` as static alternatives and verify the actual GitHub rendering before keeping the change.

## Content integrity

The name, job title, 2+ years of experience, enterprise application background, and stated interests come from the owner's brief. They are self-reported, not independently verified by repository history. Public code supports the project descriptions. It does not establish employment, production deployments, user counts, or seniority.

Spring Data JPA includes Hibernate as its usual ORM provider; the profile makes no separate expert-level Hibernate claim. SQL Server is supported by the rental-management Java repositories. Redis and RabbitMQ are explicitly classified as configured foundations in ShopCore. gRPC is a versioned contract in that project, not a completed order-to-product business flow. Elasticsearch, entity matching, and additional Micrometer instrumentation remain learning topics. Prometheus and regression tests are supported by BigData's implementation.

No verified public email or LinkedIn was available. Do not add either without the owner's information. See [RESEARCH.md](RESEARCH.md) for the source evidence and limits.

## Verification performed

On 2026-11-19, all 14 SVGs parsed successfully and all 14 README image references resolved locally. The four project links, profile link, and official contribution endpoint returned HTTP 200. GitHub's GFM rendering API returned HTTP 200 and retained all four `<picture>` elements, all four focus-card headings, and the Markdown tables.

Chromium previews at 1440px and 375px were inspected in light and dark themes. No images were broken and the page had no horizontal overflow in the local preview. All four mobile image sources were selected at 375px. SVG text bounding boxes remained within their canvases. The optional animated hero had zero running CSS animations under reduced motion.

Simulated network failure and unexpected contribution-page markup both failed without changing the existing activity assets. Workflow YAML, trigger names, scoped write permissions, and authored-file whitespace were checked. These are local and API-rendering checks; the final appearance on the published GitHub profile still requires the owner review in [SETUP.md](SETUP.md).
