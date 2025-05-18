from requests import get, put

# с несуществующей работой
print(put('http://localhost:8080/api/jobs/100',
           json={'team_leader': 1,
                 'job': 'new job post',
                 'work_size': 1,
                 'collaborators': '1, 2',
                 'is_finished': False,
                 'categories': '2'}).json())

# верный запрос
print(put('http://localhost:8080/api/jobs/2',
          json={'team_leader': 1,
                'job': 'new job put',
                'work_size': 1,
                'collaborators': '1, 2',
                'is_finished': False,
                'categories': '1'}).json())

print("Получение всех работ:")
print(get('http://localhost:8080/api/jobs').json())


