# Legitimate Interest Assessment (LIA)
## Marketing and Analytics Processing

**Version:** 1.0  
**Assessment Date:** 14 November 2025  
**Review Date:** 14 November 2026  
**Prepared By:** Levqor Data Protection Lead  

---

## 1. Introduction

### 1.1 Purpose of this Assessment

This Legitimate Interest Assessment (LIA) evaluates Levqor's reliance on **legitimate interests** as a lawful basis for processing personal data under UK GDPR Article 6(1)(f) and EU GDPR Article 6(1)(f) for the following activities:

1. **Product analytics** (aggregated and anonymized where possible)
2. **Transactional and operational emails** (service-related communications)
3. **Security monitoring and fraud prevention**

This assessment follows the ICO's three-part test:
- **Purpose Test:** Is there a legitimate interest?
- **Necessity Test:** Is the processing necessary for that purpose?
- **Balancing Test:** Do the individual's interests override the legitimate interest?

### 1.2 Scope

**In Scope:**
- Platform usage analytics (page views, feature usage, session data)
- Security and audit logging (IP addresses, access logs, error reports)
- Transactional emails (password resets, billing receipts, service notifications)
- Essential service announcements (security incidents, material changes to terms)

**Out of Scope (Not Legitimate Interest):**
- **Marketing emails to new prospects:** Requires consent or soft opt-in (PECR Regulation 22)
- **Direct marketing to existing customers:** Uses soft opt-in exemption with clear opt-out
- **Cookie-based tracking:** Separately governed by cookie consent banner (PECR Regulation 6)

---

## 2. Purpose Test

### 2.1 Legitimate Interests Identified

We have identified the following legitimate business interests:

#### Interest 1: Platform Reliability and Performance

**Description:** Understanding how users interact with the platform to identify bugs, performance bottlenecks, and usability issues.

**Benefit:**
- Improve service quality and uptime
- Reduce errors and system failures
- Enhance user experience
- Maintain competitive product offering

**Who Benefits:** Levqor (business interest) and users (better service)

**Conclusion:** This is a **legitimate business interest** recognized under UK GDPR recital 47 ("ensuring network and information security").

---

#### Interest 2: Security and Fraud Prevention

**Description:** Detecting and preventing unauthorized access, abuse, fraud, and security threats.

**Benefit:**
- Protect user accounts from compromise
- Prevent platform abuse (spam, automated attacks)
- Comply with legal obligations to secure personal data (GDPR Art. 32)
- Detect and respond to security incidents within 72 hours (GDPR Art. 33)

**Who Benefits:** All users (security) and Levqor (legal compliance, reputation)

**Conclusion:** This is a **legitimate interest** explicitly recognized in UK GDPR recital 49 ("monitoring and prevention of fraud and security incidents").

---

#### Interest 3: Essential Service Communications

**Description:** Sending transactional and operational messages necessary for service delivery.

**Examples:**
- Password reset emails (security)
- Billing receipts and invoice notifications (contractual obligation)
- Urgent service disruption alerts (user interest)
- Critical security vulnerability notifications (legal obligation)

**Benefit:**
- Users can access their accounts securely
- Users are informed of billing activity (transparency)
- Users can take action during service disruptions
- Users can protect themselves from security threats

**Who Benefits:** Primarily users (essential information)

**Conclusion:** This is a **legitimate interest** aligned with contractual necessity and user expectations. Note: Most transactional emails also have a dual legal basis (contractual necessity, Art. 6(1)(b)).

---

#### Interest 4: Product Development and Innovation

**Description:** Understanding feature usage patterns to prioritize development and improve product-market fit.

**Benefit:**
- Build features users actually need
- Remove unused features to simplify interface
- Optimize resource allocation
- Maintain competitive advantage

**Who Benefits:** Levqor (business efficiency) and users (better product)

**Conclusion:** This is a **legitimate business interest** for product improvement, provided data is minimized and aggregated where possible.

---

### 2.2 Interests NOT Claimed as Legitimate Interest

The following activities **do not** rely on legitimate interest:

- **Cold marketing emails:** These require explicit consent (PECR Regulation 22) or soft opt-in exemption
- **Marketing to new prospects:** Uses consent with double opt-in verification
- **Non-essential cookies:** Require consent under PECR Regulation 6 (separately managed via cookie banner)
- **Sharing data with third parties for their marketing:** Not permitted under any basis

---

## 3. Necessity Test

### 3.1 Is Processing Necessary for the Purpose?

