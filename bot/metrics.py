import json
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict, Counter

class MetricsCollector:
    def __init__(self):
        self.job_metrics = []
        self.failure_notes = []
    
    def record_job(self, metrics: Dict):
        self.job_metrics.append(metrics)
    
    def record_failure(self, note: str):
        self.failure_notes.append(note)
    
    def compute_weekly_report(self) -> Dict:
        now = datetime.now()
        week_start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        
        week_jobs = [m for m in self.job_metrics if m.get('timestamp', now) >= week_start]
        
        total_jobs = len(week_jobs)
        failures = [m for m in week_jobs if not m.get('success', True)]
        failure_count = len(failures)
        failure_rate = (failure_count / total_jobs * 100) if total_jobs > 0 else 0
        
        failure_causes = Counter([f.get('error', 'Unknown') for f in failures])
        top_3_failures = failure_causes.most_common(3)
        
        qa_scores = [m.get('qa_score', 0) for m in week_jobs if m.get('qa_score')]
        mean_qa = sum(qa_scores) / len(qa_scores) if qa_scores else 0
        
        latencies = [m.get('duration_ms', 0) for m in week_jobs if m.get('duration_ms')]
        latencies.sort()
        p95_latency = latencies[int(len(latencies) * 0.95)] if latencies else 0
        
        costs = [m.get('cost', 0) for m in week_jobs]
        cost_sum = sum(costs)
        
        return {
            'week_start': week_start.isoformat(),
            'jobs_total': total_jobs,
            'failures_total': failure_count,
            'failure_rate': round(failure_rate, 2),
            'top_3_failure_causes': [{'cause': k, 'count': v} for k, v in top_3_failures],
            'mean_qa': round(mean_qa, 2),
            'p95_latency_ms': round(p95_latency, 2),
            'cost_sum': round(cost_sum, 4)
        }
