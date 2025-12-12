from miapp.models import Practica

username = 'admin'
password = '12345'

obj, created = Practica.objects.get_or_create(username=username, defaults={'password': password})
if created:
    print(f"Usuario '{username}' creado con contraseña '{password}'")
else:
    obj.password = password
    obj.save()
    print(f"Usuario '{username}' ya existía. Contraseña actualizada a '{password}'")