For each legitimate interest, we assess whether the processing is **necessary** or if less intrusive means could achieve the same objective.

#### Necessity Analysis 1: Platform Reliability

**Processing:** Collect page views, feature clicks, error logs, session duration

**Why Necessary:**
- Cannot identify bugs without error logs
- Cannot measure performance without timing data
- Cannot prioritize fixes without usage frequency data

**Could we achieve this another way?**
- **Avoid logs entirely?** No - debugging without logs is impossible at scale
- **User surveys only?** Insufficient - users don't report all issues, surveys have bias
- **Manual testing only?** Inadequate - cannot cover all user scenarios and edge cases

**Conclusion:** Processing is **necessary**; less intrusive alternatives are insufficient for service reliability.

---

#### Necessity Analysis 2: Security and Fraud Prevention

**Processing:** Log IP addresses, access timestamps, authentication events, failed login attempts

**Why Necessary:**
- Cannot detect brute-force attacks without login attempt logs
- Cannot trace security incidents without IP and timestamp data
- Cannot comply with GDPR Art. 32 (security measures) without monitoring
- Cannot fulfill 72-hour breach notification (Art. 33) without incident detection

**Could we achieve this another way?**
- **No logging?** Unacceptable security posture; non-compliant with GDPR Art. 32
- **Aggregated data only?** Loses ability to trace specific incidents
- **User-provided security only?** Insufficient - users cannot detect platform-level threats

**Conclusion:** Processing is **necessary** for security and legal compliance.

---

#### Necessity Analysis 3: Essential Service Communications

**Processing:** Send transactional emails (password resets, receipts, service alerts)

**Why Necessary:**
- Users cannot reset passwords without email delivery
- Users require billing receipts for tax/accounting (legal obligation)
- Users need to know about service disruptions to plan work
- Users must be informed of security vulnerabilities to take protective action

**Could we achieve this another way?**
- **No emails?** Impossible - core service functionality depends on email delivery
- **SMS only?** Not universally accessible; higher cost; less reliable for long messages
- **In-app notifications only?** Insufficient - users not always logged in when urgent action needed

**Conclusion:** Email processing is **necessary** for service delivery; no viable alternative exists.

---

#### Necessity Analysis 4: Product Development

**Processing:** Aggregate feature usage statistics, workflow complexity metrics

**Why Necessary:**
- Cannot allocate development resources without usage data
- Cannot identify unused features without tracking
- Pure speculation leads to poor product decisions

**Could we achieve this another way?**
- **Customer interviews only?** Useful but incomplete; subject to recall bias and small sample
- **Anonymous surveys?** Helpful but users don't know what they want until they see it
- **No data?** Results in wasteful development of unused features

**Mitigation Applied:**
- Aggregate where possible (e.g., "500 users clicked this button" vs. "User X clicked this button 5 times")
- Anonymize user IDs after initial collection
- Short retention (90 days for raw events, 24 months for aggregates)

**Conclusion:** Processing is **necessary** for effective product development, with minimization measures applied.

---

## 4. Balancing Test

### 4.1 Balancing Methodology

For each legitimate interest, we assess:

1. **Impact on Individuals:** What is the effect on data subjects?
2. **Reasonable Expectations:** Would users expect this processing?
3. **Safeguards:** What measures reduce impact?
4. **Opt-Out Availability:** Can users object?

**Outcome:** If individual's interests override Levqor's legitimate interests, we **cannot** rely on Art. 6(1)(f). Alternative legal basis required.

---

### 4.2 Balancing Analysis 1: Platform Reliability (Analytics)

**Impact on Individuals:**
- Low sensitivity data (page views, clicks, session duration)
- No special category data
- Aggregated where possible
- IP addresses anonymized after 90 days

**Reasonable Expectations:**
- Users of a cloud SaaS platform expect service provider to monitor performance
- Standard industry practice for web applications
- Disclosed in Privacy Policy

**Safeguards:**
- Data minimization (only essential metrics collected)
- Aggregation after 90 days (raw events deleted)
- No cross-site tracking (analytics limited to Levqor domain)
- Cookie consent banner for non-essential analytics cookies

**Opt-Out:**
- Cookie settings page allows disabling analytics cookies
- Does not affect core service functionality
- Aggregated data (no individual tracking) after 90 days

