import time
import sys

# Add a 5-second wait to ensure indexing
print("Waiting for indexing: ", end='', flush=True)
for i in range(5, -1, -1):  # Adjusted range to include 0
    print(f"{i} ", end='', flush=True)  # Print the countdown number with a space
    time.sleep(0.9)
    print('\rWaiting for indexing: ', end='', flush=True)  # Return to the beginning of the line and overwrite
print("0")
print("Indexing complete.")
