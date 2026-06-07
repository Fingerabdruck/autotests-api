import httpx

login_payload = {
  "email": "mark@kuznetsov.ru",
  "password": "password"
}

login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print(login_response.status_code)
print(login_response_data)

refresh_payload = { "refreshToken" : login_response_data['token']['refreshToken']}
refresh_response = httpx.post('http://127.0.0.1:8000/api/v1/authentication/refresh', json=refresh_payload)
refresh_response_data = refresh_response.json()
print(refresh_response.status_code)
print(refresh_response_data)