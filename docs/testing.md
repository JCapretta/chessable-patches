# Testing

## Current evidence

- Original 3.0.4 APK installs and launches on a fresh headless Android 15 ARM64 emulator.
- Original app reaches the email/password login screen.
- Static inspection located the folder and random-review restrictions described in
  [patch-design.md](patch-design.md).
- [CI run 35977727563](https://github.com/JCapretta/chessable-patches/actions/runs/35977727563)
  passed all 11 tests with zero skips and built the bundle on commit `7bac646`.
- Morphe Desktop 1.17.0 applied the bundle and signed the test APK successfully.
- An independent archive comparison verified exactly the five intended edits and
  checksum update. The five functions also disassemble successfully with hermes-dec.
- A modified bundle with a valid checksum was rejected by Morphe; no output APK
  was produced.
- Patched app installs and reaches the same login screen on a separate fresh
  headless Android 15 ARM64 emulator, with an empty crash log.
- Patched bundle SHA-256:
  `4ab62cf227a5696408d1f48ca72c1902143133a69b977298c35a20906b386663`.
- Authenticated baseline, queue behavior, and server persistence: **pending test-account access**.
- PRO-account regressions: **not tested; no PRO account supplied**.

These observations do not establish that the feature works end to end. CI results
cover the patch engine and compilation, not Chessable's authenticated service.
Smoke checks were performed on 2026-09-24. Screenshots, APKs, and patcher reports
are retained locally, not published with the source.

## Automated checks

`task verify` checks whitespace, runs Kotlin tests, and builds the `.mpp` bundle.
Tests cover malformed input, wrong versions, unexpected code, corrupt checksums,
overlapping edits, input immutability, bounded changes, repeat application, and
the branch/register semantics of the edited instructions.

Apply the bundle with the official Morphe Desktop CLI to the supported original
APK. Use `scripts/verify-patched-apk.py ORIGINAL.apk PATCHED.apk` to independently
check that only the declared bundle bytes and checksum changed. Install the
result in an isolated headless emulator, launch it, and inspect screenshots and
crash logs. A successful patch or login-screen launch is only a smoke test.

## Authenticated acceptance procedure

Use a dedicated non-PRO account, not a personal study account. Arrange credentials
through a private local file or another agreed mechanism. Never put passwords,
tokens, raw network logs, APKs, or extracted app code in Git or CI artifacts.

Prepare a folder with two accessible courses, each containing several learned
variations due for review. Keep another course with due material outside the
folder. Also prepare an empty folder and paused or not-yet-due material. Record
course IDs, folder membership, and initial counts privately.

1. On the original APK, confirm the account is non-PRO and the folder action is
   hidden despite due reviews. Capture the baseline without account identifiers.
2. Use a separate clean emulator installation for the patched APK. Sign in with
   the same test account. Verify the button label, count, placement, and themes.
3. Start folder review. Finish variations from both courses. Record course IDs;
   none may come from outside the selected folder or be ineligible for review.
4. Turn the native randomized setting on and off. Verify that it persists after
   restart and that enabled mode can select across courses between variations.
   One randomly contiguous run does not prove randomization failed. Inspect the
   selected native branch alongside multiple-course session evidence.
5. Cancel and restart review. Completed work must remain saved; remaining eligible
   work must remain available. Finish the session and check due counts.
6. Refresh the account in the original app. Verify persisted progress and next
   review times for completed material, with the outside course unchanged.
7. Check empty and fully reviewed folders, paused variations, a folder deleted
   before loading finishes, and a temporary connection failure. Missing folders
   must stop with an error, never expand to global Review All.
8. Exercise normal single-course review and global Review All. Confirm the account
   remains non-PRO and unrelated premium controls keep their original behavior.

Use only owned test emulators with `-no-window`. Drive taps and inspect UI with
ADB; capture screenshots with `adb exec-out screencap -p`. Store evidence privately,
then commit a sanitized results summary naming the APK fingerprint, patch commit,
Android version, account tier, date, scenarios, and any limitations.

If additional real due material must be prepared, use normal study operations and
wait for it to become due. Do not fabricate server success or modify production
scheduling to make a test pass. Deterministic branch tests supplement live review;
they are not a substitute for the authenticated queue and persistence tests.
