#!/usr/bin/env node

/**
 * DFY Upsell Engine
 * 
 * Sends automated upsell emails after DFY purchase:
 * - Email #1 (0h): Welcome
 * - Email #2 (12h): Upgrade offer (£150 off Professional)
 * - Email #3 (36h): Last chance
 */

import fetch from 'node-fetch';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

async function runUpsells() {
  console.log('[DFY-UPSELLS] Starting upsell engine...');
  
  try {
    const now = Date.now();
    
    // Fetch DFY orders needing upsells
    const response = await fetch(`${BACKEND_URL}/api/dfy/upsell-needed`);
    const data = await response.json();
    
    if (!data.ok) {
      console.error('[DFY-UPSELLS] Failed to fetch orders:', data.error);
      return;
    }
    
    const orders = data.orders || [];
    console.log(`[DFY-UPSELLS] Found ${orders.length} orders needing upsells`);
    
    for (const order of orders) {
      // Only upsell Starter orders
      if (order.tier !== 'starter') continue;
      
      const createdAt = new Date(order.created_at).getTime();
      const hoursSinceCreation = (now - createdAt) / (60 * 60 * 1000);
      
      let emailType = null;
      
      if (hoursSinceCreation >= 36 && !order.sent_upsell_3) {
        emailType = 'dfy_upsell_36h';
      } else if (hoursSinceCreation >= 12 && !order.sent_upsell_2) {
        emailType = 'dfy_upsell_12h';
      } else if (hoursSinceCreation >= 0 && !order.sent_welcome) {
        emailType = 'dfy_welcome';
      }
      
      if (emailType) {
        console.log(`[DFY-UPSELLS] Sending ${emailType} to ${order.customer_email} (order ${order.id})`);
        
        await fetch(`${BACKEND_URL}/api/dfy/${order.id}/send-upsell`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email_type: emailType })
        });
      }
    }
    
    console.log('[DFY-UPSELLS] Upsell engine complete');
  } catch (error) {
    console.error('[DFY-UPSELLS] Error:', error);
  }
}

runUpsells();
