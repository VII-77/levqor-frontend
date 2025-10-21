/**
 * EchoPilot Client-Side Telemetry (Phase 111)
 * Lightweight event tracking with debounce and local retry
 */

(function() {
  'use strict';
  
  const TELEMETRY_ENDPOINT = '/api/analytics/event';
  const DEBOUNCE_MS = 1000;
  const RETRY_QUEUE_KEY = 'echopilot_telemetry_queue';
  const MAX_QUEUE_SIZE = 100;
  
  let eventQueue = [];
  let debounceTimer = null;
  let userId = localStorage.getItem('echopilot_user_id') || 'anonymous';
  
  // Set user ID
  function setUserId(id) {
    userId = id;
    localStorage.setItem('echopilot_user_id', id);
  }
  
  // Track event
  function track(eventType, feature, metadata) {
    const event = {
      event_type: eventType,
      feature: feature,
      metadata: metadata || {},
      user_id: userId,
      ts: new Date().toISOString(),
      url: window.location.pathname
    };
    
    eventQueue.push(event);
    
    // Debounce flush
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(flush, DEBOUNCE_MS);
  }
  
  // Flush events to server
  function flush() {
    if (eventQueue.length === 0) return;
    
    const batch = eventQueue.splice(0, eventQueue.length);
    
    fetch(TELEMETRY_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ events: batch }),
      keepalive: true
    })
    .then(response => {
      if (!response.ok) {
        // Save to local retry queue
        saveToRetryQueue(batch);
      }
    })
    .catch(() => {
      // Network error - save for retry
      saveToRetryQueue(batch);
    });
  }
  
  // Save failed events to retry queue
  function saveToRetryQueue(events) {
    try {
      let queue = JSON.parse(localStorage.getItem(RETRY_QUEUE_KEY) || '[]');
      queue = queue.concat(events).slice(-MAX_QUEUE_SIZE);
      localStorage.setItem(RETRY_QUEUE_KEY, JSON.stringify(queue));
    } catch (e) {
      // Storage full or quota exceeded
      console.warn('Telemetry retry queue full');
    }
  }
  
  // Retry failed events
  function retryQueue() {
    try {
      const queue = JSON.parse(localStorage.getItem(RETRY_QUEUE_KEY) || '[]');
      if (queue.length === 0) return;
      
      fetch(TELEMETRY_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ events: queue }),
        keepalive: true
      })
      .then(response => {
        if (response.ok) {
          localStorage.removeItem(RETRY_QUEUE_KEY);
        }
      });
    } catch (e) {
      // Ignore retry errors
    }
  }
  
  // Auto-track page views
  function trackPageView() {
    track('page_view', window.location.pathname.split('/')[1] || 'home');
  }
  
  // Auto-track clicks on buttons/links
  function setupClickTracking() {
    document.addEventListener('click', function(e) {
      const target = e.target.closest('[data-track]');
      if (target) {
        const feature = target.getAttribute('data-track');
        const action = target.getAttribute('data-action') || 'click';
        track('action', feature, { action: action });
      }
    });
  }
  
  // Initialize
  function init() {
    // Track page view
    trackPageView();
    
    // Setup click tracking
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setupClickTracking);
    } else {
      setupClickTracking();
    }
    
    // Retry failed events on load
    retryQueue();
    
    // Flush on page unload
    window.addEventListener('beforeunload', flush);
    
    // Periodic retry
    setInterval(retryQueue, 60000); // Every minute
  }
  
  // Export API
  window.EchoPilot = window.EchoPilot || {};
  window.EchoPilot.track = track;
  window.EchoPilot.setUserId = setUserId;
  window.EchoPilot.flush = flush;
  
  // Auto-initialize
  init();
  
})();
