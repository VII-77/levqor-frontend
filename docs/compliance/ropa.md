# Record of Processing Activities (ROPA)
## Levqor Limited

**Version:** 1.0  
**Last Updated:** 14 November 2025  
**Document Owner:** Data Protection Lead  
**Jurisdiction:** United Kingdom / European Union

---

## 1. Introduction

### 1.1 About Levqor

Levqor Limited is a UK-based B2B SaaS provider offering workflow automation services to business customers. Our platform enables organisations to automate routine business processes through integrations with third-party services and APIs.

**Company Details:**
- Legal Entity: Levqor Limited
- Primary Location: United Kingdom
- Data Protection Registration: [To be completed upon ICO registration]
- Contact: privacy@levqor.ai

### 1.2 Data Controller / Processor Status

Levqor operates in dual capacity:

- **Data Controller**: For user account data, billing information, platform analytics, and marketing communications
- **Data Processor**: For customer workflow data processed on behalf of business customers

This ROPA documents both capacities in accordance with UK GDPR Article 30 and EU GDPR Article 30.

---

## 2. Record of Processing Activities

### 2.1 User Authentication & Account Management

| Field | Details |
|-------|---------|
| **Processing Activity** | User Authentication & Account Management |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | Account administrators, authorized users |
| **Data Categories** | Email address, name, authentication tokens, session data, IP addresses, user agent strings |
| **Purpose of Processing** | Provide secure access to platform, manage user sessions, enforce access controls |
| **Legal Basis** | Contractual necessity (GDPR Art. 6(1)(b)) |
| **Retention Period** | Duration of contract + 12 months for audit purposes |
| **Recipients** | Internal operations team, authentication service providers |
| **Subprocessors** | NextAuth (authentication), Replit (hosting infrastructure) |
| **International Transfers** | EEA/UK only; US subprocessors under Standard Contractual Clauses |
| **Technical Measures** | TLS 1.3 encryption in transit, bcrypt password hashing, session token rotation, rate limiting |

---

### 2.2 Billing & Payment Processing

| Field | Details |
|-------|---------|
| **Processing Activity** | Billing & Payment Processing |
| **Data Controller** | Levqor Limited (joint with Stripe for payment data) |
| **Data Subjects** | Paying customers, billing administrators |
| **Data Categories** | Name, email, billing address, payment card details (tokenized), transaction history, invoice data |
| **Purpose of Processing** | Process payments, issue invoices, manage subscriptions, fulfill tax obligations |
| **Legal Basis** | Contractual necessity (GDPR Art. 6(1)(b)), legal obligation (GDPR Art. 6(1)(c)) for tax |
| **Retention Period** | Duration of contract + 7 years (UK tax law requirement) |
| **Recipients** | Finance team, payment processor, tax authorities (if required) |
| **Subprocessors** | Stripe (payment processing), Vercel (hosting) |
| **International Transfers** | Stripe (US) under Standard Contractual Clauses + adequacy decision |
| **Technical Measures** | PCI DSS compliant tokenization (Stripe), encrypted storage, access controls, audit logging |

---

### 2.3 Workflow Execution & Automation

| Field | Details |
|-------|---------|
| **Processing Activity** | Workflow Execution & Automation |
| **Data Controller** | Customer (Levqor acts as Processor) |
| **Data Subjects** | End users of customer systems, customer employees |
| **Data Categories** | Varies by customer workflow; may include names, contact details, business data (excluding prohibited categories) |
| **Purpose of Processing** | Execute automated workflows as instructed by customer |
| **Legal Basis** | Processing on behalf of controller under written contract (GDPR Art. 28) |
| **Retention Period** | As specified in customer agreement; typically 30-90 days for workflow logs |
| **Recipients** | Customer, authorized customer personnel, third-party APIs as configured by customer |
| **Subprocessors** | OpenAI (AI processing), Make.com (workflow execution), Google Workspace (integrations), Microsoft 365 (integrations), Notion (integrations) |
| **International Transfers** | May include US subprocessors under Standard Contractual Clauses |
| **Technical Measures** | Encryption at rest (AES-256), encryption in transit (TLS 1.3), role-based access control, workflow isolation, audit logging |

