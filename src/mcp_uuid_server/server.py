from mcp.server.fastmcp import FastMCP
from .uuid_core import get_uuidv7, get_uuidv7_batch
from typing import List
import logging
import sys
import json
import threading

logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP(name="UUIDv7Server", description="Provides UUIDv7 generation tools.")

# --- HTTP Server (FastMCP) Tools ---
@mcp.tool()
def get_uuidv7_http() -> str:
    """
    Генерує та повертає один рядок UUIDv7 через HTTP.
    """
    return get_uuidv7()

@mcp.tool()
def get_uuidv7_batch_http(count: int) -> List[str]:
    """
    Генерує та повертає список рядків UUIDv7 через HTTP.
    """
    return get_uuidv7_batch(count)

# --- Логіка STDIO сервера ---
def _handle_stdio_request(request_json: str):
    """
    Обробляє один запит, отриманий через stdio. (Приватна функція)
    """
    response = {"id": None, "result": None, "error": None}
    try:
        request_data = json.loads(request_json)
        method = request_data.get("method")
        params = request_data.get("params", {})
        response["id"] = request_data.get("id")

        if method == "get_uuidv7":
            result = get_uuidv7()
            response["result"] = result
        elif method == "get_uuidv7_batch":
            count = params.get("count")
            if count is None:
                raise ValueError("Відсутній параметр 'count' для get_uuidv7_batch.")
            result = get_uuidv7_batch(count)
            response["result"] = result
        else:
            raise ValueError(f"Невідомий метод: '{method}'")

    except json.JSONDecodeError as e:
        logger.error(f"Помилка розбору JSON: {e} - Запит: '{request_json}'", exc_info=True)
        response["error"] = {"code": -32700, "message": "Помилка розбору", "data": str(e)}
    except ValueError as e:
        logger.error(f"Помилка недійсного запиту: {e}")
        response["error"] = {"code": -32602, "message": "Недійсні параметри", "data": str(e)}
    except Exception as e:
        logger.error(f"Внутрішня помилка сервера: {e}", exc_info=True)
        response["error"] = {"code": -32603, "message": "Внутрішня помилка", "data": str(e)}
    
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def _run_stdio_server_loop():
    """
    Основний цикл для stdio сервера, призначений для запуску в окремому потоці.
    """
    logger.info("Потік STDIO запущено. Очікування запитів на stdin...")
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            logger.debug(f"STDIO отримано: {line}")
            _handle_stdio_request(line)
    except Exception as e:
        logger.error(f"Критична помилка в потоці STDIO: {e}", exc_info=True)

def main():
    """
    Запускає UUIDv7 сервер одночасно в режимах HTTP та STDIO.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(threadName)s] - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stderr)])

    logger.info("Запуск сервера в комбінованому режимі (HTTP + STDIO)...")

    # Запускаємо stdio-сервер у фоновому потоці-демоні
    stdio_thread = threading.Thread(target=_run_stdio_server_loop, name="STDIO_Thread", daemon=True)
    stdio_thread.start()

    # Запускаємо HTTP-сервер в основному потоці
    logger.info("Запуск HTTP сервера...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Отримано сигнал зупинки. Завершення роботи...")
    finally:
        logger.info("Сервер зупинено.")

if __name__ == "__main__":
    main()
