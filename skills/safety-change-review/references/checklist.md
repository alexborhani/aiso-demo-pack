# Safety change checklist (MW-300, Safety Engineering)

- The trip stays latched: nothing but `safety_manual_reset()` may leave STATE_TRIPPED.
- The trip threshold (TRIP_PRESSURE_KPA) and the warning threshold only move with an SE-REV record.
- The guard debounce (GUARD_DEBOUNCE_MS) never goes above 50 ms.
- The service override needs both the key switch in SERVICE and the override code; neither alone.
- No dynamic allocation, no floating point in firmware/safety.
- A change here needs a unit test in the same pull request.
