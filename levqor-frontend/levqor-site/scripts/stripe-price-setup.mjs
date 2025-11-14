#!/usr/bin/env node

import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-06-20',
});

const REQUIRED_PRICES = {
  // DFY (one-time)
  DFY_STARTER: { amount: 9900, currency: 'gbp', type: 'one_time', name: 'Levqor DFY Starter (One-Time)', description: '1 workflow, 48-hour delivery, 7-day support' },
  DFY_PROFESSIONAL: { amount: 24900, currency: 'gbp', type: 'one_time', name: 'Levqor DFY Professional (One-Time)', description: '3 workflows, 3-4 day delivery, 30-day support + monitoring' },
  DFY_ENTERPRISE: { amount: 59900, currency: 'gbp', type: 'one_time', name: 'Levqor DFY Enterprise (One-Time)', description: '7 workflows, 7-day delivery, 30-day support + dashboard' },
  
  // Subscriptions (monthly)
  GROWTH_M: { amount: 7900, currency: 'gbp', type: 'recurring', interval: 'month', name: 'Levqor Growth (Monthly)', description: '3 workflows/month, priority support' },
  
  // Subscriptions (yearly)
  GROWTH_Y: { amount: 79000, currency: 'gbp', type: 'recurring', interval: 'year', name: 'Levqor Growth (Yearly)', description: '3 workflows/month, priority support - 2 months free' },
};

async function findOrCreatePrice(key, spec) {
  console.log(`\n🔍 Checking: ${key} (${spec.name})`);
  console.log(`   Looking for: ${spec.currency.toUpperCase()} ${spec.amount / 100} (${spec.type}${spec.interval ? ` - ${spec.interval}` : ''})`);
  
  try {
    // List all prices
    const prices = await stripe.prices.list({
      limit: 100,
      active: true,
    });
    
    // Try to find matching price
    const match = prices.data.find(p => {
      const amountMatch = p.unit_amount === spec.amount;
      const currencyMatch = p.currency === spec.currency;
      const typeMatch = spec.type === 'one_time' ? p.type === 'one_time' : p.type === 'recurring';
      const intervalMatch = spec.type === 'recurring' ? p.recurring?.interval === spec.interval : true;
      
      return amountMatch && currencyMatch && typeMatch && intervalMatch;
    });
    
    if (match) {
      console.log(`   ✅ Found existing: ${match.id}`);
      return match;
    }
    
    // Create product first
    console.log(`   📦 Creating product: ${spec.name}`);
    const product = await stripe.products.create({
      name: spec.name,
      description: spec.description,
    });
    
    // Create price
    console.log(`   💰 Creating price...`);
    const priceData = {
      product: product.id,
      currency: spec.currency,
      unit_amount: spec.amount,
    };
    
    if (spec.type === 'one_time') {
      // No recurring field for one-time prices
    } else if (spec.type === 'recurring') {
      priceData.recurring = { interval: spec.interval };
    }
    
    const price = await stripe.prices.create(priceData);
    
    console.log(`   ✅ Created: ${price.id}`);
    return price;
    
  } catch (error) {
    console.error(`   ❌ Error: ${error.message}`);
    return null;
  }
}

async function main() {
  console.log('🚀 STRIPE PRICE SETUP - Levqor Dual Pricing');
  console.log('='.repeat(60));
  
  if (!process.env.STRIPE_SECRET_KEY) {
    console.error('❌ STRIPE_SECRET_KEY not found in environment');
    process.exit(1);
  }
  
  const results = {};
  
  for (const [key, spec] of Object.entries(REQUIRED_PRICES)) {
    const price = await findOrCreatePrice(key, spec);
    if (price) {
      results[key] = price.id;
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 RESULTS - Environment Variable Mapping:');
  console.log('='.repeat(60));
  console.log('\nAdd these to your Vercel/Replit environment:\n');
  
  for (const [key, priceId] of Object.entries(results)) {
    const envVarName = `STRIPE_PRICE_${key}`;
    console.log(`${envVarName}=${priceId}`);
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('📋 SUMMARY TABLE:');
  console.log('='.repeat(60));
  console.log('ENV VAR                              | Stripe Price ID    | Amount  | Type       | Interval');
  console.log('-'.repeat(100));
  
  for (const [key, priceId] of Object.entries(results)) {
    const spec = REQUIRED_PRICES[key];
    const envVarName = `STRIPE_PRICE_${key}`;
    const amount = `£${(spec.amount / 100).toFixed(2)}`.padEnd(7);
    const type = spec.type.padEnd(10);
    const interval = (spec.interval || '-').padEnd(8);
    
    console.log(`${envVarName.padEnd(36)} | ${priceId.padEnd(18)} | ${amount} | ${type} | ${interval}`);
  }
  
  console.log('\n✅ Stripe price setup complete!');
}

main().catch(console.error);
