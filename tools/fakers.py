import time

def get_random_email() -> str:
    return f"test{int(time.time())}@example.com"
