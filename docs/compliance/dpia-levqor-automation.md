# Data Protection Impact Assessment (DPIA)
## Levqor Automation Platform

**Version:** 1.0  
**Assessment Date:** 14 November 2025  
**Review Date:** 14 November 2026  
**Prepared By:** Levqor Data Protection Lead  
**Approved By:** Founder / DPO  

---

## 1. Context & Scope

### 1.1 Description of Processing Operation

Levqor is a B2B SaaS platform that automates business workflows by connecting disparate systems and APIs. The platform enables business customers to:

- Create automated workflows that trigger actions based on events
- Integrate with third-party services (CRM, email, spreadsheets, messaging)
- Transform and route data between systems
- Execute scheduled or event-driven automation tasks

### 1.2 Nature and Scope

**Type of Processing:** Automated workflow execution, data transformation, API orchestration

**Data Subjects:**
- Primary: Business users (employees of customer organizations)
- Secondary: End users whose data is processed through customer workflows
- Tertiary: Levqor platform users (account administrators)

**Scale:**
- Target market: B2B organizations (SMEs to enterprise)
- Geographic scope: UK and EU initially, global expansion planned
- Processing volume: Variable depending on customer workflow complexity

**Context:**
- Business-to-business service (not consumer-facing)
- Processor role for customer data, controller role for account/billing data
- Real-time and scheduled processing

### 1.3 High-Risk Categories (Prohibited)

Levqor **explicitly prohibits** workflows involving:

1. **Medical/Healthcare:** Diagnosis, treatment recommendations, health advice, patient data
2. **Legal Services:** Legal advice, contract generation, litigation support
3. **Financial Decision-Making:** Investment advice, trading signals, tax preparation, loan decisions
4. **Minor Data:** Processing personal data of individuals under 18 years old
5. **Special Category Data (GDPR Art. 9):** Race, ethnicity, religion, biometrics, health data, sexual orientation

**Enforcement:** Technical controls scan workflow content for prohibited keywords and automatically reject submissions. See `/docs/compliance/high-risk-prohibition-policy.md` (internal reference).

**Rationale:** These prohibitions reduce risk of:
- Automated decision-making with significant legal/medical consequences
- Processing sensitive personal data without appropriate safeguards
- Liability for professional services requiring human judgment and licensing

---

## 2. Description of Processing

### 2.1 Data Sources

1. **Customer Input:** Workflow definitions, configuration parameters, trigger rules
2. **Third-Party APIs:** Customer-authorized integrations (CRM, email, databases, messaging platforms)
3. **System Events:** Platform-generated events (job completion, errors, schedules)
4. **User Input:** Manual workflow execution, form submissions

### 2.2 Processing Operations

1. **Collection:** Receive data from configured sources
2. **Validation:** Check data format, apply business rules
3. **Transformation:** Map fields, apply filters, aggregate data
4. **Enrichment:** Combine data from multiple sources
5. **Transmission:** Send data to destination APIs/services
6. **Logging:** Record workflow execution for debugging and audit
7. **Storage:** Temporary storage during workflow execution; configurable retention for logs

### 2.3 Data Categories Processed

**Account Data (Levqor as Controller):**
- Email address, name, company name, billing address
- Authentication credentials (hashed)
- Usage statistics, billing history

**Workflow Data (Levqor as Processor):**
- Varies by customer configuration
- Typical examples: contact lists, sales records, support tickets, event registrations
- **Excluded categories:** Medical records, legal documents, financial portfolios, special category data

### 2.4 Recipients

1. **Customer Organization:** Primary recipient of workflow outputs
2. **Authorized Customer Personnel:** Configured users with workflow access
3. **Third-Party APIs:** As configured by customer (e.g., CRM, email service, database)
4. **Levqor Operations Team:** Limited access for support and troubleshooting (RBAC enforced)
5. **Subprocessors:** OpenAI (optional AI features), Make.com, Google, Microsoft, Notion (per customer integration choices)

### 2.5 International Transfers

**Potential International Transfers:**
- Subprocessors located in US (OpenAI, Google, Microsoft) under Standard Contractual Clauses (SCCs)
- Supplementary measures: encryption, access controls, contractual restrictions

**Customer Control:**
- Customers can choose to limit data processing to EEA-only subprocessors (configuration option)
- Transfer Impact Assessment completed for US subprocessors (internal document)

---

## 3. Assessment of Necessity & Proportionality

### 3.1 Necessity Test

**Why is this processing necessary?**

1. **Core Service Delivery:** Automation cannot function without processing customer workflow data
2. **Customer Instructions:** Processing performed strictly according to customer-defined workflows
3. **Business Need:** Customers require automation to improve efficiency, reduce manual errors
4. **Contractual Obligation:** Processing necessary to fulfill service agreement with customer

