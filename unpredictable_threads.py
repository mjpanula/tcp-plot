import threading
import time

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(10000):
        with lock:         # critical section
            edellinen = counter
            time.sleep(0.000000001)
            counter = edellinen + 1  # looks harmless, but not atomic!

threads = [threading.Thread(target=increment) for _ in range(4)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print("Expected:", 4 * 10000)
print("Actual:  ", counter)
