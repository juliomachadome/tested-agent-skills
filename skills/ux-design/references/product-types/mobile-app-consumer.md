# Mobile app (consumer)

## Key jobs
A person does a small task in a short, interrupted session, often one-handed, on a changing network, and returns later because it was easy. Notifications and permissions are earned, not assumed.

## Critical flows
First launch and onboarding; sign-in (passkeys, social, magic link); core task in 3 taps or fewer where possible; permissions in context; notifications and their settings; offline and poor network; account, privacy and deletion; rating prompts.

## Typical pitfalls
- Permission prompts at launch before value (NN/g permission requests); a denied permission with no path forward.
- Targets under 44 pt (Apple) or 48 dp (Material) (both pages read this pass); primary actions at the top beyond thumb reach.
- Wrong keyboard types, covered fields, no autofill, passwords blocked from managers.
- Gesture-only actions with no visible alternative; icon-only tabs; mixing iOS and Android idioms on one screen.
- Tours that explain what the screen already shows; sign-up wall before any value.
- State lost on interruption; no empty or offline state; spinners over 10 s with no progress or cancel.
- Notification overload (NN/g push mistakes).
- Rating prompts at the wrong moment (right after an error or in the first session).
- Account deletion buried or missing, although stores and privacy law expect it.

## Metrics
Day-1 and day-7 retention; time to first value; permission grant rate by prompt context; opt-out and mute rate per notification category; crash-free sessions; task success on a real device; store rating themes. Funnels and cohorts in `growth-analytics`.

## Checklist
- [ ] Core task reachable with one hand; primary action in the lower half.
- [ ] Permission asked at the moment of need, one line why, graceful decline.
- [ ] Keyboard types, autofill, and a visible label per field.
- [ ] Offline, slow, and interrupted states designed; drafts saved.
- [ ] Notification categories with per-category off and quiet hours.
- [ ] Dynamic type, VoiceOver and TalkBack labels, reduced motion, 200% text without clipping.
- [ ] Platform conventions kept (back, share sheet); test on real devices.

## Worked check
One-hand test: hold the phone in the right hand only, thumb reach on a 6.1-inch screen, and attempt the three core tasks; log every control you cannot reach without shifting grip and every tap that lands wrong. Repeat in bright light and with a slow network.

## Sources
Apple HIG accessibility page (44x44 pt, read via browser pass); Material 3 accessibility designing page (48x48 dp, about 9 mm, read via browser pass); NN/g touch targets (1 cm), mobile permission requests, push notification mistakes, mobile UX; Baymard mobile form findings; WCAG 2.5.8, 2.5.7.
