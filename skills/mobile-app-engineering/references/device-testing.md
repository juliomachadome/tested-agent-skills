# Device testing: what to check before calling it done

A mobile change is done when it was seen working on the conditions real people have, not when it ran on one simulator. Use this list before any "ready", scaled to the change: a copy fix needs two rows, a new flow needs all of them. Project rules (device matrix, QA checklist, release gate) come first. Release-gate verdicts and test strategy belong to `qa-verification`; this file is the device side.

## Contents
1. The matrix
2. Conditions to check
3. Simulator or real device
4. How to run it cheaply
5. Report format

## 1. The matrix
At least one of each, on a release-like build (preview or production profile, not the dev client) **[C]**:
- **iOS and Android.** The oldest OS version you support and the newest.
- **Small and large screen.** A small phone (iPhone SE class, about 375 pt wide; a compact Android) and a large one or a tablet if the app supports it; landscape only if it is enabled.
- **A mid-range or low-end Android.** Most performance and memory problems show only here (see `performance.md`).

## 2. Conditions to check
| Condition | How | What breaks |
|---|---|---|
| Dark theme (only if the app supports it or the brief asks; if unclear, ask) | switch the system appearance while the screen is open; if the app is light-only, confirm it stays light and readable | hard-coded colours, unreadable text, icons and images that vanish, status bar style, splash and keyboard colours |
| Large system font | iOS Larger Text at the largest accessibility size; Android font size and display size at max | clipped labels, buttons pushed off screen, fixed-height rows, truncated prices |
| No network and slow network | airplane mode; network link conditioner (iOS) or emulator network throttling; flaky Wi-Fi | infinite spinners, lost writes, error with no retry, duplicate submits on reconnect (see `offline-sync.md`) |
| Permission denied | deny camera, location, notifications, photos at the prompt and later in Settings | crash or dead screen; there must be an explanation and a path to Settings |
| Killed in background and reopened | open a flow, background the app, kill it (or let the OS reclaim memory), reopen; also from a push or deep link | lost form input, wrong screen restored, stale auth, duplicated navigation stack |
| Keyboard over a field | focus the lowest field on the small phone, both platforms | field hidden behind keyboard, submit button unreachable, no way to dismiss |
| Safe areas | notch, Dynamic Island, home indicator, Android gesture bar and edge-to-edge, landscape if enabled | content under the status bar or home indicator, tappable areas in gesture zones |
| Screen reader | VoiceOver and TalkBack through the changed flow | unlabeled buttons, wrong reading order, focus lost after navigation, state not announced |
| Reduced motion | iOS Reduce Motion, Android Remove animations | loops still running, essential state shown only by motion (see `motion.md`) |
| Interruptions | incoming call, notification banner, switching apps mid-upload, low battery mode | lost progress, audio not ducking, uploads restarting from zero |
| Locale | longest language the app ships, right-to-left if supported, date, number and currency formats | overflow, mirrored icons that should not mirror, wrong formats |

## 3. Simulator or real device
Simulator and emulator are enough for: layout at many screen sizes, themes, font scaling, locales, most navigation and form logic, deep links via command line, permission dialogs (most), reduced motion and screen reader basics.

Only a real device shows reliably **[C]**:
- **Push notifications.** The iOS simulator only takes simulated payloads; real delivery, tokens and background behaviour need a device and a release-like build.
- **Camera, microphone, Bluetooth, NFC, biometrics and sensors.**
- **Performance and memory.** A simulator runs on desktop CPU and RAM; frame drops, startup time and memory kills must be measured on a mid-range Android in release mode.
- **Haptics and audio routing** (silent switch, Bluetooth headphones, speaker).
- **In-app purchases end to end** (sandbox or test track accounts).
- **Battery, thermal and real network handoff** (Wi-Fi to cellular).

## 4. How to run it cheaply
- Change one condition at a time and keep the same screen open.
- Automate the stable paths (Maestro or Detox flows on release builds) and check the conditions above by hand for the changed screens only.
- Take a screenshot per condition and platform; name files by screen, platform, condition.
- Cloud device farms help with breadth (OS versions, makers) but not with push, haptics or felt performance.

## 5. Report format
Always state what was checked and what was not:

| Condition | iOS (device/OS) | Android (device/OS) | Result |
|---|---|---|---|
| Dark theme | iPhone 13, iOS 26, simulator | Pixel 6a, Android 16, device | ok / bug #… |
| Largest font | … | … | … |
| Push | not checked (no device) | … | not verified |

End with: build type and version used, what could not be verified and why, and the next check to run.
