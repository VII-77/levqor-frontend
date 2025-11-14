# 📋 Stripe Setup Checklist

## Quick Reference for Creating Price IDs

### 1️⃣ Starter Monthly (£19/mo)
- [ ] Go to: https://dashboard.stripe.com/products
- [ ] Click "Add product"
- [ ] Name: `Levqor Starter`
- [ ] Price: `£19 GBP` / `Monthly`
- [ ] Copy Price ID → `STRIPE_PRICE_STARTER`

### 2️⃣ Starter Yearly (£190/yr)
- [ ] Same product, click "Add another price"
- [ ] Price: `£190 GBP` / `Yearly`
- [ ] Copy Price ID → `STRIPE_PRICE_STARTER_YEAR`

### 3️⃣ Pro Monthly (£49/mo)
- [ ] Click "Add product"
- [ ] Name: `Levqor Pro`
- [ ] Price: `£49 GBP` / `Monthly`
- [ ] Copy Price ID → `STRIPE_PRICE_PRO`

### 4️⃣ Pro Yearly (£490/yr)
- [ ] Same product, click "Add another price"
- [ ] Price: `£490 GBP` / `Yearly`
- [ ] Copy Price ID → `STRIPE_PRICE_PRO_YEAR`

---

## Add to Replit Secrets
```
STRIPE_PRICE_STARTER=price_xxxxx
STRIPE_PRICE_PRO=price_xxxxx
STRIPE_PRICE_STARTER_YEAR=price_xxxxx
STRIPE_PRICE_PRO_YEAR=price_xxxxx
SITE_URL=https://levqor.ai
```

## Add to Vercel
Same 5 secrets + `STRIPE_SECRET_KEY`

✅ Done!
