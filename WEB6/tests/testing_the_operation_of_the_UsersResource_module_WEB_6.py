from requests import get, post, delete

BASE_URL = "http://127.0.0.1:5000"
print(get(f"{BASE_URL}/api/v2/users").json())
print(get(f"{BASE_URL}/api/v2/users/1").json())
print(get(f"{BASE_URL}/api/v2/users/999").json())
print(get(f"{BASE_URL}/api/v2/users/abc").status_code)
new_user = {
    'surname': 'Test',
    'name': 'User',
    'age': 25,
    'position': 'tester',
    'speciality': 'qa',
    'address': 'module_4',
    'email': 'test@mars.org',
    'password': '12345'}
print(post(f"{BASE_URL}/api/v2/users", json=new_user).json())
print(delete(f"{BASE_URL}/api/v2/users/7").json())
print(get(f"{BASE_URL}/api/v2/users/7").json())
print(post(f"{BASE_URL}/api/v2/users", json={}).status_code)
print(post(f"{BASE_URL}/api/v2/users", json={'name': 'No Surname'}).status_code)