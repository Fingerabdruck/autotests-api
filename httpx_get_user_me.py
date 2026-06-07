import httpx

login_payload = {
  "email": "mark@kuznetsov.ru",
  "password": "password"
}

login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
token_response = login_response_data['token']['accessToken']
print("Status code: ", login_response.status_code)
print("Response server: ", login_response_data)


headers = {"Authorization": f"Bearer {token_response}"}
get_user_response = httpx.get("http://127.0.0.1:8000/api/v1/users/me", headers=headers)

get_user_response_data = get_user_response.json()
print("Status code: ", get_user_response.status_code)
print("Response server: ", get_user_response_data)