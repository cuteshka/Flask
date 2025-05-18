from requests import get

print("Получение всех работ:")
print(get('http://localhost:8080/api/jobs').json())

print("Корректное получение одной работы:")
print(get('http://localhost:8080/api/jobs/2').json())

print("Ошибочный запрос на получение одной работы:")
print(get('http://localhost:8080/api/jobs/100').json())

print("Ошибочный запрос на получение одной работы:")
print(get('http://localhost:8080/api/jobs/апапрпр').json())


