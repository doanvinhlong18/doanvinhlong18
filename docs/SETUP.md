# Setup and final review

The complete implementation is prepared locally. No GitHub repository was created, no content was pushed, and no visibility settings were changed. The local branch is `feat/profile-redesign`.

## Local review

Open `README.md` in a Markdown preview with HTML support. VS Code's preview can differ from GitHub's renderer, particularly for `<picture>` and table spacing. Run:

```powershell
python scripts/verify_profile.py
python scripts/verify_profile.py --online
```

The first command validates asset references, SVG safety and syntax, dimensions, and the activity snapshot. The second also checks public repository links and the official activity endpoint. It performs read-only requests and does not publish anything.

## Publish only when ready

The public repository list inspected on 2026-11-19 did not contain `doanvinhlong18/doanvinhlong18`. A private repository of that name cannot be ruled out without an authenticated account. Check your account before creating a new one.

1. After approving the local design, create a repository named **`doanvinhlong18`** under **`doanvinhlong18`**, or use an existing repository of that exact name. A GitHub profile README is displayed only when this special repository is public and contains a nonempty root `README.md`.
2. If the remote has existing files, fetch it and base a dedicated feature branch on its default branch. Copy these files into that branch and resolve differences deliberately. Do not overwrite unrelated files or force-push.
3. Review the changes locally, commit, push the feature branch, and open a pull request. Merge only after review. Publishing publicly is a separate owner decision.
4. Once merged, open the actual GitHub profile in both themes and on a phone. The relative asset paths will resolve from the special profile repository.
5. To enable refreshes, allow the included GitHub Action to run and ensure repository policy permits its job-scoped write permission. Run **Refresh profile activity → Run workflow** once. No personal access token or API key is needed.

For a brand-new **empty** remote, after you have explicitly chosen to create it and publish this work:

```powershell
git add README.md assets docs scripts .github .gitignore
git commit -m "Build cohesive backend engineering profile"
git remote add origin https://github.com/doanvinhlong18/doanvinhlong18.git
git push -u origin feat/profile-redesign
```

An empty remote has no base branch for a pull request. Use GitHub's initial-branch setup deliberately; do not run these commands against an existing remote without fetching and reconciling its history. If your system reports a Git ownership warning, use a trusted normal-user checkout rather than changing global Git safety settings.

## Final verification checklist

- [ ] Confirm the 2+ years of experience and enterprise-work wording still match your current background.
- [ ] Review all research / configured-foundation labels before changing them to experience claims.
- [ ] Open all four public repository links.
- [ ] Check the hero, focus cards, toolkit, project table, and footer on the actual profile.
- [ ] Check both light and dark themes, 375px mobile width, and desktop width.
- [ ] Confirm mobile `<picture>` sources are selected and native table text remains readable.
- [ ] Ensure the activity date is recent; confirm its snapshot source matches GitHub.
- [ ] Test with image loading blocked: biography, stack, projects, principles, and contact remain available.
- [ ] Keep the static hero as the default; check reduced-motion behavior before adopting animation.
- [ ] Confirm that the publication and repository-visibility choices are intentional.

See [DESIGN.md](DESIGN.md) for design decisions and maintenance commands.
