#!/usr/bin/env node
const Stripe = require('stripe');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

async function main() {
  console.log('═══════════════════════════════════════');
  console.log('CREATING ENTERPRISE ADD-ONS');
  console.log('═══════════════════════════════════════\n');

  console.log('📦 Creating enterprise add-on products...');
  
  // Priority Support
  const pPrioritySupport = await stripe.products.create({
    name: 'Priority Support',
    description: 'Dedicated support with priority response times',
    active: true,
    metadata: { project: 'levqor', type: 'addon', sku: 'PRIORITY_SUPPORT' }
  });
  console.log(`  ✅ Priority Support: ${pPrioritySupport.id}`);

  const pricePrioritySupport = await stripe.prices.create({
    product: pPrioritySupport.id,
    currency: 'gbp',
    unit_amount: 9900, // £99
    recurring: { interval: 'month' }
  });
  console.log(`     Price: ${pricePrioritySupport.id} (£99/mo)`);

  // SLA 99.9%
  const pSLA = await stripe.products.create({
    name: 'SLA 99.9%',
    description: 'Enterprise-grade 99.9% uptime SLA with guaranteed response times',
    active: true,
    metadata: { project: 'levqor', type: 'addon', sku: 'SLA_99_9' }
  });
  console.log(`  ✅ SLA 99.9%: ${pSLA.id}`);

  const priceSLA = await stripe.prices.create({
    product: pSLA.id,
    currency: 'gbp',
    unit_amount: 19900, // £199
    recurring: { interval: 'month' }
  });
  console.log(`     Price: ${priceSLA.id} (£199/mo)`);

  // White-label
  const pWhiteLabel = await stripe.products.create({
    name: 'White-label',
    description: 'Remove Levqor branding and use your own custom branding',
    active: true,
    metadata: { project: 'levqor', type: 'addon', sku: 'WHITE_LABEL' }
  });
  console.log(`  ✅ White-label: ${pWhiteLabel.id}`);

  const priceWhiteLabel = await stripe.prices.create({
    product: pWhiteLabel.id,
    currency: 'gbp',
    unit_amount: 29900, // £299
    recurring: { interval: 'month' }
  });
  console.log(`     Price: ${priceWhiteLabel.id} (£299/mo)`);

  console.log('\n📝 Environment Variables:');
  console.log(`STRIPE_PRICE_ADDON_PRIORITY_SUPPORT=${pricePrioritySupport.id}`);
  console.log(`STRIPE_PRICE_ADDON_SLA_99_9=${priceSLA.id}`);
  console.log(`STRIPE_PRICE_ADDON_WHITE_LABEL=${priceWhiteLabel.id}`);

  const priceIds = {
    STRIPE_PRICE_ADDON_PRIORITY_SUPPORT: pricePrioritySupport.id,
    STRIPE_PRICE_ADDON_SLA_99_9: priceSLA.id,
    STRIPE_PRICE_ADDON_WHITE_LABEL: priceWhiteLabel.id,
  };

  require('fs').writeFileSync('/tmp/enterprise_addons.json', JSON.stringify(priceIds, null, 2));
  console.log('\n✅ Price IDs saved to /tmp/enterprise_addons.json');
}

main().catch(console.error);
