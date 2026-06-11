from clients.courses.courses_client import get_private_course_client, CreateCoursesResponse, CreateCoursesRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.users.public_users_client import get_public_user_client, CreateUserRequestDict
from testdata.files.files_client import get_private_file_client, CreateFileResponse, CreateFileRequestDict
from tools.fakers import get_random_email


""" 
Инициализация публичного клиента для регистрации нового пользователя без авторизации
"""
public_user_client = get_public_user_client()

"""
Формирование данных запроса на создание пользователя с рандомным email и фиксированным паролем
"""
create_user_request = CreateUserRequestDict(
    email = get_random_email(),
    password = "string",
    lastName = "string",
    firstName = "string",
    middleName = "string",
)

"""
Отправка запроса на регистрацию пользователя и получение ответа от сервера
"""
create_user_response = public_user_client.create_user(create_user_request)
print("Create user data: ", create_user_response)

"""
Подготовка данных для авторизации (email и пароль только что созданного пользователя)
"""
authentication_user = AuthenticationUserDict(
    email = create_user_request['email'],
    password = create_user_request['password'],
)

"""
Создание приватных клиентов для работы с файлами, курсами и упражнениями (требуют авторизации)
"""
files_client = get_private_file_client(authentication_user)
course_client = get_private_course_client(authentication_user)

"""
Формирование запроса на загрузку файла: указание имени, директории и пути к локальному файлу
"""
create_file_request = CreateFileRequestDict(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)

"""
Загрузка файла на сервер и получение метаданных загруженного ресурса
"""
create_file_response = files_client.create_file(create_file_request)
print("Create file data: ", create_file_response)

"""
Формирование запроса на создание курса: передача заголовка, баллов, описания и ID загруженного файла
"""
create_course_request = CreateCoursesRequestDict(
    title= "Python for QA",
    maxScore= 100,
    minScore= 10,
    description= "Python API Automation course for QA",
    estimatedTime= "2 weeks",
    previewFileId= create_file_response['file']['id'],
    createdByUserId= create_user_response['user']['id']
)

"""
Создание курса на сервере с использованием подготовленных данных и получение ответа
"""
create_course_response = course_client.create_course(create_course_request)
print("Create course data: ", create_course_response)