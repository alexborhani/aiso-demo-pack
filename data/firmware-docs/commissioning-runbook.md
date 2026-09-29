---
type: runbook
title: MW-300 commissioning and trip recovery runbook
tags: ["runbook", "commissioning", "trip"]
---
Commissioning an MW-300: confirm the guard switches read closed, run the pump at 30 percent for ten minutes, then step to the site setpoint. A pump that shows TRIPPED has latched on over-pressure or an open guard; it never clears itself. To recover: close and check every guard, confirm the line pressure is below the warning level, then press RESET on the panel. If it trips again within an hour, stop and raise a safety ticket with Safety Engineering; do not use the service override to keep it running. The override code and the trip thresholds live in firmware/safety and are not given out in this runbook.
