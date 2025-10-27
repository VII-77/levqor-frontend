// Minimal event analytics for EchoPilot
(function() {
  function trackEvent(type, meta) {
    try {
      const data = JSON.stringify({ type, meta });
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/event', new Blob([data], { type: 'application/json' }));
      } else {
        fetch('/api/event', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: data,
          keepalive: true,
        }).catch(() => {});
      }
    } catch (e) {
      // Silent fail
    }
  }

  // Phase 21: Track page views to analytics API
  function trackPageView() {
    try {
      fetch('/api/analytics/ingest/page', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: window.location.pathname,
          ref: document.referrer || '',
          ts: Date.now()
        }),
        keepalive: true
      }).catch(() => {});
    } catch (e) {}
  }

  // Track pageview on load
  if (document.readyState === 'complete') {
    trackEvent('pageview', { path: window.location.pathname });
    trackPageView();
  } else {
    window.addEventListener('load', function() {
      trackEvent('pageview', { path: window.location.pathname });
      trackPageView();
    });
  }

  // Track CTA clicks
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;
    
    const href = link.getAttribute('href');
    if (href === '/checkout' || href === '/pricing#pro') {
      trackEvent('checkout_click', { source: window.location.pathname });
    } else if (href === '/lead' || href === '/refer') {
      trackEvent('lead_click', { source: window.location.pathname });
    }
  }, true);
})();
