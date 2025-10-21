/**
 * EchoPilot Feature Flags Client Helper
 * Phase 108: Client-side feature flag evaluation with caching
 */

class FeatureFlags {
  constructor() {
    this.cache = {};
    this.cacheExpiry = 5 * 60 * 1000; // 5 minutes
    this.lastFetch = null;
    this.userId = this.getUserId();
  }

  /**
   * Get or generate user ID for consistent flag bucketing
   */
  getUserId() {
    let userId = localStorage.getItem('echopilot_user_id');
    
    if (!userId) {
      userId = 'anon_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('echopilot_user_id', userId);
    }
    
    return userId;
  }

  /**
   * Check if specific flag is enabled
   * @param {string} flagName - Name of feature flag
   * @returns {Promise<boolean>}
   */
  async isEnabled(flagName) {
    try {
      const response = await fetch(`/api/flags/check/${flagName}?user_id=${this.userId}`);
      const data = await response.json();
      
      return data.ok && data.enabled;
    } catch (error) {
      console.error('[FeatureFlags] Check failed:', error);
      return false;
    }
  }

  /**
   * Evaluate all flags for current user with caching
   * @returns {Promise<Object>} Map of flag names to boolean values
   */
  async evaluateAll() {
    const now = Date.now();
    
    // Return cache if still valid
    if (this.lastFetch && (now - this.lastFetch) < this.cacheExpiry) {
      return this.cache;
    }
    
    try {
      const response = await fetch(`/api/flags/evaluate?user_id=${this.userId}`);
      const data = await response.json();
      
      if (data.ok) {
        this.cache = data.flags;
        this.lastFetch = now;
        return this.cache;
      }
    } catch (error) {
      console.error('[FeatureFlags] Evaluate failed:', error);
    }
    
    return this.cache;
  }

  /**
   * Check multiple flags at once (uses cache)
   * @param {string[]} flagNames - Array of flag names
   * @returns {Promise<Object>} Map of flag names to boolean values
   */
  async checkMultiple(flagNames) {
    const allFlags = await this.evaluateAll();
    
    const result = {};
    flagNames.forEach(name => {
      result[name] = allFlags[name] || false;
    });
    
    return result;
  }

  /**
   * Refresh cache
   */
  async refresh() {
    this.lastFetch = null;
    return await this.evaluateAll();
  }

  /**
   * Conditional rendering helper
   * Shows/hides element based on feature flag
   * @param {string} flagName - Name of feature flag
   * @param {HTMLElement} element - DOM element to show/hide
   */
  async conditionalRender(flagName, element) {
    const enabled = await this.isEnabled(flagName);
    
    if (element) {
      element.style.display = enabled ? '' : 'none';
    }
    
    return enabled;
  }

  /**
   * A/B test variant helper
   * Returns variant A or B based on flag rollout percentage
   * @param {string} flagName - Name of feature flag
   * @param {Function} variantA - Function to execute for variant A
   * @param {Function} variantB - Function to execute for variant B
   */
  async abTest(flagName, variantA, variantB) {
    const enabled = await this.isEnabled(flagName);
    
    if (enabled) {
      return variantA();
    } else {
      return variantB();
    }
  }

  /**
   * Progressive rollout helper
   * Logs rollout participation for analytics
   * @param {string} flagName - Name of feature flag
   * @param {Function} callback - Function to execute if flag is enabled
   */
  async progressiveRollout(flagName, callback) {
    const enabled = await this.isEnabled(flagName);
    
    if (enabled) {
      console.log(`[FeatureFlags] User ${this.userId} in rollout for ${flagName}`);
      return callback();
    }
    
    return null;
  }

  /**
   * Clear local cache
   */
  clearCache() {
    this.cache = {};
    this.lastFetch = null;
  }
}

// Global instance
window.featureFlags = new FeatureFlags();

/**
 * Convenience function for checking flags
 * @param {string} flagName
 * @returns {Promise<boolean>}
 */
window.isFeatureEnabled = (flagName) => {
  return window.featureFlags.isEnabled(flagName);
};

// Auto-refresh cache every 5 minutes
setInterval(() => {
  window.featureFlags.refresh();
}, 5 * 60 * 1000);

console.log('[FeatureFlags] Client initialized');
