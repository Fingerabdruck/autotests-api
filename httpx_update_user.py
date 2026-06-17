import httpx
from tools.fakers import Fake

create_user_payload = {
  "email": get_random_email(),
  "password": "string",
  "lastName": "string",
  "firstName": "string",
  "middleName": "string"
}

create_user_response = httpx.post("http://127.0.0.1:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print("Create user data: ", create_user_response_data)


login_payload = {
    "email" : create_user_payload["email"],
    "password" : create_user_payload["password"]
}
login_response = httpx.post("http://127.0.0.1:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print("Login data: ", login_response_data)

patch_payload = {
  "email": get_random_email(),
  "lastName": "string3",
  "firstName": "string4",
  "middleName": "string5"
}
patch_headers = {"Authorization": f"Bearer {login_response_data['token']['accessToken']}"}
patch_response = httpx.patch(f"http://127.0.0.1:8000/api/v1/users/{create_user_response_data["user"]["id"]}", json=patch_payload, headers=patch_headers)
patch_response_data = patch_response.json()
print("Patch data: ", patch_response_data)
if patch_response.status_code == 200:
  print("Patch successful")
else:
  print("Patch failed")