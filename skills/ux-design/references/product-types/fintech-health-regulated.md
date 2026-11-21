# Fintech, health and other regulated products

## Key jobs
A person manages money or health data and understands what is happening, what it costs and what they agreed to, with no surprise. The business meets legal duties without turning the product into a wall of text.

## Critical flows
Onboarding with identity checks (KYC); consent and data sharing; money movement (payments, transfers, trading, claims); statements and fees; alerts and 2FA; error and fraud recovery; support and complaints; account closure and data export.

## Typical pitfalls
- Consent bundled and pre-ticked; legal text where a plain summary should be; consent that is hard to withdraw.
- Fees and risks shown late or in low contrast; claims without evidence.
- Irreversible actions (send, trade, submit) without a clear preview and a named effect; no undo where the law allows one.
- Authentication that requires memory tests or pasting blocked (WCAG 3.3.8, 3.3.7).
- Timeouts that lose a long form; errors that blame the user; error codes only.
- Security theatre: friction on low-risk steps, none on risky ones.
- Health: alarming wording on results, no route to a human, color-only status, content tuned to a "typical" user.

## Metrics
KYC completion and time; failure reasons; transaction completion and error rate; support contact per 1,000 transactions; complaint themes; 2FA failure and recovery rate; consent opt-in by purpose (opt-in rate near 100% from a pre-ticked box is a warning). Never run engagement-boosting tests on consent or risk disclosures.

## Checklist
- [ ] Plain summary of fees, risks and what the person agrees to, with the full text one step away.
- [ ] Consent per purpose, unticked, withdrawable as easily as given, stored with time.
- [ ] Preview then confirm for money movement; confirmation names amount, recipient, timing, fees.
- [ ] Error messages say what happened and the safe next step; no loss of entered data.
- [ ] Accessible authentication; no cognitive test as the only route; session timeouts warn.
- [ ] A human route (phone, chat, complaint) is visible.
- [ ] Review with the legal owner; this skill does not rule on compliance.

## Worked check
Read the consent screen aloud as a person with 30 seconds: can they say what they agree to, to whom, and how to withdraw? If not, rewrite the summary before touching the legal text.

## Sources
WCAG 2.2 (3.3.7, 3.3.8, 2.2.1, 3.3.4 reviewed in other references); NN/g confirmation dialogs, user mistakes and slips, error guidelines; Gray et al. 2018; Mathur et al. 2019; Norman (forcing functions); consumer-law and data-protection texts are for the relevant legal skills and counsel, not read for this variant.
