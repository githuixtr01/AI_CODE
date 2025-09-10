import time

def retry_on_failure(func, retries=3, delay=2):
    def wrapper(*args, **kwargs):
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[Retry] Attempt {attempt+1} failed: {e}")
                time.sleep(delay)
        raise Exception("All retries failed")
    return wrapper
