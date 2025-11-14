# Compliance Document Register

**Version:** 1.0  
**Date:** 14 November 2025  
**Owner:** Data Protection Officer (privacy@levqor.ai)  
**Part of:** [Compliance Pack v1.0](./overview.md)

---

## Purpose

This register provides a centralized index of all Levqor compliance documentation, including review schedules, ownership, and version control.

---

## Document Inventory

### Core Compliance Documents

| Document | Type | Version | Last Updated | Next Review | Owner | Status |
|----------|------|---------|--------------|-------------|-------|--------|
| [ROPA](../ropa.md) | Record of Processing Activities | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |
| [DPIA](../dpia-levqor-automation.md) | Data Protection Impact Assessment | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |
| [LIA](../lia-marketing-and-analytics.md) | Legitimate Interest Assessment | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |

### Compliance Pack Documents

| Document | Type | Version | Last Updated | Next Review | Owner | Status |
|----------|------|---------|--------------|-------------|-------|--------|
| [Overview](./overview.md) | Executive Summary | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |
| [Controls](./controls.md) | Technical & Organizational Measures | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |
| **Register** | Document Registry | 1.0 | 14 Nov 2025 | 14 Nov 2026 | DPO | ✅ Current |

### Supporting Documentation

| Document | Purpose | Last Updated | Location |
|----------|---------|--------------|----------|
| Privacy Policy | Customer-facing legal document | Dynamic | [/privacy](/privacy) |
| Terms of Service | Customer-facing legal document | Dynamic | [/terms](/terms) |
| Cookie Policy | PECR compliance | Dynamic | [/cookies](/cookies) |
| Acceptable Use Policy | User conduct rules | Dynamic | [/acceptable-use](/acceptable-use) |
| Risk Disclosure | High-risk prohibition notice | Dynamic | [/risk-disclosure](/risk-disclosure) |
| Data Requests Guide | DSAR procedure | Dynamic | [/data-requests](/data-requests) |
| GDPR Overview | Customer-facing summary | Dynamic | [/gdpr](/gdpr) |
| DPA Template | Data Processing Agreement | Static | [/dpa](/dpa) |
| Subprocessor List | Third-party processors | Dynamic | [/subprocessors](/subprocessors) |

### Operational Procedures

| Procedure | Purpose | Last Updated | Location |
|-----------|---------|--------------|----------|
| Incident Response | Security breach procedure | Dynamic | [/incident-response](/incident-response) |
| Business Continuity | Disaster recovery | Dynamic | [/business-continuity](/business-continuity) |
| Backup & Restore | Data recovery procedure | Dynamic | [/backups](/backups) |
| API Key Rotation | Zero-downtime key rotation | Static | API_KEY_ROTATION.md |
| DSAR Export System | Automated data export | Static | DSAR_IMPLEMENTATION_SUMMARY.md |

---

## Review Schedule

### Annual Review (Every 12 Months)

**Next Scheduled Review:** 14 November 2026

**Review Checklist:**
1. ✅ Verify ROPA accurately reflects current processing activities
2. ✅ Update DPIA with new risks or mitigation measures
3. ✅ Confirm LIA balancing test remains valid
4. ✅ Review subprocessor list and DPAs
5. ✅ Audit retention policies and automated cleanup
6. ✅ Test incident response procedures
7. ✅ Verify staff training completion
8. ✅ Check for regulatory changes (UK GDPR, ICO guidance)
9. ✅ Update version numbers and review dates
10. ✅ Obtain management sign-off

### Triggered Reviews

In addition to annual reviews, documentation must be updated when:

| Trigger Event | Documents to Update | Timeline |
|---------------|---------------------|----------|
| **New processing activity** | ROPA, possibly DPIA | Within 30 days |
| **New subprocessor** | ROPA, Subprocessor List, Customer Notice | 30 days advance notice |
| **High-risk feature launch** | DPIA, LIA (if applicable), Controls | Before launch |
| **Data breach or incident** | Incident Response log, Controls (if gaps identified) | Immediately + 30 days post-incident |
| **Regulatory change** | All affected documents | Within 90 days of change |
| **Change in legal basis** | ROPA, possibly LIA | Within 30 days |
| **Retention policy change** | ROPA, Controls, Privacy Policy | Before implementation |

---

## Ownership & Approval

### Document Ownership

**Primary Owner:**  
Data Protection Officer (DPO) – privacy@levqor.ai

**Responsibilities:**
- Maintain accuracy and currency of all compliance documents
- Coordinate annual and triggered reviews
- Ensure version control and change tracking
- Escalate compliance risks to management
- Liaise with ICO if required

**Backup Owner:**  
Founder / CEO

### Approval Authority

| Document Type | Approval Required | Approver |
|---------------|-------------------|----------|
| ROPA, DPIA, LIA | Management sign-off | Founder / CEO |
| Privacy Policy, Terms | Legal review + management | Founder / CEO |
| Technical Controls | Technical review + DPO | DPO |
| Operational Procedures | DPO review | DPO |

---

## Version Control

### Current Versions

All documents in this register are at **Version 1.0** as of 14 November 2025.

### Change Log

| Date | Document | Change | Updated By |
|------|----------|--------|------------|
| 14 Nov 2025 | All | Initial Compliance Pack v1.0 created | DPO |

### Future Changes

All changes to compliance documents must be:
1. **Logged** in this register
2. **Version-controlled** with date and author
3. **Reviewed** by DPO
4. **Approved** per approval matrix above
5. **Communicated** to relevant stakeholders

---

## Access & Confidentiality

### Internal Use Only

All documents in this register are **INTERNAL** and must not be shared externally without explicit approval from DPO or Founder/CEO.

**Exceptions:**
- Customer-facing legal documents (Privacy Policy, Terms, etc.) are public
- DPA and subprocessor list shared with customers on request
- ROPA, DPIA, LIA shared with regulatory authorities (ICO) on request

### Access Control

| Role | Access Level | Documents |
|------|--------------|-----------|
| **DPO** | Full access (read/write) | All |
| **Founder/CEO** | Full access (read/write) | All |
| **Engineering Team** | Read-only | Technical Controls, Operational Procedures |
| **Support Team** | Read-only | Privacy Policy, Data Requests Guide |
| **External Auditors** | Read-only (on demand) | ROPA, DPIA, LIA, Controls |
| **ICO (on request)** | Read-only | ROPA, DPIA, LIA, Privacy Policy |

---

## Related Resources

### External Guidance

- [ICO Guide to GDPR](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [ICO Accountability Framework](https://ico.org.uk/for-organisations/accountability-framework/)
- [ICO DPIA Guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/)
- [EDPB Guidelines on Legitimate Interest](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-22019-processing-personal-data-under-article-6_en)

### Internal Resources

- [Compliance Pack Overview](./overview.md)
- [Technical & Organizational Controls](./controls.md)
- [Retention Configuration](../../retention/config.py)
- [Automated Cleanup Engine](../../retention/cleanup.py)

---

## Contact

**Data Protection Officer**  
Email: privacy@levqor.ai  
Available: Monday–Friday, 9am–5pm GMT

For urgent data protection matters outside business hours, contact: founder@levqor.ai

---

**Compliance Register v1.0** – Levqor's commitment to data protection excellence.
