from tasks import process_data, long_sleep, quick_task
import time

def submit_tasks():
    """Submit a mix of tasks to demonstrate non-blocking behavior."""
    # Submit a long-running sleeping task
    print("Submitting a long sleep task (15 seconds)")
    sleep_result = long_sleep.delay(15)
    
    # Wait a moment
    time.sleep(1)
    
    # Submit 5 quick tasks that should run concurrently with the sleeping task
    print("Submitting 5 quick tasks")
    quick_results = []
    for i in range(5):
        result = quick_task.delay(f"Quick data {i}")
        quick_results.append(result)
    
    # Submit a few processing tasks
    print("Submitting 3 processing tasks")
    process_results = []
    for i in range(3):
        result = process_data.delay(f"Process data {i}")
        process_results.append(result)
    
    print("All tasks submitted!")

if __name__ == "__main__":
    submit_tasks()