# Releases

The repository uses the upstream template's semantic-release pipeline, adapted
for a main-only PR workflow. No release is triggered by pushing a task branch.

Before the first release:

1. Pass the authenticated non-PRO acceptance procedure in [testing.md](testing.md).
2. Commit the sanitized results through a task worktree and `ship`. Remove the
   experimental warning and mark the compatibility target verified only after
   those results pass. Continue to state unavailable PRO testing honestly.
3. Set repository Actions variable `FOLDER_REVIEW_E2E_VERIFIED=true` only after that
   evidence exists. The Release workflow is skipped while this variable is absent.
4. Enable GitHub Actions to create pull requests in repository workflow permissions.
5. Dispatch **Release** on `main`. It runs tests/build before semantic-release,
   generates versioned `.mpp` assets, and opens a PR for generated source metadata.
6. Merge the generated metadata PR through the server-side PR workflow. Confirm
   `patches-bundle.json` refers to the published artifact and that Morphe can add
   `JCapretta/chessable-patches`, discover the patch, and apply it to the supported APK.

Only source and patch bundles are published, never original or patched APKs.
Do not hand-edit generated metadata or CHANGELOG.md. Release automation owns those
files. Never force-push release tags or generated history. Address release issues
with a new release. Do not start another release before the metadata PR is merged.

Reset the verification variable when changing supported app builds or behavior
until the new version's authenticated checks pass. Development builds remain
downloadable as CI artifacts without representing a verified release.
