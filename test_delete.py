from requests import delete, get

# верный запрос
print(delete('http://localhost:8080/api/jobs/3', json={}).json())

# проверяем, что работа удалилась
print(get('http://localhost:8080/api/jobs').json())

# несуществующий id
print(delete('http://localhost:8080/api/jobs/3', json={}).json())
