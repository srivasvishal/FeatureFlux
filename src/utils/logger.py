"""
logger.py

Configures a logger using Python's logging module.
Provides a function to set up a named logger with a standard format.
"""

import logging

def setup_logger(name: str):
    """
    Creates and returns a logger with the specified name.
    
    Parameters:
      name: The name of the logger.
      
    Returns:
      A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Create console handler and set level to debug.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create formatter and add it to the handler.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # Add the handler to the logger if not already present.
    if not logger.handlers:
        logger.addHandler(ch)
    return logger

# Example usage:
if __name__ == "__main__":
    log = setup_logger("FeatureFluxLogger")
    log.debug("Debug message from FeatureFluxLogger")