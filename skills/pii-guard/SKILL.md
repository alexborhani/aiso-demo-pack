---
name: pii-guard
description: PII and OWASP security filtering rules. Use when an answer could include personal data or credentials, or when text from a person reaches a tool.
---

# PII Guard

## Sensitive Data Categories (NEVER include in responses)

- SSN, tax IDs, government identifiers
- Salary, compensation, financial data
- Home addresses, personal phone numbers
- Dates of birth, ages
- Full email addresses (mask as j***@company.com)
- Medical, legal, or disciplinary records

## Behavior

- **Default:** silently omit PII from responses — don't announce filtering
- **Explicit request:** decline politely citing company data policy
- **User provides PII:** refuse to process, store, or format it
- **Partial info OK:** name, title, department, general location, hire year
