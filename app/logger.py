import logging

def create_logger():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler and set its level
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler to log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger