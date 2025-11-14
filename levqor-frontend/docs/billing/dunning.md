# Stripe Dunning System - Levqor

**Version:** 1.0  
**Date:** 14 November 2025  
**Owner:** Billing Operations  

---

## Overview

Levqor implements a fair, transparent payment dunning system for subscription billing failures. This document describes the automated payment recovery process that activates when a customer's payment fails.

---

## Payment Failure Events

The dunning system responds to the following Stripe webhook events:

### 1. `invoice.payment_failed`
Triggered when Stripe fails to charge a customer's payment method for a subscription invoice.

**System Response:**
- Record the payment failure
- Schedule dunning email sequence (if dunning enabled)
- Continue monitoring subscription status

### 2. `customer.subscription.updated`
Triggered when subscription status changes (e.g., active → past_due → canceled).

**System Response:**
- Cancel scheduled dunning emails if subscription becomes active
- Update account status based on subscription state

---

## Dunning Email Schedule

When a payment fails, Levqor schedules a progressive email sequence:

| Timeline | Email | Content | Action |
|----------|-------|---------|--------|
| **Day 0** | Payment failed notice | Payment attempt failed, we'll retry automatically | None (informational) |
| **Day 7** | Second notice | Payment still outstanding, please update payment method | Warning |
| **Day 14** | Final notice | Final attempt before account pause | Account will be paused |

### Email Characteristics

All dunning emails include:
- Clear subject line indicating payment issue
- Total amount due and subscription plan name
- Link to billing management portal: `https://www.levqor.ai/billing`
- Support contact: `support@levqor.ai`
- No threatening language, respectful tone
- Plain text + HTML versions

---

## Account States

The dunning system manages account status through the following states:

| State | Description | Service Access | Resolution |
|-------|-------------|----------------|------------|
| **active** | Payment current, no issues | Full access | N/A |
| **dunning** | Payment failed, recovery in progress | Full access (grace period) | Update payment method |
| **paused** | 14 days unpaid, service suspended | No API/workflow execution | Resolve payment |
| **cancelled** | Customer cancelled subscription | No access | Resubscribe |

---

## Dunning Flow

```
┌─────────────────────┐
│  Payment Failure    │
│  (Day 0)            │
└──────┬──────────────┘
       │
       ├─ Day 1: Email #1 sent
       │
       ├─ Day 7: Email #2 sent
       │  Warning: service at risk
       │
       ├─ Day 14: Email #3 sent
       │  Final notice
       │
       └─ After Day 14: Account paused
          (subscription still active in Stripe,
           but API access disabled in Levqor)
```

### Recovery at Any Stage

If the customer updates their payment method and Stripe successfully charges:
- Subscription status returns to `active`
- All pending dunning emails are cancelled
- Account access is immediately restored
- Customer receives confirmation email

---

## Policy Details

### No Hidden Retries

Levqor does NOT retry payments outside of the documented schedule. The only retry attempts are:

1. **Stripe's automatic smart retry** (typically within 24 hours of initial failure)
2. **Explicit customer-initiated retries** via billing portal

We do not attempt additional charges without customer action.

### UK & EU Compliance

This dunning policy adheres to:
- **UK Consumer Rights Act 2015**: Clear communication of charges
- **EU Payment Services Directive (PSD2)**: Strong Customer Authentication (SCA) compliance
- **FCA Principles**: Treating customers fairly (TCF)
- **GDPR Article 6(1)(b)**: Processing necessary for contract performance

Customers receive:
- At least **14 days notice** before service suspension
- Clear instructions to resolve payment issues
- No surprise charges or auto-renewals without explicit consent
- Right to cancel subscription at any time

### Grace Period

Levqor provides a **14-day grace period** from initial payment failure:
- Days 0-14: Full service access maintained
- Days 14+: Service paused until payment resolved

This grace period exceeds industry standard (typically 7 days) to support customers experiencing temporary payment issues.

---

## Technical Implementation

### Database Schema

**Table:** `billing_dunning_events`

Tracks each scheduled dunning email:

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid | Primary key |
| created_at | timestamptz | Event creation time |
| updated_at | timestamptz | Last modification |
| stripe_customer_id | text | Stripe customer identifier (indexed) |
| stripe_subscription_id | text | Stripe subscription ID (indexed) |
| invoice_id | text | Failed invoice ID |
| email | text | Customer email address |
| plan | text | Subscription plan name |
| attempt_number | integer | Email sequence number (1, 2, 3) |
| scheduled_for | timestamptz | When to send this email |
| sent_at | timestamptz | When email was actually sent (null if pending) |
| status | text | `pending`, `sent`, `skipped`, `error` |
| error_message | text | Error details if send failed |

### Webhook Handler

Location: Backend `/webhooks/stripe` (or Flask equivalent)

