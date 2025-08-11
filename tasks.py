import time
import random
from celery_app import app

@app.task(bind=True, name='tasks.process_data')
def process_data(self, data):
    """Process some data with potential for sleeping."""
    task_id = self.request.id
    print(f"Starting task {task_id} with data: {data}")
    
    # Simulate processing
    processing_time = random.randint(1, 5)
    print(f"Task {task_id} processing for {processing_time} seconds")
    time.sleep(processing_time)
    
    result = f"Processed data: {data} (took {processing_time}s)"
    print(f"Task {task_id} completed: {result}")
    return result

@app.task(bind=True, name='tasks.long_sleep')
def long_sleep(self, sleep_time=10):
    """A task that sleeps for a specified amount of time."""
    task_id = self.request.id
    print(f"Starting long sleep task {task_id} for {sleep_time} seconds")
    
    # This is a long-running task that sleeps
    time.sleep(sleep_time)
    
    print(f"Task {task_id} woke up after {sleep_time} seconds")
    return f"Slept for {sleep_time} seconds"

@app.task(bind=True, name='tasks.quick_task')
def quick_task(self, data):
    """A quick task that should not be blocked by sleeping tasks."""
    task_id = self.request.id
    print(f"Starting quick task {task_id} with data: {data}")
    
    # Quick processing
    result = f"Quickly processed: {data}"
    print(f"Task {task_id} completed: {result}")
    return result