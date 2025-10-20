# Getting Started with EchoPilot AI

## 🚀 5-Minute Quickstart

### Step 1: Access Your Dashboard

Visit your EchoPilot dashboard:
```
https://echopilotai.replit.app/dashboard
```

### Step 2: Enter Your Dashboard Key

Your dashboard key is:
```
CHMDlYY5TNE0NIB7qul7KYRa9a4BSbID-4WqpoE_DaE
```

1. **Mobile (Galaxy Fold 6):** 
   - Key is auto-filled and visible at top
   - Tap tabs at bottom to navigate
   - Toggle dark mode with moon/sun icon

2. **Desktop:**
   - Sidebar navigation appears at ≥1024px
   - Full keyboard navigation support
   - Press ⌘K (Mac) or Ctrl+K (Windows) for command palette

### Step 3: Key Workflows

#### Create a Test Brief
1. Go to **Automations** tab
2. Tap "Create Test Job"
3. View results in activity log

#### Check System Status
1. Go to **Operations** tab
2. Tap "✅ Check Health"
3. View metrics summary

#### Manage Payments (Stripe Live)
1. Go to **Payments** tab
2. Create invoice or view transactions
3. Stripe webhooks visible in real-time

### Step 4: Explore Features

- **⚙️ Automations:** Scheduler status, task management
- **💰 Payments:** Invoice creation, refunds, reconciliation
- **🔧 Operations:** Self-heal, metrics, system tools
- **📊 Audit:** Logs, events, compliance tracking
- **⚙️ Settings:** Theme, notifications, preferences

## 📱 Mobile-First Experience

### Galaxy Fold 6 Optimization

EchoPilot v2 is optimized for 360-430px screens:

- **Thumb-reachable tabs** at bottom
- **No horizontal scrolling**
- **Fast load times** (<1.5s TTI on 4G)
- **Smooth animations** (60fps)
- **Dark mode** with OLED-friendly blacks

### Keyboard Navigation

- **Tab:** Navigate between elements
- **Enter:** Activate buttons
- **⌘K/Ctrl+K:** Open command palette
- **Esc:** Close modals/dialogs

## 🔐 Security

### Dashboard Key

Your dashboard key provides authenticated access to:
- All API endpoints
- Automation controls
- Payment operations
- System administration

**Never share your dashboard key publicly.**

### Best Practices

1. **Store securely:** Use password manager
2. **Rotate regularly:** Contact admin for new key
3. **Monitor access:** Check audit logs for suspicious activity
4. **Use HTTPS:** Always access via secure connection

## 🎯 Common Tasks

### Create an Automation

```javascript
// POST /api/create-test-job
const response = await fetch('/api/create-test-job', {
  method: 'POST',
  headers: {
    'X-Dash-Key': 'YOUR_KEY_HERE',
    'Content-Type': 'application/json'
  }
});
```

### Check System Health

```javascript
// GET /api/status/summary
const response = await fetch('/api/status/summary');
const data = await response.json();
console.log(data.data.overall); // 'healthy', 'degraded', 'warning'
```

### View SLO Status

Navigate to **Operations** → **SLO Guard** to view:
- 99.9% availability target
- Error budget remaining
- P95 latency metrics
- Webhook success rates

## 🆘 Troubleshooting

### Dashboard Won't Load

1. Check system status at `/about`
2. Verify dashboard key is correct
3. Clear browser cache (Ctrl+Shift+R)
4. Try `/dashboard/v1` for legacy UI

### API Errors

**401 Unauthorized:**
- Verify dashboard key is correct
- Check key is properly set in input field

**429 Rate Limited:**
- You've exceeded request limits
- Wait 60 seconds and try again

**500 Server Error:**
- Check system status
- View audit logs for details
- Contact admin if persists

### Mobile Issues

**Tabs not working:**
- Ensure JavaScript is enabled
- Try hard refresh
- Check browser console for errors

**Layout broken:**
- Clear browser cache
- Verify screen width is supported
- Try desktop mode as fallback

## 📚 Next Steps

1. **Read Architecture:** `/docs/ARCHITECTURE.md`
2. **Security Guide:** `/docs/SECURITY.md`
3. **Runbook:** `/docs/RUNBOOK.md`
4. **Changelog:** `/docs/CHANGELOG.md`

## 💬 Support

For questions or issues:
1. Check audit logs in **Audit** tab
2. View system metrics in **Operations**
3. Review documentation in `/docs`

---

**Welcome to EchoPilot! 🤖**  
Your autonomous enterprise operations platform.