Responsibilities:
- Verify Stripe webhook signature
- Handle `invoice.payment_failed` events
- Handle `customer.subscription.updated` events
- Schedule dunning emails (if `DUNNING_ENABLED=True`)
- Skip dunning events when subscription recovers

### Dunning Job

Location: `backend/billing/dunning.py`

Responsibilities:
- Query pending dunning events (`status=pending`, `scheduled_for <= now`)
- Render appropriate email template (attempt 1/2/3)
- Send via configured email provider (Resend)
- Update event status (`sent`, `error`)
- Log all actions for audit

**Execution:** Intended to run as cron job (e.g., every 6 hours)

**Safety:** Respects `DUNNING_ENABLED` flag - no emails sent if disabled

---

## Configuration

### Environment Variables

```bash
# Feature flag (default: False for safety)
DUNNING_ENABLED=false

# Stripe webhook signature verification
STRIPE_WEBHOOK_SECRET=whsec_...

# Email provider (Resend)
RESEND_API_KEY=re_...

# Billing portal URL
BILLING_PORTAL_URL=https://www.levqor.ai/billing
```

### Constants

```python
DUNNING_ENABLED = False  # CRITICAL: Must be explicitly enabled
DUNNING_SCHEDULE_DAYS = [1, 7, 14]  # Days after failure to send emails
```

---

## Enabling Dunning System

**Prerequisites:**
1. ✅ Database migration applied (`billing_dunning_events` table exists)
2. ✅ Webhook handler deployed and receiving Stripe events
3. ✅ Email templates tested and approved
4. ✅ Cron job scheduled (e.g., `*/6 * * * *` - every 6 hours)
5. ✅ `STRIPE_WEBHOOK_SECRET` configured
6. ✅ `RESEND_API_KEY` configured

**Activation:**
1. Set `DUNNING_ENABLED=true` in environment variables
2. Restart backend application
3. Monitor logs for first 24 hours
4. Verify emails send correctly for test failures

**Rollback:**
1. Set `DUNNING_ENABLED=false`
2. Restart backend
3. System returns to passive monitoring (no emails sent)

---

## Monitoring & Alerts

### Key Metrics

Track the following in production:
- **Dunning email delivery rate**: % of scheduled emails successfully sent
- **Email bounce rate**: % of emails rejected by recipient servers
- **Payment recovery rate**: % of failed payments recovered within 14 days
- **Account pause rate**: % of subscriptions reaching Day 14 unpaid

### Alerts

Set up alerts for:
- ⚠️ Dunning email send failures (>5% error rate)
- ⚠️ Webhook processing errors (signature verification failures)
- ⚠️ Database write failures (event recording issues)
- 🚨 DUNNING_ENABLED changed (security audit)

---

## Customer Support

### Common Scenarios

**"I already updated my card, why did I get another email?"**
- Dunning emails are scheduled in advance
- If payment succeeds, subsequent emails are auto-cancelled
- Any emails received after successful payment are final notifications

**"Can I get more time to pay?"**
- Grace period is 14 days (fixed)
- Contact support@levqor.ai for hardship arrangements
- Account pause does not cancel subscription (can be reactivated)

**"Why was my account paused without warning?"**
- 3 emails sent over 14 days
- Check spam/junk folder for dunning notices
- Contact support to verify email delivery

---

## Audit Trail

All dunning events are logged:

| Event Type | Logged Data | Retention |
|------------|-------------|-----------|
| Payment failure | customer_id, subscription_id, invoice_id, amount | 90 days |
| Email scheduled | event_id, scheduled_for, attempt_number | 90 days |
| Email sent | event_id, sent_at, recipient | 90 days |
| Email error | event_id, error_message, retry_count | 90 days |
| Account paused | customer_id, pause_reason, timestamp | 7 years (billing) |

---

## FAQ

**Q: How many payment retries does Levqor make?**  
A: Levqor does not retry payments. Stripe retries once within 24 hours. After that, the customer must update their payment method.

**Q: Will I be charged if I fix my payment on Day 5?**  
A: Yes, Stripe will automatically charge once a valid payment method is added. You'll receive a confirmation email.

**Q: Does pausing my account cancel my subscription?**  
A: No. Your subscription remains active in Stripe but service access is disabled. Resolve payment to restore access.

**Q: Can I cancel during the grace period?**  
A: Yes. You can cancel anytime via the billing portal. Cancellation is immediate.

**Q: What happens to my data if my account is paused?**  
A: Data is retained for 30 days. After 30 days, workflows and logs are deleted per retention policy.

---

## Related Documentation

- [Payment Failure Handling (Customer-facing)](/billing)
- [Billing Support Policy](/support-policy)
- [Subscription Terms](/terms)
- [Data Retention Policy](/privacy)

---

**Document Revision History**

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 14 Nov 2025 | 1.0 | Initial dunning system documentation | Billing Ops |

---

**Review Schedule:** Annually or upon regulatory changes  
**Owner:** Billing Operations Team  
**Contact:** billing@levqor.ai
