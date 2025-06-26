import uuid6
from typing import List
import logging

# Use a separate logger for core logic, or it will use the root logger
logger = logging.getLogger(__name__)

def get_uuidv7() -> str:
    """
    Generates and returns a single UUIDv7 string.
    """
    uuid_value = str(uuid6.uuid7())
    logger.debug(f"Generated UUIDv7: {uuid_value}") # Use debug for frequent logs
    return uuid_value

def get_uuidv7_batch(count: int) -> List[str]:
    """
    Generates and returns a list of UUIDv7 strings.

    Args:
        count: The number of UUIDv7 strings to generate.
               Must be a positive integer.
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer.")
    
    logger.debug(f"Generating a batch of {count} UUIDv7 strings") # Use debug
    uuids = [str(uuid6.uuid7()) for _ in range(count)]
    return uuids