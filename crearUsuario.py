#*
import bcrypt
import json

usuarios = [
    {"username": "Kimmy", "password": "Kimmy0627@"},
    {"username": "Cesy", "password": "Cedi82430@@"},
    {"username": "ADMIN", "password": "Admin2025*"},
]

usuarios_hashed = []

for u in usuarios:
    hashed = bcrypt.hashpw(u["password"].encode('utf-8'), bcrypt.gensalt())
    usuarios_hashed.append({
        "username": u["username"],
        "password": hashed.decode('utf-8')
    })

with open('usuarios.json', 'w') as f:
    json.dump(usuarios_hashed, f, indent=4)

print("usuarios.json generado correctamente.")
#