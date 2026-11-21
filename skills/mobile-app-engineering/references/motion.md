# Motion, gestures, haptics and sound (Expo and React Native)

The native counterpart of the web `web-motion` method. Motion shows change or confirms an action; the screen must work standing still first. Which feedback to give is `ux-design`'s call, how it looks (durations, easing tokens) is `ui-design`'s; this file is how it moves on iOS and Android. Project motion tokens win over every number here.

When the official Expo plugin is installed (`expo@claude-plugins-official`), its `expo-animation` skill holds the implementation detail (spring and easing tables, recipes, keyboard and sheet patterns) and `expo-upgrade` holds migrations. Use them for code; this file is the method and the checks. Versions and API names read 20/11/2026: `BIBLIOGRAPHY.md`, entries 45 onward.

## 1. Should it animate at all
- Things done many times a day (tab switches, keyboard, toggles in settings, scrolling) get the platform default or nothing. Tabs never slide.
- Press feedback and list navigation: barely visible, under about 150 ms, or nothing.
- Sheets, modals, toasts, onboarding steps: standard motion. Celebration only for rare moments.
- Name the purpose in one word (feedback, spatial continuity, state, explanation). No purpose, no animation.

## 2. Tool selector (cheapest that works; climb only on the signal)
1. **Platform and navigator first.** Native stack transitions, `formSheet` sheets, native tabs, `RefreshControl`, native menus. Never hand-roll screen transitions.
2. **Reanimated CSS transitions and keyframes** (`transitionProperty`, `animationName` in the style) for state-driven changes with no finger: press, toggle, colour, a value flipping. In a project without Reanimated, core `Animated` with `useNativeDriver: true` (transform and opacity only) or `LayoutAnimation` (opacity and scale only, not interruptible; on by default in the New Architecture) do the same small jobs.
3. **Layout animations** (`entering`, `exiting`, list item layout) for mount, unmount and reflow.
4. **Shared values + Gesture Handler + `useAnimatedStyle`** when a finger drives it or it follows scroll: drag, swipe, interruptible springs. Runs on the UI thread, so it stays smooth while JS works. Reanimated 4 and Gesture Handler 3 need the New Architecture (required since Expo SDK 55).
5. **Lottie or Rive** for designer-made illustration (empty states, celebration); Rive when it reacts to state or input. Never for core UI state. Check file weight and stop loops.
6. **Skia** for custom drawing and very large animated scenes, when the view hierarchy itself is the bottleneck.
Install animation packages with `npx expo install` so versions match the SDK.

## 3. Touch feedback and states
- Pressed state visible within 100 ms of touch down, never after the network reply.
- Idle, pressed, loading, success, error without layout jump: fixed button size, spinner inside the same box, space for the error reserved or faded in.
- Block double submit; keep input on error; announce the result to VoiceOver and TalkBack.
- Skeletons for content arriving in place; images with a same-size placeholder and a short fade (`expo-image` `placeholder`, `transition`).
- Animate `transform` and `opacity`; heights measured with `onLayout`, never hard-coded (system font scaling changes them).
- Every state works with motion, haptics and sound off: text plus icon carry it.

## 4. Gestures
- Every gesture is cancelable: dragging back returns to the start; reset state in the gesture's finalize callback, which runs even when activation fails (Gesture Handler 3 marks interruptions as `canceled`).
- Every gesture has a visible button alternative (swipe to delete also has Delete; a sheet has a close button). Needed for screen readers and motor access.
- If a finger was involved, settle with a spring that carries the release velocity; otherwise timing.
- Thresholds so a horizontal swipe does not fight vertical scroll; system back gestures keep working.
- Never make people wait for an animation to finish before they can act again; any running animation can be interrupted (Apple HIG).

## 5. Haptics: confirmation or error only
- Custom haptics only for the outcome of a meaningful action: success or error. System controls (switches, pickers, sliders) already play their own haptics; do not add more on top.
- `expo-haptics`: `notificationAsync(Success | Error)`; on Android prefer `performAndroidHapticsAsync(AndroidHaptics.Confirm | Reject)`, which uses system haptic constants.
- Use each system pattern only for its documented meaning, and the same pattern always for the same meaning (Apple HIG; Android haptics principles).
- One haptic per user action, in the same frame as the visual and matching its strength; never on scroll, entrance animations or every tap.
- Optional and never the only feedback: an in-app switch to turn haptics off; iOS also skips them in Low Power Mode, with the camera running and during dictation.

## 6. Sound: only when asked
- Never on launch; only after a user action; short, quiet, with a remembered in-app mute.
- Respect the silent switch: `expo-audio` `setAudioModeAsync({ playsInSilentMode: false })` for interface sounds (the default is true), and mix with the user's audio instead of stopping it.
- Preload once (`useAudioPlayer`); never a player per tap. Use `expo-audio`, not `expo-av`.
- Never the only signal.

## 7. Reduced motion
- Reanimated animations accept `reduceMotion: ReduceMotion.System`: timing and springs jump to the end, entering animations land at the final state, exiting ones are skipped. `useReducedMotion()` reads the value at app start only; for live changes use `AccessibilityInfo.reduceMotionChanged`.
- Reduced means fewer and gentler, not zero: keep opacity and colour changes that explain state; drop translation, scale, parallax and overshoot; screen transitions become fades; Lottie and Rive show a static frame.

## 8. Style and platform idiom
- Sober by default: short distances, opacity plus small translate or scale from about 0.95 (never from 0), no visible bounce unless a flick carried momentum. No confetti or glow unless the brief asks.
- iOS follows Apple HIG: motion with a purpose, brief and precise feedback, little or no custom motion on frequent interactions, motion always optional.
- Android follows Material 3, which since May 2025 (M3 Expressive) drives motion with springs instead of easing and duration (the old easing tables are kept only for transitions and no longer maintained). Two schemes: expressive (spatial springs overshoot and bounce) and standard (minimal bounce, for utilitarian products). The sober default here means the standard scheme; expressive only when the brand asks. Colour and opacity use effects springs, which never overshoot.
- Do not mix idioms on one platform.

## 9. Before calling it done
- [ ] Felt on a release build on the slowest supported Android and an iPhone, not Expo Go or a simulator (see `performance.md`).
- [ ] Interrupt, reverse and flick every gesture; button path works.
- [ ] Reduce Motion (iOS) and Remove animations (Android) on: state complete, nothing loops.
- [ ] App usable with haptics and sound off.
- [ ] Device conditions per `device-testing.md`; report what was and was not checked.
