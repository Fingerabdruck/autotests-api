import platform
import sys
from config import settings


def create_allure_environment_file():
    # 1. Создаем список из элементов конфигурации в формате {key}={value}
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    # 2. Получаем данные об ОС и Python
    os_info = f'{platform.system()}, {platform.release()}'
    python_version = str(sys.version).replace('\n', '')  # Убираем возможные переносы строк из версии

    # 3. Добавляем системную информацию в наш список
    items.append(f'os_info={os_info}')
    items.append(f'python_version={python_version}')

    # 4. Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # 5. Открываем файл ./allure-results/environment.properties на запись
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w') as file:
        file.write(properties)  # Записываем переменные в файл