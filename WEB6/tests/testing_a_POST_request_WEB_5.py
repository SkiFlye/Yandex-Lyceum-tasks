from requests import get, post

print(get("http://localhost:5000/api/jobs").json())
print(post("http://localhost:5000/api/jobs", json={'job': 'Deployment of solar panels', 'team_leader': 1,
                                                   'work_size': 20, 'collaborators': '2, 3, 4',
                                                   'category': 'construction', 'is_finished': False}).json())
print(post("http://localhost:5000/api/jobs", json={}).json())
print(post("http://localhost:5000/api/jobs", json={'team_leader': 1, 'work_size': 15, 'collaborators': '2, 3',
                                                   'category': 'test', 'is_finished': False}).json())
print(post("http://localhost:5000/api/jobs", json={'job': 'Wrong type test', 'team_leader': 'one', 'work_size': 10,
                                                   'collaborators': '2, 3', 'category': 'test',
                                                   'is_finished': False}).json())
print(get("http://localhost:5000/api/jobs").json())