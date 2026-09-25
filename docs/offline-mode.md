# Offline course study

Enable offline mode exposes Chessable's existing course downloads to non-PRO
accounts. Sign in and download an owned course while online. After its download
finishes, its lessons and due reviews are available without connectivity. Native
local storage keeps completed progress across restarts; reconnect with the app
open to synchronize it. Undownloaded courses remain unavailable offline.

This covers course MoveTrainer content, not video downloads, browsing the shop,
or signing in without a connection. Course ownership and server authorization
remain unchanged. The patch does not mark the account PRO or alter schedules.

## Supported build and implementation

The supported original APK and Hermes bundle fingerprints are the same as
[the folder patch](patch-design.md): Chessable 3.0.4 (118333), Hermes 96.
Ten fixed-size edits preserve function offsets and exception tables:

| Native component | Change |
| --- | --- |
| DownloadCourseItem | Use the native downloader and remove its PRO badge. |
| authorizeJwtOrSignUserOut | Permit offline startup through existing cached-token and sign-out checks. |
| Network error handler | Apply the existing offline route allowlist to every account tier. |
| Home and course page | Permit downloaded content and local dashboard refresh while disconnected. |
| NetworkState | Display the existing network transition banner. |
| Cached session restoration | Decode the JSON-serialized token before passing it to the original setJwt path. |

Native storage serializes values as JSON, but the fallback token restore reads
the raw serialized string. Without decoding, an offline cold start can install
quotation marks as part of the token, producing a 401 on reconnection. The patch
reuses the app's existing JSON.parse callback in the now-unreachable PRO error
block, then rejoins the original setJwt path. The success-only redirect follows
ResumeGenerator's rejection check; active tokens bypass it. Null still reaches
the missing-token sign-out check. HTTP errors and the progress queue are unchanged.

Both patches share a recognized edit profile. Either can be selected alone or
applied after the other; unselected edits are not enabled. Validation normalizes
only these audited edits before checking the full original SHA-256, so other
bundle changes still fail closed. The Hermes footer is recomputed after editing.

## Verification

Local tests cover integrity, independent patch composition in either order,
unexpected sibling edits, startup branch targets, local feature registers, and
the stored-token decoding trampoline returning to the original session setter.

Audit a combined APK with:

```sh
python3 scripts/verify-patched-apk.py ORIGINAL.apk PATCHED.apk \
  --patches folder-reviews offline-mode
```

For an offline-only APK, use `--patches offline-mode`. Morphe CLI requires
`--exclusive -e 'Enable offline mode'` to disable other default-selected patches.
The auditor verifies every declared edit, unchanged length, the Hermes checksum,
and byte-for-byte equality outside those edits and the checksum.

## Live acceptance

Testing on 2026-09-25 used a dedicated non-PRO account on headless Android 15 ARM64, with the
emulator's Wi-Fi and mobile data disabled independently of the host network.
Private screenshots and storage snapshots stay outside version control.

- The baseline course download action opens the PRO upsell.
- The patched action downloads owned Basic Endgames (6371) and Everything You
  Need to Know About Chess (193039), showing their native downloaded indicators.
- Downloaded courses open offline; an undownloaded control course is grayed out.
- Basic Endgames review completed offline and created a pending progress record.
  The record survived a force-stop/restart. A manual retry helped diagnose the
  original reconnect error, so that first run alone is not automatic-sync proof.
- A separate offline lesson increased course 193039's local learned count from
  2 to 3. Its pending record survived three cold starts. An independent server
  read still showed 2 before reconnection; automatic native sync changed it to 3
  and cleared the local queue. That run exposed the incorrect token restoration
  addressed by the final decoding edits.
- With the final offline-only build, a new lesson increased the local count
  from 4 to 5. One pending record survived an offline force-stop/restart. The
  independent server count was 4 immediately before reconnection and 5 after
  automatic sync; the queue became empty. There were zero 401 or sync-error log
  entries, and no error dialog on reconnection. The restored token also retained
  the correct single JSON serialization layer in storage.
- All 17 local tests pass without failures or skips. Morphe Desktop 1.17.0 builds
  both the combined and standalone APKs. Independent audits verify their exact
  declared changes, and the edited functions and reused JSON parser disassemble.
- Canceling download deletion preserves the local copy. Confirming deletion
  restores **Download course**, removes its downloaded indicator, and leaves the
  learned count at 5/92.

Final Hermes bundle SHA-256:

- Offline only: `911c7c78822852ab3230b5bc34c8826a0551c0a99ccb4a7086128ab2d19a0f53`.
- With folder reviews: `fb2af0cae8b1d21977b2ba5cd93551b456f5f7736e9274cd4a1512cc9ebdf501`.

PRO accounts, dark-theme rendering, video downloads, long-duration background
execution, low-storage failures, and expired-session recovery are not validated.
Exact next-review timestamps and simultaneous study on multiple devices are not
asserted by the course-count checks. Never clear app storage or uninstall with
unsynced work pending.
