curl -X POST http://127.0.0.1:8000/users/login/ \   
-H "Content-Type: application/json" \
-d '{"first_name": "usuario1", "password": "1234"}'

curl -X POST http://127.0.0.1:8000/users/registro/ \
-H "Content-Type: application/json" \
-d '{"first_name": "usuario1", "email": "usuario1@ejemplo.com", "password": "1234"}'