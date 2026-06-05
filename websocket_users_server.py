import asyncio
import websockets
from websockets import ServerConnection

async def echo(websocket: ServerConnection):
    # Получаем ОДНО сообщение от клиента
    message = await websocket.recv()
    print(f"Получено сообщение от пользователя: {message}")

    # Отправляем 5 ответных сообщений с порядковыми номерами
    for i in range(1, 6):
        response = f"{i} Сообщение пользователя: {message}"
        await websocket.send(response)

async def main():
    server = await websockets.serve(echo, "localhost", 8765)
    print("WebSocket сервер запущен на ws://localhost:8765")
    await server.wait_closed()

asyncio.run(main())