---

### 2.4 Platform Monitoring & Security Logs

| Field | Details |
|-------|---------|
| **Processing Activity** | Platform Monitoring & Security Logs |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | All platform users |
| **Data Categories** | IP addresses (anonymized after 90 days), request logs, error logs, performance metrics, security events |
| **Purpose of Processing** | Ensure platform availability, detect security threats, troubleshoot issues, comply with legal obligations |
| **Legal Basis** | Legitimate interests (GDPR Art. 6(1)(f)) - platform security and reliability |
| **Retention Period** | 90 days for full logs; 365 days for aggregated security metrics |
| **Recipients** | Operations team, security team, monitoring service providers |
| **Subprocessors** | Sentry (error tracking), Replit (infrastructure logs) |
| **International Transfers** | Sentry (US) under Standard Contractual Clauses |
| **Technical Measures** | Log aggregation, automated IP anonymization, role-based access, encrypted storage |

---

### 2.5 Marketing Communications

| Field | Details |
|-------|---------|
| **Processing Activity** | Marketing Communications |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | Prospects, customers who have consented |
| **Data Categories** | Email address, name, company name, marketing preferences, engagement metrics |
| **Purpose of Processing** | Send product updates, feature announcements, educational content |
| **Legal Basis** | Explicit consent (GDPR Art. 6(1)(a)) with double opt-in verification (PECR Regulation 22) |
| **Retention Period** | Until consent withdrawn + 30 days for processing |
| **Recipients** | Marketing team, email service provider |
| **Subprocessors** | Resend (email delivery) |
| **International Transfers** | EEA/UK hosting only |
| **Technical Measures** | Double opt-in verification, unsubscribe mechanisms, consent timestamp logging, encrypted storage |

---

### 2.6 Product Analytics (Aggregated)

| Field | Details |
|-------|---------|
| **Processing Activity** | Product Analytics (Aggregated) |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | Platform users (anonymized where possible) |
| **Data Categories** | Page views, feature usage, session duration, workflow statistics (aggregated), anonymized user IDs |
| **Purpose of Processing** | Improve product, identify bugs, optimize performance, understand user needs |
| **Legal Basis** | Legitimate interests (GDPR Art. 6(1)(f)) - product improvement and service optimization |
| **Retention Period** | 90 days for raw events; 24 months for aggregated statistics |
| **Recipients** | Product team, engineering team |
| **Subprocessors** | Vercel Analytics (infrastructure analytics) |
| **International Transfers** | EEA/UK or under Standard Contractual Clauses |
| **Technical Measures** | Anonymization, aggregation, IP masking, cookie consent controls |

---

### 2.7 Customer Support & Communications

| Field | Details |
|-------|---------|
| **Processing Activity** | Customer Support & Communications |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | Customers, support ticket requesters |
| **Data Categories** | Name, email, support ticket content, communication history |
| **Purpose of Processing** | Provide technical support, resolve issues, respond to inquiries |
| **Legal Basis** | Contractual necessity (GDPR Art. 6(1)(b)) for customers; legitimate interests for pre-sales inquiries |
| **Retention Period** | Duration of contract + 12 months |
| **Recipients** | Support team, engineering team (for technical issues) |
| **Subprocessors** | Email service provider (Resend) |
| **International Transfers** | EEA/UK only |
| **Technical Measures** | Encrypted email, access controls, ticket system security |

---

### 2.8 Backup & Disaster Recovery

| Field | Details |
|-------|---------|
| **Processing Activity** | Backup & Disaster Recovery |
| **Data Controller** | Levqor Limited |
| **Data Subjects** | All data subjects across all processing activities |
| **Data Categories** | All data categories (copies for recovery purposes) |
| **Purpose of Processing** | Business continuity, disaster recovery, data integrity |
| **Legal Basis** | Legitimate interests (GDPR Art. 6(1)(f)) - business continuity |
| **Retention Period** | 30 days (rolling backups) |
| **Recipients** | Infrastructure team (restore access only) |
| **Subprocessors** | Replit (infrastructure), PostgreSQL/Neon (database hosting) |
| **International Transfers** | EEA/UK infrastructure |
| **Technical Measures** | Encrypted backups (AES-256), access controls, automated backup processes |