**Balancing Outcome:**
- **Levqor Interest:** Moderate (important for service quality, not critical)
- **Individual Impact:** Low (minimal privacy intrusion, safeguards strong)
- **Balance:** Levqor's legitimate interest **does not** override individual's rights
- **Conclusion:** Legitimate interest is **appropriate** with safeguards in place

---

### 4.3 Balancing Analysis 2: Security and Fraud Prevention

**Impact on Individuals:**
- Moderate sensitivity (IP addresses, login times)
- Necessary for account security
- Protects individuals from unauthorized access
- Short retention (90 days for detailed logs)

**Reasonable Expectations:**
- Users expect service providers to protect accounts from hacking
- Security monitoring is standard practice
- Users benefit directly from breach prevention
- Disclosed in Privacy Policy and Security page

**Safeguards:**
- IP anonymization after 90 days (last octet replaced with .xxx)
- Access limited to security team (RBAC)
- Automated threat detection (no manual browsing of logs)
- Incident response playbook (proportionate actions)

**Opt-Out:**
- Not applicable - security monitoring is essential to service delivery
- Opting out would create unacceptable risk for user and platform
- Alternative: Don't use the service

**Balancing Outcome:**
- **Levqor Interest:** High (legal obligation, user protection, business continuity)
- **Individual Impact:** Low (processing benefits user; minimal intrusion)
- **Balance:** Levqor's legitimate interest **does not** override individual's rights
- **Conclusion:** Legitimate interest is **strongly justified**

---

### 4.4 Balancing Analysis 3: Essential Service Communications

**Impact on Individuals:**
- Very low impact (users need these emails)
- Primarily transactional (not marketing)
- Sent only when triggered by user action or system event

**Reasonable Expectations:**
- Users expect to receive password reset emails
- Users expect to receive billing receipts
- Users expect to be notified of service disruptions
- Standard for any online service

**Safeguards:**
- Emails sent only when necessary (not promotional)
- Clear subject lines (no deceptive messaging)
- Frequency: Event-driven only (not periodic spam)
- Unsubscribe not applicable (these are essential, but users can close account)

**Opt-Out:**
- Not applicable for truly transactional emails (password reset, billing receipt)
- Users can opt out of service-level announcements (if not urgent security issues)
- Alternative: Don't use the service

**Balancing Outcome:**
- **Levqor Interest:** High (contractual necessity, user benefit)
- **Individual Impact:** Negligible (users want these emails)
- **Balance:** No conflict - interests aligned
- **Conclusion:** Legitimate interest is **clearly appropriate** (though most also qualify as contractual necessity, Art. 6(1)(b))

---

### 4.5 Balancing Analysis 4: Product Development

**Impact on Individuals:**
- Low impact when aggregated
- No special category data
- Short retention for raw data (90 days)
- Long retention for aggregates (24 months)

**Reasonable Expectations:**
- SaaS users expect product improvement based on usage patterns
- Standard practice disclosed in Privacy Policy
- Users benefit from better features

