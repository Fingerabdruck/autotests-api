from clients.courses.courses_client import get_private_course_client, CreateCoursesResponseSchema, CreateCoursesRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_user_client, CreateUserRequestSchema
from testdata.files.files_client import get_private_file_client, CreateFileResponseSchema, CreateFileRequestSchema
from tools.fakers import get_random_email


""" 
Инициализация публичного клиента для регистрации нового пользователя без авторизации
"""
public_user_client = get_public_user_client()

"""
Формирование данных запроса на создание пользователя с рандомным email и фиксированным паролем
"""
create_user_request = CreateUserRequestSchema(
    email = get_random_email(),
    password = "string",
    last_name = "string",
    first_name = "string",
    middle_name = "string",
)

"""
Отправка запроса на регистрацию пользователя и получение ответа от сервера
"""
create_user_response = public_user_client.create_user(create_user_request)
print("Create user data: ", create_user_response)

"""
Подготовка данных для авторизации (email и пароль только что созданного пользователя)
"""
authentication_user = AuthenticationUserSchema(
    email = create_user_request.email,
    password = create_user_request.password,
)

"""
Создание приватных клиентов для работы с файлами, курсами и упражнениями (требуют авторизации)
"""
files_client = get_private_file_client(authentication_user)
course_client = get_private_course_client(authentication_user)

"""
Формирование запроса на загрузку файла: указание имени, директории и пути к локальному файлу
"""
create_file_request = CreateFileRequestSchema(
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
create_course_request = CreateCoursesRequestSchema(
    title= "Python for QA",
    max_score= 100,
    min_score= 10,
    description= "Python API Automation course for QA",
    estimated_time= "2 weeks",
    preview_file_id= create_file_response.file.id,
    created_by_user_id= create_user_response.user.id
)

"""
Создание курса на сервере с использованием подготовленных данных и получение ответа
"""
create_course_response = course_client.create_course(create_course_request)
print("Create course data: ", create_course_response)