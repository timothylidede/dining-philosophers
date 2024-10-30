import time
import redis
from celery_app import app

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

NUM_PHILOSOPHERS = 5

@app.task(bind=True, name="dining_philosophers_project.philosopher", max_retries=3, default_retry_delay=2)
def philosopher(self, philosopher_id):
    left_fork = f"fork_{philosopher_id}"
    right_fork = f"fork_{(philosopher_id + 1) % NUM_PHILOSOPHERS}"
    
    while True:
        print(f"[Philosopher {philosopher_id}] Thinking.")
        time.sleep(1)

        if philosopher_id % 2 == 0:
            forks_acquired = try_acquire_forks(left_fork, right_fork)
        else:
            forks_acquired = try_acquire_forks(right_fork, left_fork)
        
        if forks_acquired:
            print(f"[Philosopher {philosopher_id}] Successfully acquired both forks: {left_fork} and {right_fork}. Eating.")
            time.sleep(2)
            
            release_fork(left_fork)
            release_fork(right_fork)
            print(f"[Philosopher {philosopher_id}] Released forks: {left_fork} and {right_fork}.")
        else:
            print(f"[Philosopher {philosopher_id}] Could not acquire both forks. Returning to thinking.")
            try:
                self.retry(countdown=2 ** self.request.retries)
            except self.MaxRetriesExceededError:
                print(f"[Philosopher {philosopher_id}] Max retries exceeded. Going back to thinking.")
        
        time.sleep(1)

def try_acquire_forks(first_fork, second_fork):
    if acquire_fork(first_fork):
        if acquire_fork(second_fork):
            return True
        else:
            release_fork(first_fork)
    return False

def acquire_fork(fork):
    return redis_client.setnx(fork, 1)

def release_fork(fork):
    redis_client.delete(fork)