**Could less intrusive means achieve the same purpose?**

- Manual workflows: Not feasible at scale; defeats the purpose of automation
- On-premise solutions: Higher cost, complexity; customer preference is cloud-based SaaS
- Data minimization applied: Only fields explicitly configured by customer are processed

**Conclusion:** Processing is necessary and proportionate to achieve legitimate business automation objectives.

### 3.2 Data Minimization Measures

1. **Optional Fields:** Customers only configure required data fields
2. **Anonymization Options:** Platform supports hashing/masking of sensitive fields (e.g., PII redaction)
3. **Log Scrubbing:** Automated removal of credentials and tokens from workflow logs
4. **Retention Limits:** Workflow logs retained for 30-90 days only (configurable per customer agreement)
5. **Access Controls:** Role-based access limits who can view workflow data

### 3.3 Retention Alignment

Retention periods align with documented policies:

- **Workflow Logs:** 30-90 days (operational requirement for debugging)
- **Account Data:** Duration of contract + 12 months (audit/dispute resolution)
- **Billing Data:** 7 years (UK tax law requirement)
- **Backups:** 30 days rolling (disaster recovery)

See `/privacy` and `/backups` pages for public-facing retention schedules.

---

## 4. Risk Identification & Evaluation

### 4.1 Risk Assessment Methodology

**Likelihood Scale:**
- Low (1): Unlikely to occur
- Medium (2): Possible under certain conditions
- High (3): Likely or has occurred before

**Impact Scale:**
- Low (1): Minor inconvenience, no material harm
- Medium (2): Moderate harm, limited scope
- High (3): Severe harm, significant consequences

**Risk Rating:** Likelihood × Impact = Inherent Risk Score

---

### 4.2 Identified Risks

#### Risk 1: Unauthorized Access to Workflow Data

**Description:** Attacker gains access to customer workflow data through platform vulnerability or credential compromise.

**Affected Individuals:** Business users, end users in customer workflows

**Likelihood:** Low (2) - Strong security controls in place, but external threats persist

**Impact:** High (3) - Could expose business-critical or personal data

**Inherent Risk:** Medium-High (6/9)

**Consequences:**
- Data breach affecting customer operations
- Regulatory penalties under GDPR
- Reputational damage to Levqor and customer
- Potential identity theft or fraud for data subjects

---

#### Risk 2: Misconfigured Workflow Sending Data to Wrong Recipient

**Description:** Customer configuration error causes workflow to send data to unintended destination (e.g., wrong email address, wrong API endpoint).

**Affected Individuals:** Data subjects whose information is mis-routed

**Likelihood:** Medium (2) - Human error in workflow configuration is possible

**Impact:** Medium (2) - Limited scope (single workflow), correctable

**Inherent Risk:** Medium (4/9)

**Consequences:**
- Unintended disclosure of personal data
- Customer embarrassment or business disruption
- Potential GDPR breach notification requirement
- Loss of customer trust

---

#### Risk 3: Vendor/Subprocessor Compromise

**Description:** Third-party subprocessor (e.g., OpenAI, Make.com, cloud provider) suffers security incident affecting Levqor customer data.

**Affected Individuals:** All users of workflows using compromised subprocessor

**Likelihood:** Low (1) - Vendors have strong security, but third-party risk exists

**Impact:** High (3) - Widespread impact, difficult to detect/remediate

**Inherent Risk:** Medium (3/9)

**Consequences:**
- Mass data exposure across multiple customers
- Regulatory investigation and penalties
- Contractual liability claims from customers
- Service disruption

---

#### Risk 4: Abuse/Misuse by Customer (Disallowed Use Cases)

**Description:** Customer attempts to use Levqor for prohibited purposes (medical advice, legal services, financial decisions, special category data).

**Affected Individuals:** Vulnerable individuals (patients, legal clients, minors)

**Likelihood:** Low (1) - Technical controls block prohibited content

**Impact:** High (3) - Could cause serious harm if controls bypassed

**Inherent Risk:** Medium (3/9)

**Consequences:**
- Serious harm to data subjects (e.g., incorrect medical advice)
- Regulatory enforcement action (ICO/EDPB)
- Legal liability for Levqor
- Ethical breach of duty of care

---

#### Risk 5: Inadequate Data Retention Leading to Premature Deletion

**Description:** Data deleted before legal retention period expires (e.g., tax records deleted before 7-year requirement).

**Affected Individuals:** Levqor (as data controller for billing data)

**Likelihood:** Low (1) - Automated retention schedules prevent this

**Impact:** Low (1) - Administrative burden to reconstruct records

**Inherent Risk:** Low (1/9)

