# Email Footer Requirements - PECR/GDPR Compliance

## Mandatory Footer for Marketing & Product Update Emails

All marketing emails and product update emails MUST include the following footer:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are receiving this email because you opted in at levqor.ai

Levqor Ltd
London, United Kingdom

Manage your preferences or unsubscribe:
https://levqor.ai/marketing/unsubscribe?token={{UNSUBSCRIBE_TOKEN}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Token Generation

Each email must include a unique unsubscribe token that:
- Is unique per recipient
- Maps to the user's email and consent record
- Allows one-click unsubscribe without login
- Remains valid indefinitely (no expiry for unsubscribe tokens)

## Email Sending Policy

### ✅ ALLOWED WITHOUT CONSENT (Transactional)
- Order confirmations
- Payment receipts
- Security alerts
- Password resets
- Account verification
- Service notifications
- Incident reports
- Legal notices

### ❌ REQUIRES CONSENT (Marketing)
- Product updates
- New feature announcements
- Promotional offers
- Newsletter content
- Event invitations
- Tips and best practices
- Partnership announcements

### ⚠️ MUST CHECK BEFORE SENDING
Before sending any marketing/product update email:

```python
# Check user has granted consent
cursor.execute("""
    SELECT COUNT(*) FROM user_marketing_consent 
    WHERE email = ? 
    AND scope IN ('marketing', 'product_updates') 
    AND status = 'granted'
""", (recipient_email,))

if cursor.fetchone()[0] == 0:
    # DO NOT SEND - User has not opted in
    log.warning(f"Skipping marketing email to {recipient_email} - no consent")
    return
```

## Compliance Notes

1. **PECR (UK)**: Requires explicit consent for marketing emails
2. **GDPR**: Right to withdraw consent must be "as easy as to give"
3. **One-click unsubscribe**: Must work without requiring login
4. **Sender information**: Must include company name and location
5. **Consent status**: "pending_double_opt_in" is NOT granted - do not send

## HTML Email Template

```html
<table width="100%" cellpadding="20" bgcolor="#1e293b" style="margin-top: 40px; border-top: 2px solid #475569;">
  <tr>
    <td align="center">
      <p style="color: #94a3b8; font-size: 12px; line-height: 1.6; margin: 0;">
        You are receiving this email because you opted in at <strong>levqor.ai</strong>
      </p>
      <p style="color: #94a3b8; font-size: 12px; margin: 10px 0;">
        <strong>Levqor Ltd</strong><br/>
        London, United Kingdom
      </p>
      <p style="margin: 15px 0;">
        <a href="https://levqor.ai/marketing/unsubscribe?token={{UNSUBSCRIBE_TOKEN}}" 
           style="color: #10b981; text-decoration: none; font-size: 12px;">
          Manage preferences or unsubscribe
        </a>
      </p>
    </td>
  </tr>
</table>
```

## Plain Text Email Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are receiving this email because you opted in at levqor.ai

Levqor Ltd
London, United Kingdom

Manage your preferences or unsubscribe:
https://levqor.ai/marketing/unsubscribe?token={{UNSUBSCRIBE_TOKEN}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Audit Trail

All unsubscribe actions are automatically logged in:
- `user_marketing_consent` table (status updated to 'revoked')
- Application logs with timestamp and IP address

## Testing Checklist

- [ ] Footer appears in all marketing emails
- [ ] Unsubscribe link is clickable and valid
- [ ] One-click unsubscribe works without login
- [ ] Confirmation page displays after unsubscribe
- [ ] Re-sending to unsubscribed user is blocked
- [ ] Transactional emails still work after unsubscribe
