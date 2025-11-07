import os
import sys
import redis
from rq import Worker, Queue, Connection

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def main():
    print("=" * 60)
    print("Levqor RQ Worker")
    print("=" * 60)
    print(f"Redis URL: {REDIS_URL}")
    print()
    
    try:
        redis_conn = redis.from_url(REDIS_URL)
        redis_conn.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("\nTo start Redis locally:")
        print("  redis-server --daemonize yes")
        print("\nOr set REDIS_URL to an external Redis service (Upstash, Redis Cloud)")
        sys.exit(1)
    
    with Connection(redis_conn):
        worker = Worker(['levqor_jobs', 'default'])
        print("🚀 Worker starting...")
        print("   Listening on queues: levqor_jobs, default")
        print()
        worker.work()

if __name__ == '__main__':
    main()
