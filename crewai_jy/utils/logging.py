import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Create a logger instance for the module
logger = logging.getLogger(__name__)

ERROR_MESSAGE = "An unexpected error occurred"

def some_function():
    try:
        # Simulate an error
        1 / 0
    except Exception as e:
        # Log the exception with traceback and additional details
        logger.exception(ERROR_MESSAGE + ": " + str(e))
        raise

if __name__ == "__main__":
    some_function()
