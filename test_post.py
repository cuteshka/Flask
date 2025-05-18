from requests import post, get

# без параметров
print(post('http://localhost:8080/api/jobs', json={}).json())



# верный запрос
print(post('http://localhost:8080/api/jobs',
           json={'team_leader': 1,
                 'job': 'new job post',
                 'work_size': 1,
                 'collaborators': '1, 2',
                 'is_finished': False,
                 'categories': '1'}).json())

print("Получение всех работ:")
print(get('http://localhost:8080/api/jobs').json())

# с несуществующей категорией
print(post('http://localhost:8080/api/jobs',
           json={'team_leader': 1,
                 'job': 'new job post',
                 'work_size': 1,
                 'collaborators': '1, 2',
                 'is_finished': False,
                 'categories': '2'}).json())

