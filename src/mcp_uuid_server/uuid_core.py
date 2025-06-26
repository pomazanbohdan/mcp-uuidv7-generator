import uuid6
from typing import List
import logging

# Використовуємо окремий логер для основної логіки, або він буде використовувати кореневий
logger = logging.getLogger(__name__)

def get_uuidv7() -> str:
    """
    Генерує та повертає один рядок UUIDv7.
    """
    uuid_value = str(uuid6.uuid7())
    logger.debug(f"Згенеровано UUIDv7: {uuid_value}") # Використовуємо debug для частих логів
    return uuid_value

def get_uuidv7_batch(count: int) -> List[str]:
    """
    Генерує та повертає список рядків UUIDv7.

    Args:
        count: Кількість рядків UUIDv7 для генерації.
               Має бути додатним цілим числом.
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Кількість має бути додатним цілим числом.")
    
    logger.debug(f"Генерується партія з {count} рядків UUIDv7") # Використовуємо debug
    uuids = [str(uuid6.uuid7()) for _ in range(count)]
    return uuids