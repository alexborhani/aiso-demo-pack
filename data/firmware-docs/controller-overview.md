---
type: docs
title: MW-300 controller overview
tags: ["controller", "architecture"]
---
The MW-300 controller runs a PID flow loop (src/controller/pid.c) every 50 milliseconds, with anti-windup when the drive saturates, and unit conversions in src/controller/units.c. The safety layer (firmware/safety) evaluates the guard interlock and the over-pressure trip before every drive update and can latch the pump off; it is owned by Safety Engineering, and any change to it needs their safety change review before merge. The controls team owns the rest of the repository. Code is C99 with no dynamic allocation in the controller or the firmware.
