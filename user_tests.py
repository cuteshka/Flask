from requests import get, post, delete

# print("Получение всех сотрудников")
# print(get('http://localhost:8080/api/users').json())
#
# print("Корректное получение одного")
# print(get('http://localhost:8080/api/users/1').json())
#
# print("Ошибочный запрос:")
# print(get('http://localhost:8080/api/users/100').json())
#
# print("Ошибочный запрос на получение одной работы:")
# print(get('http://localhost:8080/api/users/апапрпр').json())

# # без параметров
# print(post('http://localhost:8080/api/users', json={}).json())
#
# # верный запрос
# print(post('http://localhost:8080/api/users',
#            json={'surname': "L",
#                  'name': 'l',
#                  'age': 17,
#                  'position': 'developer',
#                  'speciality': 'no',
#                  'address': 'module',
#                  'email': 'fgh@fgg.tt'}).json())

# мало параметров
# print(post('http://localhost:8080/api/users',
#            json={'surname': "L",
#                  'name': 'l'}).json())

# неуникальный email
# print(post('http://localhost:8080/api/users',
#            json={'surname': "L",
#                  'name': 'l',
#                  'age': 17,
#                  'position': 'developer',
#                  'speciality': 'no',
#                  'address': 'module',
#                  'email': 'fgh@fgg.tt'}).json())

# верный запрос
print(delete('http://localhost:8080/api/users/3', json={}).json())



# несуществующий id
print(delete('http://localhost:8080/api/users/100', json={}).json())