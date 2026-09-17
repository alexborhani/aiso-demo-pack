---
type: scenario
title: "14. A support page for people outside the building"
tags: ["scenario-14"]
---
*The same governed platform, published to customers, with limits and without any of the internal data.*

**You are** nobody: a third window with no Studio session. Agent: `support` over `product-faq`.

1. Open `/chat/support`. It asks for the page password (`meridian-customer`, standing in for a
   customer-portal login). Say: published pages have their own authentication, separate from staff
   accounts.
2. Ask: **"How often should an MW-300 be serviced?"** Answered from the product FAQ with the
   intervals. **"My pump is two years old and leaking at the seal, is that under warranty?"** The
   warranty terms, and the service desk contact.
3. Ask something internal: **"What happened with the USB incident at the Halden plant?"** The page
   has one store, the FAQ; it says it cannot help and gives the service desk.
4. As Dana, Admin → Policy → Limits: the *Anonymous* row caps published pages per IP address. Set
   requests per minute to 2, then ask three questions quickly from the customer window: the third is
   refused with a retry time. Admin → Audit: `limits.exceeded` for the anonymous scope. Set it back.

**Land:** one platform serves customers and staff with the same controls: a published page can only
reach the store it was given, and it is rate-limited like any other caller.

---
