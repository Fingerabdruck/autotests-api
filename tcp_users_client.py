import socket

def client():
    # Создаём TCP‑сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        server_address = ('localhost', 12345)
        client_socket.connect(server_address)
        print("Подключено к серверу localhost:12345")

        # Отправляем сообщение серверу
        message = "Привет, сервер!"
        client_socket.send(message.encode())

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode()
        print(response)  # Выводим ответ сервера в консоль (как в примере задания)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем соединение в любом случае
        client_socket.close()
        print("Соединение закрыто")

if __name__ == "__main__":
    client()