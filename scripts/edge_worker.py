#!/usr/bin/env python3
"""
EchoPilot Edge Worker (Phase 119)
Distributed edge queue processing for scaling job execution
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from collections import deque

def log_event(event_type, details=None):
    """Log edge worker events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'worker_id': os.getenv('WORKER_ID', 'worker_1'),
        'details': details or {}
    }
    
    log_file = Path('logs/edge_worker.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def enqueue_job(job_type, payload, priority='normal'):
    """
    Enqueue job for edge processing
    
    Args:
        job_type: Type of job (ai_task, report_gen, data_sync, etc.)
        payload: Job-specific data
        priority: low, normal, high, critical
    
    Returns:
        job_id
    """
    import uuid
    
    job_id = str(uuid.uuid4())[:8]
    
    job = {
        'job_id': job_id,
        'job_type': job_type,
        'payload': payload,
        'priority': priority,
        'status': 'queued',
        'queued_at': datetime.utcnow().isoformat() + 'Z',
        'worker_id': None,
        'attempts': 0
    }
    
    queue_file = Path('logs/edge_queue.ndjson')
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(queue_file, 'a') as f:
        f.write(json.dumps(job) + '\n')
    
    log_event('job_enqueued', {
        'job_id': job_id,
        'job_type': job_type,
        'priority': priority
    })
    
    return job_id

def get_queue_status():
    """Get queue statistics (de-duplicated by job_id)"""
    try:
        queue_file = Path('logs/edge_queue.ndjson')
        if not queue_file.exists():
            return {
                'total_jobs': 0,
                'queued': 0,
                'processing': 0,
                'completed': 0,
                'failed': 0
            }
        
        # De-duplicate by job_id - keep latest state only
        jobs_by_id = {}
        
        with open(queue_file, 'r') as f:
            for line in f:
                try:
                    job = json.loads(line)
                    job_id = job.get('job_id')
                    if job_id:
                        jobs_by_id[job_id] = job
                except:
                    continue
        
        # Calculate stats from de-duplicated jobs
        stats = {
            'total_jobs': len(jobs_by_id),
            'queued': 0,
            'processing': 0,
            'completed': 0,
            'failed': 0,
            'by_type': {}
        }
        
        for job in jobs_by_id.values():
            status = job.get('status', 'unknown')
            if status in stats:
                stats[status] += 1
            
            job_type = job.get('job_type', 'unknown')
            if job_type not in stats['by_type']:
                stats['by_type'][job_type] = 0
            stats['by_type'][job_type] += 1
        
        return stats
        
    except Exception as e:
        log_event('queue_status_error', {'error': str(e)})
        return {'error': str(e)}

def fetch_next_job(worker_id='worker_1'):
    """
    Fetch next job from queue (priority-based, de-duplicated)
    
    Returns:
        job dict or None
    """
    try:
        queue_file = Path('logs/edge_queue.ndjson')
        if not queue_file.exists():
            return None
        
        # De-duplicate by job_id - keep latest state only
        jobs_by_id = {}
        with open(queue_file, 'r') as f:
            for line in f:
                try:
                    job = json.loads(line)
                    job_id = job.get('job_id')
                    if job_id:
                        jobs_by_id[job_id] = job
                except:
                    continue
        
        # Filter to queued jobs only (using latest state)
        queued_jobs = [j for j in jobs_by_id.values() if j.get('status') == 'queued']
        
        if not queued_jobs:
            return None
        
        # Priority order: critical > high > normal > low
        priority_order = {'critical': 0, 'high': 1, 'normal': 2, 'low': 3}
        queued_jobs.sort(key=lambda j: priority_order.get(j.get('priority', 'normal'), 2))
        
        # Take first job
        job = queued_jobs[0].copy()
        job['status'] = 'processing'
        job['worker_id'] = worker_id
        job['started_at'] = datetime.utcnow().isoformat() + 'Z'
        job['attempts'] = job.get('attempts', 0) + 1
        
        # Update queue file (append updated job)
        with open(queue_file, 'a') as f:
            f.write(json.dumps(job) + '\n')
        
        log_event('job_fetched', {
            'job_id': job['job_id'],
            'job_type': job['job_type'],
            'worker_id': worker_id
        })
        
        return job
        
    except Exception as e:
        log_event('fetch_error', {'error': str(e)})
        return None

def complete_job(job_id, result=None, success=True):
    """Mark job as completed or failed"""
    completion = {
        'job_id': job_id,
        'status': 'completed' if success else 'failed',
        'completed_at': datetime.utcnow().isoformat() + 'Z',
        'result': result
    }
    
    queue_file = Path('logs/edge_queue.ndjson')
    with open(queue_file, 'a') as f:
        f.write(json.dumps(completion) + '\n')
    
    log_event('job_completed' if success else 'job_failed', {
        'job_id': job_id,
        'success': success
    })

def process_job(job):
    """Process a job (worker logic)"""
    job_type = job.get('job_type')
    payload = job.get('payload', {})
    
    log_event('job_processing', {
        'job_id': job['job_id'],
        'job_type': job_type
    })
    
    # Job type handlers
    if job_type == 'ai_task':
        # Simulate AI task processing
        time.sleep(0.5)
        return {'status': 'completed', 'tokens_used': 150, 'cost_usd': 0.02}
    
    elif job_type == 'report_gen':
        # Simulate report generation
        time.sleep(0.3)
        return {'status': 'completed', 'report_url': '/reports/report_123.pdf'}
    
    elif job_type == 'data_sync':
        # Simulate data sync
        time.sleep(0.2)
        return {'status': 'completed', 'records_synced': payload.get('record_count', 100)}
    
    else:
        return {'status': 'completed', 'note': 'No handler for this job type'}

def run_worker(max_jobs=10, worker_id='worker_1'):
    """Run edge worker - process jobs from queue"""
    print(f"Starting edge worker: {worker_id}")
    log_event('worker_started', {'worker_id': worker_id, 'max_jobs': max_jobs})
    
    processed = 0
    
    while processed < max_jobs:
        # Fetch next job
        job = fetch_next_job(worker_id=worker_id)
        
        if not job:
            print("  No jobs in queue, waiting...")
            time.sleep(1)
            continue
        
        print(f"  Processing job {job['job_id']} ({job['job_type']})...")
        
        try:
            # Process job
            result = process_job(job)
            
            # Mark as complete
            complete_job(job['job_id'], result=result, success=True)
            print(f"    ✓ Completed: {job['job_id']}")
            
            processed += 1
            
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            complete_job(job['job_id'], result={'error': str(e)}, success=False)
    
    log_event('worker_stopped', {'worker_id': worker_id, 'jobs_processed': processed})
    print(f"\nWorker stopped. Processed {processed} jobs.")
    
    return processed

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Edge Worker')
    parser.add_argument('--mode', choices=['worker', 'enqueue', 'status'], default='worker')
    parser.add_argument('--max-jobs', type=int, default=10)
    parser.add_argument('--worker-id', default='worker_1')
    args = parser.parse_args()
    
    if args.mode == 'worker':
        # Run worker
        run_worker(max_jobs=args.max_jobs, worker_id=args.worker_id)
    
    elif args.mode == 'enqueue':
        # Enqueue test job
        job_id = enqueue_job('ai_task', {'prompt': 'Test task'}, priority='normal')
        print(f"Enqueued job: {job_id}")
    
    elif args.mode == 'status':
        # Show queue status
        status = get_queue_status()
        print(json.dumps(status, indent=2))
