from requests import get, post, delete

BASE_URL = "http://127.0.0.1:5000"

print(get(f"{BASE_URL}/api/v2/jobs").json())
print(get(f"{BASE_URL}/api/v2/jobs/1").json())
print(get(f"{BASE_URL}/api/v2/jobs/999").json())
print(get(f"{BASE_URL}/api/v2/jobs/abc").status_code)
new_job = {
    'job': 'Test job',
    'team_leader': 1,
    'work_size': 10,
    'collaborators': '2, 3',
    'is_finished': False,
    'category': 'test'}
print(post(f"{BASE_URL}/api/v2/jobs", json=new_job).json())
print(delete(f"{BASE_URL}/api/v2/jobs/7").json())
print(get(f"{BASE_URL}/api/v2/jobs/7").json())
print(post(f"{BASE_URL}/api/v2/jobs", json={}).status_code)
print(post(f"{BASE_URL}/api/v2/jobs", json={'job': 'No team leader'}).status_code)
print(post(f"{BASE_URL}/api/v2/jobs", json={
    'job': 'Wrong type',
    'team_leader': 'one',
    'work_size': 10,
    'collaborators': '2, 3',
    'is_finished': False}).status_code)