**Safeguards:**
- Anonymization of user IDs in aggregated reports
- No tracking of individual user behavior beyond 90 days
- Data used only for internal product decisions (not sold)
- Aggregation thresholds (e.g., don't report feature usage for <10 users)

**Opt-Out:**
- Cookie settings allow disabling analytics
- Aggregated data (no individual tracking) cannot be opted out (already anonymous)
- Does not affect service delivery

**Balancing Outcome:**
- **Levqor Interest:** Moderate (business efficiency, competitive advantage)
- **Individual Impact:** Very low (aggregated data, strong safeguards)
- **Balance:** Levqor's legitimate interest **does not** override individual's rights
- **Conclusion:** Legitimate interest is **appropriate** with strong minimization

---

## 5. Safeguards & Controls

### 5.1 Data Minimization

- **Collection:** Only fields necessary for stated purposes
- **Retention:** 90 days for raw logs; 24 months for aggregates; 365 days for security events
- **Aggregation:** Individual events rolled up into anonymous statistics after 90 days

### 5.2 Anonymization & Pseudonymization

- **IP Addresses:** Last octet replaced with .xxx after 90 days (e.g., 192.168.1.xxx)
- **User IDs:** Replaced with anonymous hashes in aggregate reports
- **Session IDs:** Rotated frequently; not cross-referenced with PII in analytics database

### 5.3 Access Controls

- **RBAC:** Role-based access; analytics data accessible only to product team
- **Security Logs:** Restricted to security team and authorized incident responders
- **Audit Trail:** All access to personal data logged for accountability

### 5.4 Transparency

- **Privacy Policy:** Clear explanation of analytics and security processing on `/privacy` page
- **Cookie Banner:** Granular controls for analytics cookies (separate from necessary cookies)
- **Opt-Out:** Cookie settings page (`/cookie-settings`) allows disabling non-essential tracking

### 5.5 Objection Rights (GDPR Art. 21)

Users can object to processing based on legitimate interests by:
- Adjusting cookie settings (analytics cookies)
- Contacting privacy@levqor.ai (security/operational emails reviewed case-by-case)

**Response Time:** 28 days to assess objection and respond

**Outcome:** If objection is valid and no overriding legitimate grounds exist, processing will cease for that individual.

---

## 6. Marketing Communications (NOT Legitimate Interest)

### 6.1 Clear Exclusion

**Important:** Levqor does **NOT** rely on legitimate interest for:

1. **Cold marketing emails to prospects:** Requires explicit consent (PECR Regulation 22)
2. **Direct marketing to new customers:** Uses double opt-in consent system
3. **Marketing to existing customers:** Uses soft opt-in exemption (PECR Regulation 22(3)) with clear opt-out

### 6.2 Consent-Based Marketing

**Legal Basis:** Consent (GDPR Art. 6(1)(a)) + PECR Regulation 22 compliance

**Implementation:**
- Marketing checkbox on sign-in page (unchecked by default)
- Double opt-in verification via email (cryptographic token)
- Unsubscribe link in every marketing email
- Separate consent tracking in database (marketing_consent, marketing_double_opt_in)

**Rationale:** UK/EU law is strict about marketing emails. Consent is the only safe basis for cold marketing; soft opt-in applies only to existing customers purchasing similar products.

See `/docs/compliance/marketing-consent-implementation.md` for technical details (internal reference).

---

## 7. Outcome & Conclusion

### 7.1 Summary of Legitimate Interest Reliance

| Processing Activity | Legitimate Interest | Necessity | Balance | LI Appropriate? |
|---------------------|---------------------|-----------|---------|-----------------|
| **Platform Analytics** | Product improvement | Yes (with minimization) | Pass | ✅ Yes |
| **Security Monitoring** | Fraud prevention, legal compliance | Yes | Pass (strong) | ✅ Yes |
| **Transactional Emails** | Service delivery | Yes | Pass (aligned interests) | ✅ Yes |
| **Product Development** | Business efficiency | Yes (aggregated) | Pass | ✅ Yes |
| **Marketing Emails** | N/A - uses consent | N/A | N/A | ❌ No (consent required) |

### 7.2 Overall Assessment

**Conclusion:** With the safeguards and controls documented in this LIA, **legitimate interest is an appropriate lawful basis** for:

1. Product analytics (aggregated, anonymized, minimal retention)
2. Security and fraud prevention monitoring
3. Essential transactional emails (password resets, billing, service alerts)
4. Product development (aggregated usage statistics)

**Key Safeguards:**
- Strong data minimization (only essential fields)
- Short retention periods (90 days for raw data)
- Anonymization and aggregation
- Clear transparency (Privacy Policy, cookie banner)
- Robust opt-out mechanisms (cookie settings, objection rights)

**Exclusions:**
- Pure marketing campaigns to new contacts: **Consent required**
- Soft opt-in for existing customers: **Separate legal basis** (PECR 22(3))
- Cookie tracking: **Separate consent** (PECR Regulation 6)

### 7.3 Compliance Statement

**Assessment:** Levqor's reliance on legitimate interests for the activities described in this LIA **complies with UK GDPR Article 6(1)(f) and EU GDPR Article 6(1)(f)**, provided:

1. Safeguards continue to be implemented and monitored
2. Data minimization and retention policies are enforced
3. Transparency (Privacy Policy, cookie banner) remains current
4. Users can exercise objection rights effectively

---

## 8. Review & Maintenance

### 8.1 Review Schedule

- **Frequency:** Annually, or upon significant changes to processing activities
- **Next Review Date:** 14 November 2026
- **Responsible Party:** Data Protection Lead

### 8.2 Triggers for Early Review

- Introduction of new analytics tools or tracking methods
- Changes to retention periods or data minimization practices
- Regulatory guidance from ICO or EDPB on legitimate interests
- User complaints or objections indicating balancing test may be incorrect

### 8.3 Version Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 14 November 2025 | Initial LIA for marketing and analytics | Data Protection Lead |

---

**Document End**

For questions regarding this LIA, contact: privacy@levqor.ai
