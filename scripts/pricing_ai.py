#!/usr/bin/env python3
"""
Adaptive Pricing AI - Phase 36
Dynamic pricing optimization based on QA scores and margins
"""
import os
import json
import statistics

def optimize_pricing(qa_scores=None, profit_margins=None):
    """Calculate optimized pricing based on performance metrics"""
    base_rate = float(os.getenv("DEFAULT_RATE_USD_PER_MIN", "0.50"))
    
    # Use defaults if not provided
    if qa_scores is None:
        qa_scores = [85, 88, 90]  # Default: good quality
    
    if profit_margins is None:
        profit_margins = [42, 46, 44]  # Default: healthy margins
    
    # Calculate adjustments
    qa_avg = statistics.mean(qa_scores)
    margin_avg = statistics.mean(profit_margins)
    
    # QA factor: 90% QA = 1.0x, higher = up to 1.15x, lower = down to 0.85x
    qa_factor = (qa_avg / 90.0)
    qa_factor = max(0.85, min(1.15, qa_factor))
    
    # Margin factor: 50% margin = 1.0x, higher allows lower price, lower requires higher price
    margin_factor = (50.0 / max(margin_avg, 20))
    margin_factor = max(0.85, min(1.15, margin_factor))
    
    # Combined adjustment (balanced between QA and margins)
    adjustment = (qa_factor + margin_factor) / 2.0
    
    # Apply adjustment with caps
    new_rate = base_rate * adjustment
    new_rate = max(base_rate * 0.8, min(base_rate * 1.25, new_rate))
    new_rate = round(new_rate, 2)
    
    return {
        "current_rate": base_rate,
        "new_rate": new_rate,
        "adjustment": round(adjustment, 3),
        "factors": {
            "qa_avg": round(qa_avg, 1),
            "qa_factor": round(qa_factor, 3),
            "margin_avg": round(margin_avg, 1),
            "margin_factor": round(margin_factor, 3)
        },
        "recommendation": "increase" if new_rate > base_rate else "decrease" if new_rate < base_rate else "maintain"
    }

if __name__ == "__main__":
    result = optimize_pricing([85, 88, 90], [42, 46, 44])
    print(json.dumps(result, indent=2))
