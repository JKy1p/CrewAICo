import signal
import sys
import time

def signal_handler(sig, frame):
    print("Signal received: ", sig)
    print("Gracefully shutting down...")
    # Here, add your clean-up code
    # For example, inform Langsmith to terminate any pending operations
    # Close any open resources, files, etc.
    sys.exit(0)

def main():
    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Simulate a long-running process
    try:
        while True:
            print("Running... Press Ctrl+C to stop.")
            time.sleep(1)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        print("Performing final clean-up...")
        # Additional clean-up actions can be performed here

if __name__ == "__main__":
    main()