**Consequences:**
- Non-compliance with UK tax law
- HMRC penalties
- Audit difficulties

---

#### Risk 6: Insufficient Transparency (Data Subjects Unaware of Processing)

**Description:** End users whose data flows through customer workflows are unaware that Levqor is processing their data.

**Affected Individuals:** End users in customer workflows (secondary data subjects)

**Likelihood:** Medium (2) - Transparency depends on customer's own privacy notices

**Impact:** Low (1) - Levqor acts as processor; transparency obligation primarily on customer (controller)

**Inherent Risk:** Low (2/9)

**Consequences:**
- Data subjects cannot exercise rights effectively
- GDPR transparency principle (Art. 12-14) not fully met
- Complaints to ICO

---

## 5. Mitigation Measures & Residual Risk

### 5.1 Risk 1 Mitigation: Unauthorized Access

**Controls Implemented:**

1. **Access Control:**
   - Role-based access control (RBAC) with least privilege
   - Multi-factor authentication (MFA) for administrative access
   - Automatic session timeout (15 minutes inactivity)

2. **Encryption:**
   - TLS 1.3 for all data in transit
   - AES-256 for data at rest (database, backups)
   - Separate encryption keys per environment

3. **Network Security:**
   - Rate limiting (20 req/min per IP, 200 req/min global)
   - IP allowlisting for admin access (optional)
   - DDoS protection via infrastructure provider

4. **Monitoring & Detection:**
   - Real-time security alerts (Sentry integration)
   - Audit logging of all data access
   - Anomaly detection for unusual access patterns

5. **Incident Response:**
   - 72-hour breach notification process (GDPR Art. 33)
   - Incident response playbook
   - Regular security drills

**Residual Risk:** Low (2/9) - Strong controls reduce likelihood to Low (1)

---

### 5.2 Risk 2 Mitigation: Workflow Misconfiguration

**Controls Implemented:**

1. **Workflow Validation:**
   - Pre-execution checks for valid destinations
   - Test mode for workflow dry-runs
   - Email confirmation for high-risk actions (optional)

2. **User Education:**
   - Documentation emphasizing configuration best practices
   - Warning prompts for destructive actions
   - Examples and templates for common workflows

3. **Audit Trail:**
   - Complete log of workflow executions
   - Traceable to specific user and timestamp
   - Available for customer review

4. **Rollback Capability:**
   - Version history for workflow definitions
   - Ability to revert to previous configurations
   - Disaster recovery backups

**Residual Risk:** Low (2/9) - Impact reduced to Low with validation checks

---

### 5.3 Risk 3 Mitigation: Vendor Compromise

**Controls Implemented:**

1. **Vendor Due Diligence:**
   - Annual security assessments of all subprocessors
   - Data Processing Agreements (DPAs) with all vendors
   - Review of vendor SOC 2 / ISO 27001 certifications

2. **Contractual Safeguards:**
   - Standard Contractual Clauses for international transfers
   - Breach notification clauses in vendor contracts
   - Right to audit vendor security practices

3. **Data Isolation:**
   - Customer data segregated by tenant
   - Encryption keys unique per customer (where feasible)
   - No shared credentials across customers

4. **Monitoring:**
   - Vendor security incident tracking
   - Regular review of vendor security bulletins
   - Incident escalation procedures

**Residual Risk:** Low (2/9) - Likelihood remains Low, monitoring reduces impact

---

### 5.4 Risk 4 Mitigation: Customer Abuse/Misuse

**Controls Implemented:**

1. **High-Risk Workflow Prohibition System:**
   - **Keyword Scanning:** 26 prohibited keywords across 6 categories (medical, legal, financial, tax, minors, special category data)
   - **Automated Rejection:** API-level blocking of workflows containing prohibited content
   - **Audit Logging:** Every rejection logged with user ID, timestamp, matched keywords
   - **User Warning:** HighRiskWarning component displayed on workflow creation page

2. **Policy Documentation:**
   - Risk disclosure page (`/risk-disclosure`) explains prohibited use cases
   - Terms of Service include acceptable use policy
   - Footer message on every page referencing restrictions

3. **Manual Review:**
   - Escalation path for edge cases
   - Human review of flagged workflows (if automated system uncertain)

4. **Account Suspension:**
   - Repeated attempts to bypass controls trigger account review
   - Immediate suspension for severe violations (e.g., medical decision-making)

**Residual Risk:** Low (1/9) - Technical controls highly effective; likelihood reduced to Very Low

---

### 5.5 Risk 5 Mitigation: Inadequate Data Retention

**Controls Implemented:**

1. **Automated Retention Schedules:**
   - Database-level retention policies
   - Scheduled cleanup jobs for expired data
   - Backup retention aligned with legal requirements

