# 📧 EMAIL FLOWS - POST-CHECKOUT AUTOMATION

## Flow Overview

```
Payment → Confirmation Email → Intake Form → Reminder (if not submitted) → Kickoff Call → Pre-Call Prep → Delivery → Handover → Upsell
```

---

## EMAIL 1: Payment Confirmation + Next Steps

**Trigger:** Immediately after Stripe payment success

**Subject Line:**  
✅ Payment confirmed! Here's what happens next (Levqor DFY)

**Body:**

```
Hey [First Name],

Thanks for trusting Levqor to build your automation! 🚀

Here's what you just purchased:
✅ [Plan Name] DFY Build (£[Amount])
✅ [X] workflow(s)
✅ Delivery in [Timeframe]
✅ [X] days of support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEP (5 minutes):
Fill out this quick intake form so we can start building:
👉 [LINK_INTAKE_FORM]

This form asks:
• What manual task is eating your time?
• Which tools do you use? (Gmail, Sheets, CRM, etc.)
• What's the desired outcome?
• Preferred contact method (call or async)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ TIMELINE:
• Today: You fill the intake form (5 min)
• Within 24h: We schedule a kickoff call (15-30 min)
• [Delivery timeframe]: We build, test, and deliver your automation
• Days after delivery: You use it, we support you ([X] days of email support)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ QUESTIONS?
Reply to this email or reach out at support@levqor.ai

We're here to make this smooth and stress-free.

Talk soon,
The Levqor Team

P.S. The faster you submit the intake form, the faster we start building. Most clients get their automation running within 48-72 hours!
```

**Tracking:** Log "confirmation_email_sent" event in CRM

---

## EMAIL 2: Intake Form Reminder (if not submitted after 24-48h)

**Trigger:** 24 hours after payment if intake form not submitted

**Subject Line:**  
Quick reminder: We need your intake form to start building

**Body:**

```
Hey [First Name],

Just a quick heads-up!

We're ready to build your [Plan Name] automation, but we need a bit of info first.

🎯 Please fill out your intake form (takes 5 minutes):
👉 [LINK_INTAKE_FORM]

Once you submit it, we'll:
1. Review your workflow in 24 hours
2. Schedule a kickoff call (or go async if you prefer)
3. Start building your automation immediately

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ REMINDER: Your [X]-day support period starts AFTER we deliver your automation.
The sooner we get the form, the sooner you start saving time!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need help? Reply to this email or ping us at support@levqor.ai

Cheers,
The Levqor Team
```

**Tracking:** Log "intake_reminder_sent" event

**Follow-up:** If still not submitted after 48h, send a second reminder or call them

---

## EMAIL 3: Pre-Call Prep (for DFY plans with a kickoff call)

**Trigger:** 1 hour before scheduled kickoff call

**Subject Line:**  
Your Levqor kickoff call is in 1 hour - here's what to bring

**Body:**

```
Hey [First Name],

Looking forward to our call in 1 hour! ☎️

Call Details:
📅 [Date/Time]
🔗 [Zoom Link or Phone Number]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 WHAT TO BRING (optional, but helpful):

1. **Logins for tools you want to connect**
   Example: Gmail, Google Sheets, CRM (HubSpot, Pipedrive, etc.)
   → We'll ask for read-only access where possible

2. **1-2 real examples of the task you want automated**
   Example: "Here's a lead from my website" or "Here's the report I manually create every Monday"

3. **Your biggest pain points**
   What manual task is eating the most time?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ AGENDA (15-30 minutes):
• Understand your current process (5-10 min)
• Design the automation together (5-10 min)
• Set expectations for delivery (5 min)
• Answer any questions you have

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Can't make it? No problem! Reply to this email and we can reschedule or go async (we'll design the automation via email instead).

See you soon,
The Levqor Team
```

**Tracking:** Log "pre_call_prep_sent" event

---

## EMAIL 4: Project Complete + Handover

**Trigger:** When automation is delivered and tested

**Subject Line:**  
🎉 Your automation is ready! Here's how to use it

**Body:**