---

## 3. Technical & Organisational Measures

### 3.1 Encryption

- **In Transit:** TLS 1.3 for all communications
- **At Rest:** AES-256 encryption for database storage
- **Backups:** Encrypted backups with separate encryption keys

### 3.2 Access Control

- **Principle:** Least privilege, role-based access control (RBAC)
- **Authentication:** Multi-factor authentication for administrative access
- **Session Management:** Automatic session timeout, secure token rotation

### 3.3 Security Monitoring

- **Real-time Alerts:** Sentry integration for error tracking and security events
- **Audit Logging:** Comprehensive logging of all data access and modifications
- **Incident Response:** 72-hour breach notification procedure (UK GDPR Art. 33)

### 3.4 Data Minimization & Retention

- **Collection:** Only essential data fields collected
- **Anonymization:** IP addresses anonymized after 90 days
- **Automated Deletion:** Scheduled cleanup jobs for expired data
- **Retention Schedules:** Documented and enforced per processing activity

### 3.5 High-Risk Processing Prohibitions

- **Automated Rejection:** Medical, legal, financial decision-making workflows blocked at API level
- **Special Category Data:** Prohibited by technical controls (keyword scanning)
- **Minor Data:** Processing of data relating to under-18s prohibited
- **Audit Trail:** All rejection attempts logged for compliance review

### 3.6 Vendor Management

- **Due Diligence:** All subprocessors assessed for GDPR compliance
- **Contracts:** Data Processing Agreements in place with all processors
- **Review Cycle:** Annual review of subprocessor compliance status

---

## 4. Data Subject Rights

Levqor supports the following rights under UK GDPR:

1. **Right of Access** (Art. 15): Data export functionality via `/data-requests`
2. **Right to Rectification** (Art. 16): Account settings, contact support
3. **Right to Erasure** (Art. 17): Account deletion with 30-day retention for recovery
4. **Right to Restriction** (Art. 18): Temporary processing suspension on request
5. **Right to Data Portability** (Art. 20): Export in JSON/CSV format
6. **Right to Object** (Art. 21): Opt-out from marketing, analytics
7. **Rights Related to Automated Decision-Making** (Art. 22): Not applicable (no automated decisions made)

**Contact for Rights Requests:** privacy@levqor.ai

---

## 5. Subprocessor List

| Subprocessor | Service | Location | Transfer Mechanism |
|--------------|---------|----------|-------------------|
| Stripe | Payment processing | US | Standard Contractual Clauses + Adequacy |
| Vercel | Frontend hosting | Global (EU nodes available) | Standard Contractual Clauses |
| Replit | Backend hosting | US | Standard Contractual Clauses |
| OpenAI | AI processing | US | Standard Contractual Clauses |
| Google Workspace | Workflow integrations | US | Standard Contractual Clauses |
| Microsoft 365 | Workflow integrations | EU/US | Standard Contractual Clauses |
| Make.com | Workflow automation | EU | EEA-based |
| Notion | Documentation integrations | US | Standard Contractual Clauses |
| Resend | Email delivery | EU | EEA-based |
| Sentry | Error monitoring | US | Standard Contractual Clauses |
| Neon (PostgreSQL) | Database hosting | EU | EEA-based |

---

## 6. Version Control & Change Log

### Version History

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | 14 November 2025 | Initial ROPA document | Data Protection Lead |

### Change Log

_No changes yet. This section will track material updates to processing activities._

---

## 7. Review & Maintenance

- **Review Frequency:** Annually, or upon material changes to processing activities
- **Next Review Date:** 14 November 2026
- **Responsible Party:** Data Protection Lead
- **Escalation:** Material changes require founder/DPO approval

---

**Document End**

For questions or updates to this ROPA, contact: privacy@levqor.ai
