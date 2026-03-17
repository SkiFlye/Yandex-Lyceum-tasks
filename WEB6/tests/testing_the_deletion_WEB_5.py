from requests import get, post, delete

print(get("http://localhost:5000/api/jobs").json())
create_response = post("http://localhost:5000/api/jobs", json={
    'job': 'Job for deletion test',
    'team_leader': 1,
    'work_size': 10,
    'collaborators': '2, 3',
    'is_finished': False})
print(create_response.json())
job_id = create_response.json().get('id')
print(delete(f"http://localhost:5000/api/jobs/{job_id}").json())
print(delete(f"http://localhost:5000/api/jobs/{job_id}").json())
print(delete("http://localhost:5000/api/jobs/99999").json())
response = delete("http://localhost:5000/api/jobs/abc")
try:
    print(response.json())
except:
    print(response.text)
print(get("http://localhost:5000/api/jobs").json())