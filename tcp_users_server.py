import socket

# Список для хранения всех сообщений
messages = []

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    # Поддерживаем до 10 подключений одновременно
    server_socket.listen(10)

    print("Сервер запущен и ждёт подключений...")

    try:
        while True:
            # Принимаем новое подключение
            client_socket, client_address = server_socket.accept()
            print(f"Пользователь с адресом: {client_address} подключился к серверу")

            # Получаем сообщение от клиента
            data = client_socket.recv(1024).decode()
            message = data.strip()  # Убираем лишние пробелы и переносы

            if message:  # Если сообщение не пустое
                print(f"Пользователь с адресом: {client_address} отправил сообщение: {message}")
                # Добавляем сообщение в историю
                messages.append(message)

            # Отправляем клиенту всю историю сообщений
            response = '\n'.join(messages)
            client_socket.send(response.encode())

            # Закрываем соединение
            client_socket.close()

    except KeyboardInterrupt:
        print("Сервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server()
