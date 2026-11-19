# Review and activate the profile

The implementation is local on `feat/lowlighter-profile`. This task does not push, merge, or change repository visibility. The public special repository `doanvinhlong18/doanvinhlong18` now exists; it was observed while researching this redesign. Use a feature-branch pull request against its current default branch when you decide to publish.

## Local review

Open the README preview in your editor. The `.preview/` folder contains local browser previews and desktop/mobile screenshots from verification; it is deliberately ignored by Git.

```powershell
python scripts/build_assets.py
python scripts/verify_profile.py
python scripts/verify_profile.py --online
```

To update the actual public data:

```powershell
python scripts/refresh_metrics.py
```

These commands need Python 3.10+ and no third-party packages. Public-data fetching uses GitHub's unauthenticated API quota. If GitHub is unavailable or the source format changes, keep the existing checked-in snapshot and try again later.

## Automatic updates without a personal token

After the files are merged into the special repository's default branch, open **Actions → Refresh profile metrics → Run workflow**. The workflow also runs on Mondays at 09:23 Asia/Bangkok. It fetches public data and commits the generated images and snapshot using GitHub's built-in repository token. Only the refresh job has `contents: write`; no personal token is needed for this path.

Repository policies or protected branches can reject a bot push. In that case run the refresh locally and submit the asset changes in a pull request. The checked-in images continue to work if a refresh fails. Scheduled workflows can be disabled by GitHub after prolonged repository inactivity.

## Activate the native lowlighter/metrics engine

This optional step changes the left infographic to a render produced by the actual Metrics engine. The layout and cached files are already complete without it.

1. In your GitHub account, create a **Personal access token (classic)** for public data, with **no scopes selected** and a suitable expiration. This follows the [Metrics setup guide](https://github.com/lowlighter/metrics/blob/366f8b9dfe3a59656c67d5dcad9950f59c9bc96d/.github/readme/partials/documentation/setup/action.md). The built-in `GITHUB_TOKEN` is not a replacement for Metrics' account-data token.
2. In `doanvinhlong18/doanvinhlong18`, open **Settings → Secrets and variables → Actions → New repository secret**. Name it **`METRICS_TOKEN`** and paste the token into GitHub's secret value field. Do not put the token in a repository file or chat.
3. Run **Refresh profile metrics**. The workflow detects the secret and executes the pinned native action. The action writes only to the runner; a separate validation step adopts the image, and the final workflow step commits the approved output files.
4. If the native step fails, inspect its Action log. The custom public-data infographic remains the fallback. No private-repository scope is needed for this configuration.

The native step builds the pinned source rather than pulling a mutable prebuilt Metrics image. It can take longer than the standard-library refresh. Its first authenticated run cannot be verified locally without your repository secret; no token was available or requested during implementation.

## Local maintenance

Python 3.10+ is sufficient; these commands use only the standard library:

```powershell
python scripts/refresh_metrics.py
python scripts/verify_profile.py --online
python -m unittest discover -s tests -v
```

To rebuild the artwork from the existing snapshot without making network requests, run `python scripts/build_assets.py`. This selects the custom renderer again, replacing any previously adopted native overview image; the next configured workflow run can regenerate the native version.

The implementation was checked using GitHub's Markdown API, local Chromium previews in both themes at 1440px and 375px, SVG text bounds, public link checks, and six regression tests. The two images shared a row on desktop and stacked on mobile without page overflow. Local review screenshots are in the ignored `.preview/` directory; GitHub's final profile appearance should still be reviewed after publication.

## Git ownership

If Git again reports the known `CodexSandboxOffline` / `ACER` ownership mismatch, this repository-specific trust exception is sufficient for the trusted workspace:

```powershell
git config --global --add safe.directory D:/Work/doanvinhlong18
```

The implementation does not modify global Git configuration. Do not use a wildcard safety exception.

## Final checklist

- [ ] Check the README in the actual GitHub profile, in both themes.
- [ ] Confirm two columns on desktop and stacked columns at 375px mobile width.
- [ ] Check all four project links; none should have a prominent showcase card.
- [ ] Confirm the snapshot date, contribution counts, and language-exclusion note.
- [ ] Confirm your 2+ years / enterprise-experience wording is still current.
- [ ] Expand the text profile and verify that it describes project and learning scope accurately.
- [ ] Run the workflow without a Metrics token to verify the fallback path in GitHub Actions.
- [ ] If enabling the native engine, add `METRICS_TOKEN` in GitHub Secrets and review its first run.
- [ ] Publish through your normal review process; do not force-push or merge automatically.

See [DESIGN.md](DESIGN.md) for the layout, data interpretation, rendering paths, and maintenance details.
