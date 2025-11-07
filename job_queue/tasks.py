import os
import redis
from rq import Queue
from rq.job import Job
import logging

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_conn = redis.from_url(REDIS_URL)
    job_queue = Queue('levqor_jobs', connection=redis_conn)
    logger.info(f"✅ Redis queue connected: {REDIS_URL}")
except Exception as e:
    logger.warning(f"⚠️  Redis unavailable: {e}. Queue disabled.")
    redis_conn = None
    job_queue = None

def execute_workflow_task(workflow_id, user_id, steps):
    import time
    logger.info(f"Executing workflow {workflow_id} for user {user_id}")
    
    results = []
    for step in steps:
        connector = step.get('connector')
        payload = step.get('payload', {})
        logger.info(f"  Step: {connector} with payload keys: {list(payload.keys())}")
        results.append({
            'connector': connector,
            'status': 'simulated_success',
            'executed_at': time.time()
        })
        time.sleep(0.1)
    
    logger.info(f"✅ Workflow {workflow_id} completed with {len(results)} steps")
    return {'workflow_id': workflow_id, 'results': results, 'status': 'completed'}

def enqueue_workflow(workflow_id, user_id, steps):
    if not job_queue:
        return {'error': 'queue_unavailable', 'fallback': 'sync_execution'}
    
    try:
        job = job_queue.enqueue(
            execute_workflow_task,
            workflow_id=workflow_id,
            user_id=user_id,
            steps=steps,
            job_timeout='5m'
        )
        logger.info(f"✅ Job enqueued: {job.id}")
        return {'job_id': job.id, 'status': 'enqueued'}
    except Exception as e:
        logger.error(f"❌ Failed to enqueue job: {e}")
        return {'error': str(e)}

def get_queue_health():
    if not redis_conn or not job_queue:
        return {
            'status': 'unavailable',
            'depth': 0,
            'fail_rate': 0,
            'retry_count': 0,
            'message': 'Redis not configured'
        }
    
    try:
        depth = len(job_queue)
        failed_queue = Queue('failed', connection=redis_conn)
        failed_count = len(failed_queue)
        
        total_jobs = depth + failed_count
        fail_rate = (failed_count / total_jobs * 100) if total_jobs > 0 else 0
        
        return {
            'status': 'healthy',
            'depth': depth,
            'failed': failed_count,
            'fail_rate': round(fail_rate, 2),
            'retry_count': 0
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'depth': 0,
            'fail_rate': 0,
            'retry_count': 0
        }