2. **Retention Documentation:**
   - Public-facing retention schedule on `/privacy` page
   - Internal ROPA documents retention per processing activity
   - Customer-configurable retention for workflow logs

3. **Safeguards Against Premature Deletion:**
   - Billing data retention: 7 years minimum (UK tax law)
   - 30-day recovery window for deleted accounts
   - Backup systems with independent retention

**Residual Risk:** Very Low (1/9) - Automated systems prevent human error

---

### 5.6 Risk 6 Mitigation: Insufficient Transparency

**Controls Implemented:**

1. **Customer Guidance:**
   - Data Processing Agreement (DPA) template provided to customers
   - Guidance on updating customer privacy notices to reference Levqor as processor
   - Sample privacy notice language available

2. **Processor Transparency:**
   - Levqor's own privacy policy explains processor role
   - Subprocessor list published and maintained (`/subprocessors`)
   - Data subject rights supported (access, erasure, portability)

3. **Customer Contracts:**
   - DPA requires customers to maintain lawful basis for processing
   - Customer warrants they have transparent privacy notices
   - Levqor provides data subject request support (within 28 days)

**Residual Risk:** Very Low (1/9) - Transparency obligation primarily on customer; Levqor provides tools and support

---

## 6. Consultation & Sign-Off

### 6.1 Stakeholder Consultation

The following stakeholders were consulted during this DPIA:

- **Engineering Team:** Reviewed technical controls and security measures
- **Legal Counsel:** Confirmed alignment with UK GDPR and PECR requirements
- **Customer Advisory Board:** Provided feedback on transparency and usability (planned)

### 6.2 Data Protection Officer (DPO)

**DPO Consultation:** This DPIA has been reviewed by Levqor's Data Protection Lead (acting DPO function).

**DPO Recommendation:** Approve with ongoing monitoring of:
1. High-risk workflow rejection rates (ensure controls not over-blocking)
2. Subprocessor security incidents (quarterly review)
3. Customer feedback on transparency tools

**DPO Contact:** privacy@levqor.ai

### 6.3 Customer Obligations

For high-risk use cases (large-scale processing, special category data if permissible, international transfers), **customers must consult their own DPO or legal counsel** before implementing workflows.

Levqor provides:
- Technical documentation for customer DPIAs
- Subprocessor information
- Security certifications (upon request)
- Cooperation with customer impact assessments

---

## 7. Approval & Review

### 7.1 Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Prepared By** | Data Protection Lead | [Digital signature] | 14 November 2025 |
| **Approved By** | Founder / DPO | [Digital signature] | 14 November 2025 |

### 7.2 Review Schedule

- **Frequency:** Annually, or upon material changes to processing operations
- **Next Review Date:** 14 November 2026
- **Triggers for Early Review:**
  - Introduction of new high-risk processing activities
  - Significant security incidents
  - Changes to GDPR/UK data protection law
  - Expansion into new geographic markets
  - Addition of new subprocessors with higher risk profile

### 7.3 Version Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 14 November 2025 | Initial DPIA for Levqor automation platform | Data Protection Lead |

---

## 8. Conclusion

### 8.1 Overall Assessment

**Summary:** The Levqor automation platform presents **moderate inherent risk** due to the nature of automated data processing and use of third-party subprocessors. However, **comprehensive technical and organizational measures** reduce residual risk to **acceptable low levels**.

**Key Safeguards:**
1. Technical controls prohibiting high-risk workflows (medical, legal, financial, special category data)
2. Strong encryption and access controls
3. Vendor due diligence and contractual safeguards
4. Transparent data subject rights processes
5. Comprehensive audit logging and incident response

**Residual Risk Rating:** **Low to Very Low** across all identified risks

### 8.2 Recommendations

1. **Continue Monitoring:** Track high-risk workflow rejection metrics to ensure controls are effective but not over-restrictive
2. **Annual Vendor Review:** Maintain rigorous subprocessor security assessments
3. **Customer Education:** Provide ongoing guidance on privacy best practices and transparent data processing
4. **Proactive Updates:** Review this DPIA whenever significant changes occur (new features, new subprocessors, regulatory changes)

### 8.3 Compliance Statement

**Assessment:** Processing operations described in this DPIA **comply with UK GDPR and EU GDPR** requirements, subject to ongoing implementation and monitoring of identified safeguards.

**Basis for Compliance:**
- Lawful basis established for all processing activities (see ROPA)
- Data minimization and purpose limitation applied
- Appropriate technical and organizational measures in place
- Data subject rights processes functional
- International transfer mechanisms valid (SCCs)
- Accountability demonstrated through documentation

---

**Document End**

For questions regarding this DPIA, contact: privacy@levqor.ai
