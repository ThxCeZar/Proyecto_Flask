#*
import bcrypt
import json

usuarios = [
    {"username": "", "password": ""},
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