from celery_app import app

if __name__ == '__main__':
    # Start the Celery worker with eventlet pool
    # This ensures sleeping tasks don't block other tasks
    app.worker_main(
        argv=[
            'worker',
            '--loglevel=info',
            '-P', 'eventlet',  # Use eventlet pool for non-blocking tasks
            '--concurrency=4',
            '--prefetch-multiplier=1',
            '--without-mingle',  # Disable worker mingle
            '--without-gossip',  # Disable worker gossip
        ]
    )