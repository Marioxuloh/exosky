curl -X POST http://127.0.0.1:8000/users/login/ \   
-H "Content-Type: application/json" \
-d '{"first_name": "usuario1", "password": "1234"}'

curl -X POST http://172.20.10.2:8000/users/login/ \
-H "Content-Type: application/json" \
-d '{"name": "marito"}'

curl -X GET http://127.0.0.1:8000/exoplanets/getall/