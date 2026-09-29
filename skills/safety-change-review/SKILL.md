---
name: safety-change-review
description: Review a change or pull request to the MW-300 safety firmware (firmware/safety — the guard interlock and the over-pressure trip) before it is merged. Use when someone asks to review, check or approve a change, branch or pull request that touches firmware/safety, the over-pressure trip or its threshold, the guard debounce or the service override.
inputs:
  change:
    type: string
    required: true
    description: the branch, pull request or commit to review
done:
  - Every changed line under firmware/safety is listed with a finding or "no finding"
  - Any change to a threshold, the debounce or the override is named as needing Safety Engineering sign-off (SE-REV)
  - The reviewer is told whether the change can merge without SE-REV
---
# Safety change review

Review change $ARGUMENTS against references/checklist.md.

1. List the files the change touches under firmware/safety. If it touches none, say so and stop: this review does not apply.
2. For each changed line, check it against every item in the checklist and give a finding or "no finding".
3. Say plainly whether the change needs Safety Engineering sign-off (SE-REV) before merge. Any change to a threshold, the debounce, the latch or the override does.
4. Do not paste firmware/safety code into a cloud model: AI Stackops refuses it. Review it on the project's local model.
