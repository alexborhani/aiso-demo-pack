---
type: api-spec
title: MW-300 service API guide
tags: ["service-api", "mw-300"]
---
The MW-300 service API (repository meridian-pump-controller, folder service-api, version 1.4.0) gives the service desk and field engineers a pump's state without a site visit. It is read-only by decision (ADR 0001): setpoints change only on the controller's own panel with the key switch in SERVICE. One endpoint: GET /v1/pumps/{serial} returns the site, flow in litres per minute, pressure in bar, state (RUN, DERATED or TRIPPED) and running hours; an unknown serial answers 404. The contract is openapi/service-api.yaml in the repository. The service platform team owns it; requests for new fields go to them through the service-platform queue, never directly to the firmware team.
