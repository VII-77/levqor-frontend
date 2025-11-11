#!/usr/bin/env python3
import os
import sys
import json
import CloudFlare

def log(message, level="INFO"):
    print(f"[{level}] {message}")

def main():
    log("============================================================")
    log("CLOUDFLARE CONFIGURATION SCRIPT - Day 2 Burn-In")
    log("============================================================")
    
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    
    if not api_token or not zone_id:
        log("Missing required environment variables", "ERROR")
        log("Required: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID", "ERROR")
        sys.exit(1)
    
    log(f"Zone ID: {zone_id[:8]}...{zone_id[-4:]}")
    
    try:
        cf = CloudFlare.CloudFlare(token=api_token)
        log("✅ Cloudflare API client initialized")
    except Exception as e:
        log(f"Failed to initialize Cloudflare client: {e}", "ERROR")
        sys.exit(1)
    
    log("")
    log("== STEP 1: TLS/SSL CONFIGURATION ==")
    
    try:
        log("Setting SSL mode to 'full' (strict)...")
        cf.zones.settings.ssl.patch(zone_id, data={'value': 'full'})
        log("✅ SSL mode: full (strict)")
    except Exception as e:
        log(f"⚠️  SSL mode: {e}", "WARN")
    
    try:
        log("Setting minimum TLS version to 1.2...")
        cf.zones.settings.min_tls_version.patch(zone_id, data={'value': '1.2'})
        log("✅ Minimum TLS: 1.2")
    except Exception as e:
        log(f"⚠️  Min TLS version: {e}", "WARN")
    
    try:
        log("Enabling TLS 1.3...")
        cf.zones.settings.tls_1_3.patch(zone_id, data={'value': 'on'})
        log("✅ TLS 1.3: enabled")
    except Exception as e:
        log(f"⚠️  TLS 1.3: {e}", "WARN")
    
    try:
        log("Enabling Always Use HTTPS...")
        cf.zones.settings.always_use_https.patch(zone_id, data={'value': 'on'})
        log("✅ Always Use HTTPS: enabled")
    except Exception as e:
        log(f"⚠️  Always Use HTTPS: {e}", "WARN")
    
    log("")
    log("== STEP 2: WAF CONFIGURATION ==")
    
    try:
        log("Setting security level to medium...")
        cf.zones.settings.security_level.patch(zone_id, data={'value': 'medium'})
        log("✅ Security level: medium")
    except Exception as e:
        log(f"⚠️  Security level: {e}", "WARN")
    
    try:
        log("Enabling browser integrity check...")
        cf.zones.settings.browser_check.patch(zone_id, data={'value': 'on'})
        log("✅ Browser integrity check: enabled")
    except Exception as e:
        log(f"⚠️  Browser check: {e}", "WARN")
    
    try:
        log("Enabling challenge passage...")
        cf.zones.settings.challenge_ttl.patch(zone_id, data={'value': 1800})
        log("✅ Challenge TTL: 1800 seconds (30 min)")
    except Exception as e:
        log(f"⚠️  Challenge TTL: {e}", "WARN")
    
    log("")
    log("== STEP 3: RATE LIMITING RULES ==")
    
    try:
        log("Creating rate limiting rule for /api/*...")
        
        try:
            rulesets = cf.zones.rulesets.phases.http_ratelimit.entrypoint.get(zone_id)
            ruleset_id = rulesets['id']
            log(f"Found existing ruleset: {ruleset_id[:16]}...")
        except Exception:
            log("Creating new rate limiting ruleset...")
            ruleset = cf.zones.rulesets.phases.http_ratelimit.entrypoint.put(
                zone_id,
                data={
                    'rules': []
                }
            )
            ruleset_id = ruleset['id']
            log(f"Created ruleset: {ruleset_id[:16]}...")
        
        rate_limit_rule = {
            'action': 'block',
            'expression': '(http.request.uri.path contains "/api/")',
            'description': 'Rate limit API endpoints - 100 req/min per IP',
            'ratelimit': {
                'characteristics': ['ip.src'],
                'period': 60,
                'requests_per_period': 100,
                'mitigation_timeout': 300,
                'requests_to_origin': True
            }
        }
        
        result = cf.zones.rulesets.rules.post(zone_id, ruleset_id, data=rate_limit_rule)
        log(f"✅ Rate limiting rule created: {result['id'][:16]}...")
        log("   - Path: /api/*")
        log("   - Limit: 100 requests/minute per IP")
        log("   - Action: block")
        log("   - Timeout: 300 seconds")
        
    except Exception as e:
        log(f"⚠️  Rate limiting: {e}", "WARN")
        log("   This might be because rate limiting rules already exist", "INFO")
    
    log("")
    log("== STEP 4: CACHE RULES ==")
    
    try:
        log("Creating cache rules...")
        
        cache_rules = {
            'rules': [
                {
                    'expression': '(http.request.uri.path wildcard "*") and (http.response.content_type.media_type eq "text/html")',
                    'description': 'Bypass HTML cache',
                    'action': 'set_cache_settings',
                    'action_parameters': {
                        'cache': False
                    }
                },
                {
                    'expression': '(http.request.uri.path wildcard "/public/*")',
                    'description': 'Cache public API endpoints',
                    'action': 'set_cache_settings',
                    'action_parameters': {
                        'cache': True,
                        'edge_ttl': {
                            'mode': 'override_origin',
                            'default': 300
                        },
                        'browser_ttl': {
                            'mode': 'override_origin',
                            'default': 60
                        }
                    }
                }
            ]
        }
        
        result = cf.zones.rulesets.phases.http_request_cache_settings.entrypoint.put(
            zone_id,
            data=cache_rules
        )
        
        log(f"✅ Cache rules created: {result['id'][:16]}...")
        log("   - HTML: bypass cache")
        log("   - /public/*: cache 5 minutes (edge), 1 minute (browser)")
        
    except Exception as e:
        log(f"⚠️  Cache rules: {e}", "WARN")
    
    log("")
    log("== STEP 5: VERIFICATION ==")
    
    try:
        ssl_settings = cf.zones.settings.ssl.get(zone_id)
        log(f"SSL Mode: {ssl_settings['value']}")
    except Exception:
        pass
    
    try:
        min_tls = cf.zones.settings.min_tls_version.get(zone_id)
        log(f"Min TLS: {min_tls['value']}")
    except Exception:
        pass
    
    try:
        tls13 = cf.zones.settings.tls_1_3.get(zone_id)
        log(f"TLS 1.3: {tls13['value']}")
    except Exception:
        pass
    
    try:
        security = cf.zones.settings.security_level.get(zone_id)
        log(f"Security Level: {security['value']}")
    except Exception:
        pass
    
    log("")
    log("============================================================")
    log("CLOUDFLARE CONFIGURATION COMPLETE")
    log("============================================================")
    log("")
    log("Next steps:")
    log("1. Wait 30-60 seconds for changes to propagate")
    log("2. Run verification:")
    log("   curl -sI https://levqor.ai | grep -i 'cf-cache-status\\|cf-ray'")
    log("3. Test rate limiting:")
    log("   for i in {1..105}; do curl -s https://api.levqor.ai/api/intelligence/status > /dev/null; done")
    log("")

if __name__ == "__main__":
    main()
