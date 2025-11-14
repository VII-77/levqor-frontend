#!/usr/bin/env node

/**
 * ASE Follow-up Engine
 * 
 * Sends automated follow-up emails to leads:
 * - Email #1 (24h): Value content
 * - Email #2 (48h): Case study
 * - Email #3 (72h): Soft pitch
 */

import fetch from 'node-fetch';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const HOURS_24 = 24 * 60 * 60 * 1000;

async function runFollowups() {
  console.log('[ASE-FOLLOWUP] Starting followup engine...');
  
  try {
    const now = Date.now();
    
    // Fetch leads needing followup
    const response = await fetch(`${BACKEND_URL}/api/leads/followup-needed`);
    const data = await response.json();
    
    if (!data.ok) {
      console.error('[ASE-FOLLOWUP] Failed to fetch leads:', data.error);
      return;
    }
    
    const leads = data.leads || [];
    console.log(`[ASE-FOLLOWUP] Found ${leads.length} leads needing followup`);
    
    for (const lead of leads) {
      const lastContact = new Date(lead.last_contact).getTime();
      const hoursSinceContact = (now - lastContact) / (60 * 60 * 1000);
      
      let emailType = null;
      
      if (hoursSinceContact >= 72 && !lead.sent_email_3) {
        emailType = 'followup_soft_pitch';
      } else if (hoursSinceContact >= 48 && !lead.sent_email_2) {
        emailType = 'followup_case_study';
      } else if (hoursSinceContact >= 24 && !lead.sent_email_1) {
        emailType = 'followup_value';
      }
      
      if (emailType) {
        console.log(`[ASE-FOLLOWUP] Sending ${emailType} to ${lead.email}`);
        
        await fetch(`${BACKEND_URL}/api/leads/${lead.id}/send-followup`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email_type: emailType })
        });
      }
    }
    
    console.log('[ASE-FOLLOWUP] Followup engine complete');
  } catch (error) {
    console.error('[ASE-FOLLOWUP] Error:', error);
  }
}

runFollowups();