```
Hey [First Name],

Your automation is DONE! 🚀

Here's what we built for you:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [Workflow 1 Name]: [Brief description of what it does]
✅ [Workflow 2 Name]: [Brief description] (if applicable)
✅ [Workflow 3 Name]: [Brief description] (if applicable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 YOUR DELIVERABLES:

1. **Fully-built automation(s)** → Already live in your accounts
2. **Documentation** → [LINK_TO_DOCS]
3. **Video walkthrough** → [LINK_TO_LOOM]
4. **Testing report** → [LINK_TO_TEST_RESULTS]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEPS:

1. Watch the Loom video (5 minutes) to see how it works
2. Test it yourself with 1-2 real examples
3. Reach out with questions (you have [X] days of email support)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 SUPPORT PERIOD:
You have [X] days of email support starting TODAY.

Need a tweak? Found a bug? Have questions?
Just reply to this email and we'll help you out (usually within 24h).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 WANT MORE AUTOMATION?

You just saved [X] hours/week with this automation.

Imagine saving 30+ hours/week by automating 10 more workflows...

Here's how:
→ **DFY Builds:** Buy another one-time build (£99-£599)
→ **Subscriptions:** Get 1-7 new workflows built every month (£29-£299/month)

👉 See all options: https://levqor.ai/pricing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thanks for trusting Levqor!
If you found this valuable, we'd love a testimonial (reply with 1-2 sentences and we'll feature you on our site 😊)

Cheers,
The Levqor Team

P.S. Your automation runs forever (it's yours). After the support period ends, you can still modify/use it. If you need updates later, just reach out!
```

**Tracking:** Log "handover_complete" event

**Upsell Trigger:** If user doesn't reply within 7 days, send a soft upsell email

---

## EMAIL 5: Upsell to Subscription (7 days after handover, if DFY only)

**Trigger:** 7 days after handover email sent, only if customer bought DFY (not subscription)

**Subject Line:**  
How's your automation working out?

**Body:**

```
Hey [First Name],

Quick check-in!

It's been a week since we delivered your automation. How's it working out?

→ Saving you time?
→ Any issues or questions?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 NEXT LEVEL AUTOMATION:

You automated [X] workflow(s) with your DFY build.

But most of our clients find they have 5-10 more processes they want automated as they grow.

Instead of buying DFY builds one at a time, you could **subscribe** and get:
→ 1-7 new workflows built every month
→ Ongoing support for all your automations
→ Monitoring + optimization + updates

Starting at **£29/month** (cheaper than 1 DFY build every 3 months).

👉 See subscription plans: https://levqor.ai/pricing#subscriptions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Not ready to subscribe? No worries!

Just reply if you have any questions or need help with your automation.

Cheers,
The Levqor Team
```

**Tracking:** Log "subscription_upsell_sent" event

**Conversion tracking:** If user clicks pricing link, tag them as "upsell_interested"

---

## EMAIL FLOW DIAGRAM (Text Version)

```
┌─────────────────────────────────────────────────────────────┐
│ PAYMENT SUCCESS (Stripe webhook)                            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ EMAIL 1: Confirmation + Intake Form Link (immediate)        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ USER ACTION: Fill intake form                               │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
    Form submitted            Form NOT submitted
             │                       │
             ▼                       ▼
┌──────────────────────┐   ┌──────────────────────────────────┐
│ Schedule kickoff call│   │ EMAIL 2: Reminder (24h later)    │
└──────────┬───────────┘   └────────────┬─────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────────────────────────────────────────────┐
│ EMAIL 3: Pre-Call Prep (1 hour before call)                 │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ KICKOFF CALL: 15-30 min (or async)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ WE BUILD: 24h - 7 days (depending on tier)                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ EMAIL 4: Handover + Deliverables (automation complete)      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ SUPPORT PERIOD: 7-30 days (depending on tier)               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ EMAIL 5: Upsell to Subscription (7 days after handover)     │
└─────────────────────────────────────────────────────────────┘
```

---

## IMPLEMENTATION NOTES

### Where to integrate:
1. **Stripe webhook:** Trigger Email 1 on payment success
2. **Intake form:** Track submission, trigger reminder if not submitted in 24h
3. **Calendar system:** Send Email 3 (Pre-Call Prep) 1 hour before call
4. **Project delivery:** Manually send Email 4 when automation is complete
5. **CRM automation:** Auto-send Email 5 (Upsell) 7 days after Email 4

### Email service:
- Use existing Resend/email infrastructure
- Store all emails as templates in backend
- Track opens/clicks for optimization

### Metrics to track:
- Intake form completion rate (target: 80%+)
- Call show-up rate (target: 70%+)
- Support question volume (optimize if >5 questions per build)
- Upsell conversion rate (target: 10-15%)

---

**Last Updated:** November 15, 2025  
**Status:** Ready to implement  
**Next Action:** Wire these emails into Stripe webhook + email automation system
