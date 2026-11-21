# Mobile app security (iOS, Android, Expo and React Native)

Format: **rule** · source (B# = `BIBLIOGRAPHY.md`). Tags: **[C]** standard or vendor doc, **[M]** single or dated source, **[F]** practitioner judgment. Frame: the binary and the phone belong to the user, so anything on the device can be read, replayed or modified; the server is the only trusted place. OWASP MASVS (v2.1.0 latest seen, B53) has eight areas: storage, crypto, auth, network, platform, code, resilience, privacy. Control texts were not read.

## 1. Mobile threat model
Assets: user data on the device, tokens, paid entitlements, your API and its cost. Attackers: someone with the app on a rooted phone (Frida, proxy, decompiler), malware on the same phone, a thief, a hostile network, a scraper with a modified client, an abuser of trials and credits. Walk the app as each (`playbooks.md` 1) and write what each can reach; MASVS areas are a checklist, not a certification. · B53, B31, B2

## 2. Secrets in the bundle
1. **Assume everything in the binary or JS bundle is extracted.** API keys, "obfuscated" strings, `EXPO_PUBLIC_*` values, service-role keys and admin URLs are readable in minutes. · B31, B54 **[C]**
2. **Keep provider keys and business rules on your server;** the app calls your API, your API calls the provider. When a client key is unavoidable (maps, analytics), restrict it by bundle id, quota and API scope, and expect abuse. · B31 **[F]**
3. **Use short-lived tokens:** the user signs in, the server issues an access token of minutes and a rotating refresh token; on logout and password change the server revokes them. · B50 (refresh rotation), B31

## 3. Secure storage
1. **Tokens and small secrets go in the Keychain (iOS) or Keystore-backed storage (Android), via `expo-secure-store` or a native library; never `AsyncStorage`, plain files or `UserDefaults`.** AsyncStorage is unencrypted app storage, readable on a rooted device and in some backups. · B59, B58, B61 **[C]**
2. **Limits of `expo-secure-store`:** `requireAuthentication` adds biometrics or passcode but not in Expo Go; keys are invalidated when biometric enrollment changes, so treat read errors as "sign in again"; keep it out of Android auto-backup and never make it the only copy of critical data. · B59
3. **Hardware-backed keys stop extraction, not misuse** by an attacker who controls the running app. · B58
4. **Store as little as possible:** cache only what offline needs, encrypt the local database when it holds personal or health data, wipe on logout and deletion. · B31, B53

## 4. Network: TLS and pinning
1. **TLS everywhere, no cleartext exceptions in production** (iOS App Transport Security, Android network security config). · B31
2. **Certificate or key pinning is a trade-off, not a default.** It stops a user-installed CA or a rogue proxy, but a rotated certificate bricks every installed copy until users update. If you pin: pin an intermediate's public key, ship a backup pin, a kill switch and a rotation rehearsal; otherwise rely on platform trust and strong server TLS. A tester can hook the check at runtime anyway. · B53 (NETWORK area), B31 **[M]**

## 5. Deep links, universal links, intents
1. **A custom URL scheme (`myapp://`) is not owned by you:** any other app can register it and receive the link, including OAuth redirects. Use verified https links: Apple universal links (apple-app-site-association) and Android App Links (`autoVerify`, `assetlinks.json`). · B57 **[C]**
2. **Treat every deep link as untrusted input:** allowlist host, path and parameters, never run a state-changing or paid action from a link without in-app confirmation, no tokens in the link. · B31, B53 (insecure deep links and intents are named PLATFORM weaknesses)
3. **OAuth in a native app:** authorization code with PKCE in the system browser, exact redirect-URI match; no embedded WebView sign-in, no implicit grant. · B50 **[C]**
4. **Android components:** export only what must be reachable, check the caller, validate intent extras. · B53, B31 **[C]**

## 6. WebViews
Load only your own https content or an allowlist; disable file access and JavaScript bridges you do not need; validate every bridge call and never expose a bridge to remote or user-supplied pages; no tokens in URLs or `postMessage` to unknown origins; open third-party sites in the system browser. A WebView with a JavaScript interface turns XSS on a loaded page into native access. · B31, B53 **[C]**.

## 7. Reverse engineering, obfuscation, root and jailbreak detection
1. **Obfuscation, anti-debug and root/jailbreak detection raise cost; they create no secrecy.** Frida can hook or skip any client-side check. Use them after the server design is right, for logic worth the effort (licence checks, anti-cheat, fraud). · B53 (RESILIENCE area is explicitly defense in depth), B56 **[C]**
2. **A client-side check is never the only control** for money, access or personal data; a rooted-device flag is a server signal, not a gate. · B31 **[F]**
3. **Reduce what is learned:** no debug symbols or source maps in the shipped binary (upload them to the crash tool only), no debuggable release builds. · B31

## 8. Leaks through logs, screenshots, clipboard, backups
- **Logs:** tokens, headers or personal data in `console.log` reach device logs and crash reports; strip by build type. · B53 (named STORAGE weakness)
- **Screenshots and app switcher:** blur sensitive screens in the background; secure-window flag on Android. · B53, B31
- **Clipboard:** other apps can read it; do not copy secrets. · B53
- **Backups:** exclude token stores and sensitive databases from iCloud and Android Auto Backup. · B53, B59
- **Notifications and keyboard cache:** no secrets in push bodies; mark password and OTP fields. · B53

## 9. The server never trusts the client
1. **Every price, role, entitlement, quota and tenant check is server-side;** a modified client can send any request your API accepts. The web rules in `access-control-tenancy.md` and `business-logic-payments.md` apply unchanged. · B9 (API1, API3, API5, API6), B2
2. **In-app purchases:** the app sends the transaction to your server, which validates it with Apple's App Store Server API (signed data; check bundle id, product, environment, expiry, revocation) or Google Play's developer API and grants the entitlement from that state and store notifications; handle restore, refund, grace period. "Purchase succeeded" on the client is a hint only. · B62 (page needs a browser pass, details from vendor knowledge **[F]**), B31
3. **Attestation signals** (Play Integrity, Apple App Attest) help the server score abuse of free trials and credits; decode the verdict on the server, give failing devices limits rather than a hard block, never treat a pass as proof. · B60 (landing page only; verdict docs not read)
4. **Rate limit and cap cost per account** on endpoints a modified client would hammer (signup, codes, AI calls, receipts); `input-files-apis.md` 5.

## 10. Testing (own or authorised apps only)
Static: MobSF (B55) on the APK/IPA, `semgrep` on the source, dependency scan. Dynamic: an intercepting proxy on a test device, Frida (B56), and the MASTG test cases (B54) per MASVS area. Write scope and authorisation down first; never aim these tools at someone else's app or at real users' data. Report in the web format (`SKILL.md`).

## 11. Release gate for a mobile build (adds to `playbooks.md` 8)
- [ ] No secret, private key or admin URL in the built artifact (search the build, not the repo).
- [ ] Tokens only in secure store; logout and account deletion wipe local data.
- [ ] Release build not debuggable, no verbose logs, cleartext off.
- [ ] Deep links verified and parameters allowlisted; purchases validated on the server.
- [ ] Sensitive screens handle backups and screenshots; privacy label matches the SDKs.

Related: `mobile-app-engineering`.
