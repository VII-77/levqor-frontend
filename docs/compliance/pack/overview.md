# Levqor Compliance Pack v1.0 – Overview

**Version:** 1.0  
**Date:** 14 November 2025  
**Owner:** Data Protection Officer (privacy@levqor.ai)  
**Review Cycle:** Every 12 months or upon major feature changes  

---

## Executive Summary

Levqor is a B2B SaaS automation platform committed to UK GDPR compliance and data protection best practices. This Compliance Pack v1.0 provides a unified view of our data protection posture, including:

- **ROPA** (Record of Processing Activities) – Article 30 compliance
- **DPIA** (Data Protection Impact Assessment) – High-risk processing assessment
- **LIA** (Legitimate Interest Assessment) – Balancing test for non-consent processing

---

## Purpose of This Pack

This Compliance Pack serves as:

1. **Internal Reference** – Single source of truth for data protection practices
2. **Audit Readiness** – Structured documentation for regulatory audits (ICO)
3. **Risk Management** – Ongoing identification and mitigation of data protection risks
4. **Governance** – Annual review cycle to ensure continuous compliance

---

## GDPR Posture Summary

### Legal Basis for Processing

Levqor processes personal data under the following legal bases:

| Processing Activity | Legal Basis | Reference |
|---------------------|-------------|-----------|
| Account management | Contract (GDPR Art. 6(1)(b)) | ROPA Section 1 |
| Workflow automation | Contract (GDPR Art. 6(1)(b)) | ROPA Section 2 |
| Billing & payments | Contract + Legal obligation | ROPA Section 3 |
| Marketing communications | Consent (GDPR Art. 6(1)(a)) | ROPA Section 4 |
| Security & fraud prevention | Legitimate interest (GDPR Art. 6(1)(f)) | LIA |
| Platform analytics | Legitimate interest (GDPR Art. 6(1)(f)) | LIA |

### Data Subject Rights

Levqor supports all GDPR rights:

- ✅ Right of access (Art. 15) – Automated DSAR export system
- ✅ Right to rectification (Art. 16) – Self-service account settings
- ✅ Right to erasure (Art. 17) – One-click data deletion
- ✅ Right to restriction (Art. 18) – Account suspension on request
- ✅ Right to data portability (Art. 20) – JSON export format
- ✅ Right to object (Art. 21) – Marketing unsubscribe
- ✅ Rights related to automated decision-making (Art. 22) – High-risk prohibition

---

## Risk Classification

### Risk Matrix

| Risk Level | Impact | Likelihood | Examples |
|------------|--------|------------|----------|
| **High** | Significant harm to data subjects | Probable | Special category data processing, large-scale profiling |
| **Medium** | Moderate harm | Possible | Routine workflow automation, standard analytics |
| **Low** | Minimal harm | Unlikely | Aggregated metrics, anonymized reporting |

### Levqor's Risk Profile

**Current Risk Level:** **MEDIUM**

**Rationale:**
- ✅ No special category data (GDPR Art. 9) processed – **HIGH-RISK PROHIBITED**
- ✅ No large-scale profiling or automated decision-making – **HIGH-RISK PROHIBITED**
- ⚠️ Customer workflows may process personal data at scale – **MEDIUM RISK**
- ✅ Technical controls in place (encryption, access control, retention policies) – **RISK MITIGATED**

**High-Risk Prohibitions:**
Levqor explicitly prohibits workflows involving:
- Medical or healthcare data/decisions
- Legal advice or document generation
- Financial advice, credit scoring, or trading
- Safety-critical systems
- Special category data (race, religion, health, biometrics, sexual orientation)

These prohibitions are enforced via automated keyword scanning at the API level. See [DPIA](../dpia-levqor-automation.md) for full risk assessment.

---

## Subprocessors & International Transfers

Levqor relies on trusted subprocessors, all compliant with UK GDPR:

| Subprocessor | Purpose | Location | Safeguards |
|--------------|---------|----------|------------|
| **Stripe** | Payment processing | US | SCCs, PCI DSS |
| **Vercel** | Frontend hosting | US/EU | SCCs, encryption |
| **Replit** | Backend infrastructure | US | SCCs, ISO 27001 |
| **Resend** | Email delivery | US/EU | SCCs |
| **Sentry** | Error monitoring | US | SCCs, data minimization |
| **Notion** | Operations logging | US | SCCs |

**International Transfer Mechanism:**  
Standard Contractual Clauses (SCCs) per GDPR Chapter V, with supplementary measures (encryption, access controls).

---

## Data Minimization & Retention

Levqor adheres to data minimization principles:

| Data Type | Retention Period | Justification |
|-----------|------------------|---------------|
| API usage logs | 90 days | Security & debugging |
| Status snapshots | 30 days | System monitoring |
| DSAR exports | 30 days | Compliance delivery |
| Referral data | 2 years | Attribution tracking |
| Billing records | 7 years | **UK tax law requirement** |
| Marketing consents | Until revoked + 2 years | Proof of consent withdrawal |

**Automated Cleanup:** Daily retention job runs at 3:00 AM UTC via APScheduler.

See [retention/config.py](../../retention/config.py) for technical implementation.

---

## Technical & Organizational Controls

For a comprehensive list of security and data protection controls, see:

📋 **[Technical & Organizational Controls](./controls.md)**

Key highlights:
- 🔒 Encryption at rest and in transit (TLS 1.2+)
- 🔑 Zero-downtime API key rotation
- 🚨 Rate limiting (20 req/min per IP, 200 global)
- 🛡️ High-risk data firewall (automatic blocking)
- 📊 Comprehensive audit logging
- 🗑️ Automated data deletion (GDPR Art. 17)

---

## Document Register

For the full compliance document registry, including review schedules and ownership, see:

📚 **[Compliance Register](./register.md)**

---

## Review & Maintenance

**Review Schedule:**  
- **Annual Review:** Every 12 months (Next: November 2026)
- **Trigger Review:** Major feature launches, new subprocessors, regulatory changes

**Ownership:**  
Data Protection Officer – privacy@levqor.ai

**Approval:**  
Founder / CEO

---

## Related Documents

- [ROPA (Record of Processing Activities)](../ropa.md)
- [DPIA (Data Protection Impact Assessment)](../dpia-levqor-automation.md)
- [LIA (Legitimate Interest Assessment)](../lia-marketing-and-analytics.md)
- [Technical & Organizational Controls](./controls.md)
- [Compliance Register](./register.md)

---

**Compliance Pack v1.0** – Levqor is committed to data protection excellence.
