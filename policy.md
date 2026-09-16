# Meridian Works — Data Classification and Handling Policy

**Document owner:** Chief Information Officer · **Version:** 2.1 · **Status:** in force for evaluation

> This policy belongs to Meridian Works, a fictional company. It ships with the AI Stackops demo pack so the platform's classification, clearance and handling controls can be evaluated end to end. Nothing in it describes a real organisation.

## 1. Purpose and scope

This policy establishes how information created, received or processed by Meridian Works is classified, labelled, handled and retained. It applies to every employee, contractor and system, including the AI Stackops platform and every agent, knowledge store and model configured on it. It follows the structure of ISO/IEC 27001 controls A.5.12 (classification of information) and A.5.13 (labelling of information).

## 2. Classification levels

Information is classified at one of four levels, ordered from least to most sensitive.

| Level | Meaning | Examples |
| --- | --- | --- |
| Public | Published, or safe to publish, with no harm on disclosure | Employee handbook, product pages, press releases |
| Internal | Operating information for staff; disclosure would be inconvenient, not harmful | IT runbooks, procedures, plans without figures |
| Confidential | Disclosure would harm a person, a customer or the company | Personnel files, compensation, unreleased financial results, customer contracts |
| Restricted | Disclosure would cause serious harm or legal exposure | Legal matters, security incidents, credentials, regulator correspondence |

Information that carries no classification is treated as **Internal**.

## 3. Categories

Independently of its level, information may carry one or more categories that mark the kind of harm disclosure would cause and who may hold it: **HR** (identifiable employees), **Finance** (ledgers, forecasts, close packages, pricing), **Legal** (matters, counsel's advice, regulator correspondence) and **Security** (incidents, vulnerabilities, credentials). A person may read information in a category only if their clearance names that category.

## 4. Clearances

Every person holds a clearance: a highest level and a set of categories. Staff hold the Staff role, which clears Internal; the member tier itself clears Public only, so contractors and anyone without a role read public information alone. Named roles extend that: People Partners clear Confidential within HR, Finance Analysts clear Confidential within Finance, and administrators clear Restricted in every category. Contractors clear Public only. Clearances are granted by the role's owner and reviewed quarterly.

## 5. Handling rules

- **Confidential** information is stored only in systems that restrict access to named roles, is never sent to a public model or service, and is retained for seven years after the end of the relationship it concerns.
- **Restricted** information is stored only in systems administrators control, is processed by models running on Meridian Works equipment, is never shared outside the company without counsel's approval, and is retained for ten years.
- **Internal** information may be shared with any member of staff and with contractors under agreement.
- **Public** information may be published without review.

## 6. Labelling and automated classification

New documents are classified when they arrive. Where the platform's classifier decides, a decision below the confidence threshold is queued for a person to confirm. A person may raise a classification at any time; lowering one requires review by the information owner.

## 7. Roles and responsibilities

The Chief Information Officer owns this policy. Information owners classify what they produce and review clearances for their categories. Administrators configure systems so that handling rules are enforced, and run the compliance check monthly. Every person reports suspected mishandling to the Security Lead.

## 8. Review

This policy is reviewed annually and whenever a regulator, customer or incident requires it.
