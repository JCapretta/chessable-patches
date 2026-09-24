# Chessable Patches

Focused Android usability patches for Chessable, distributed as a third-party Morphe source.

**Experimental: authenticated folder-review and server-persistence testing is pending. No verified release is published yet.**

The first patch restores native folder reviews and the existing random/sequential review setting on Chessable 3.0.4 (118333). It reviews due material using the app's own scheduling and progress tracking.

## Installation

After the first verified release, [add this source to Morphe](https://morphe.software/add-source?github=JCapretta/chessable-patches), select the supported original Chessable APK, and enable **Enable folder reviews**.

Open a folder containing due reviews and tap **Review Folder**. During review, use the board settings' **Review All is randomized** switch to mix courses. The native preference is shared with global Review All; its default is unchanged.

Development bundles are available in successful GitHub Actions runs. They are test artifacts, not verified releases. Unsupported or previously modified bundles fail with an explanation.

## Development

Use Java 21 and an Android SDK. For local dependency resolution, configure a dedicated GitHub token with `read:packages` in your user-level Gradle properties (`gpr.user`, `gpr.key`). Never commit credentials. CI uses its short-lived GitHub Actions token.

```sh
task verify
```

The bundle is written to `patches/build/libs/`. Follow [AGENTS.md](AGENTS.md) for the worktree and PR workflow. See [patch design](docs/patch-design.md), [testing](docs/testing.md), and [releasing](docs/releasing.md).

## Patch catalogue

<!-- PATCHES_START EXPANDED -->
> **Development build (unreleased)**&nbsp;&nbsp;•&nbsp;&nbsp;`agent/folder-reviews`&nbsp;&nbsp;•&nbsp;&nbsp;1 patches total
<details open>
<summary>📦 Chessable&nbsp;&nbsp;•&nbsp;&nbsp;1 patch</summary>
<br>

**🎯 Supported versions:**

| 🧪&nbsp;3.0.4 |
| :---: |

| 💊&nbsp;Patch | 📜&nbsp;Description | ⚙️&nbsp;Options |
|----------|----------------|-----------|
| [Enable folder reviews](#enable-folder-reviews) | Review due material across a folder using Chessable's native random or sequential order. |  |

</details>

<!-- PATCHES_END -->

## License

[GPLv3](LICENSE), with the inherited notices in [NOTICE](NOTICE). This project is not affiliated with Chessable or the Morphe project. APKs and extracted app code are not distributed here.
