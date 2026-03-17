from requests import get, post, put

print(get("http://localhost:5000/api/jobs").json())
create_response = post("http://localhost:5000/api/jobs", json={
    'job': 'Job for edit test',
    'team_leader': 1,
    'work_size': 10,
    'collaborators': '2, 3',
    'is_finished': False})
print(create_response.json())
job_id = create_response.json().get('id')
print(put(f"http://localhost:5000/api/jobs/{job_id}", json={
    'job': 'Updated job title',
    'work_size': 15,
    'is_finished': True}).json())
print(get(f"http://localhost:5000/api/jobs/{job_id}").json())
print(put("http://localhost:5000/api/jobs/99999", json={'job': 'This job does not exist'}).json())
print(put(f"http://localhost:5000/api/jobs/{job_id}", json={}).json())
response = put("http://localhost:5000/api/jobs/abc", json={'job': 'test'})
try:
    print(response.json())
except:
    print(response.text)
print(get("http://localhost:5000/api/jobs").json())