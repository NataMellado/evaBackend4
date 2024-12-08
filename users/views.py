from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import json, requests

# Vista de la página principal
def index(request):
    return render(request, 'index.html')

# Vista de la página de registro
def register(request):
    
    if request.method == 'POST':
        print("SE HIZO POST...")
        new_user_nombre = request.POST.get('nombre')
        new_user_apellidos = request.POST.get('apellidos')
        new_user_edad = request.POST.get('edad')
        new_user_fecha_nacimiento = request.POST.get('fecha_nacimiento')
        new_user_telefono = request.POST.get('telefono')
        new_user_email = request.POST.get('email')
        new_user_cant_visitas = request.POST.get('cant_visitas')
        
        req = requests.post('http://localhost:8001/api/pacientes/', data = {
            "nombre":new_user_nombre,
            "apellidos":new_user_apellidos,
            "edad":new_user_edad,
            "fecha_nacimiento":new_user_fecha_nacimiento,
            "telefono":new_user_telefono,
            "email":new_user_email,
            "cant_visitas":new_user_cant_visitas,
        })
        
        if req.status_code != 200:
            print("Error al guardar usuario")
            messages.error(request, f'No se puede guardar este usuario. (Error en:{req.text})')
            return redirect('register')
        
        print("Usuario registrado")
        messages.success(request, 'Usuario registrado exitosamente!')
        redirect('users_list')
        
    
    return render(request, 'register.html')

# Vista de la lista de usuarios
def users_list(request):
    message = request.GET.get('message')
    if message == 'error':
        messages.error(request, 'No se puede guardar este usuario.')    
    # return render(request, 'users_list.html')
        
    if request.method == 'POST': 
        try:
            eliminar = request.POST.get('deleteUser')
            
                
            if eliminar:
                user = User.objects.get(id=eliminar)
                req = requests.delete(f'http://localhost:8001/api/pacientes/{eliminar}/')
        
                if req.status_code != 200:
                    print("Error al eliminar usuario")
                    messages.error(request, f'No se puede eliminar este usuario. (Error en:{req.text})')
                
                print("Usuario eliminado")
                messages.success(request, 'Usuario eliminado exitosamente!')
            else:
            
                new_user_id = request.POST.get('userId')
                new_user_nombre = request.POST.get('nombre')
                new_user_apellidos = request.POST.get('apellidos')
                new_user_edad = request.POST.get('edad')
                new_user_fecha_nacimiento = request.POST.get('fecha_nacimiento')
                new_user_telefono = request.POST.get('telefono')
                new_user_email = request.POST.get('email')
                new_user_cant_visitas = request.POST.get('cant_visitas')

                print("Info obtenida:")
                print(new_user_nombre)
                print(new_user_apellidos)
                print(new_user_edad)
                print(new_user_fecha_nacimiento)
                print(new_user_telefono)
                print(new_user_email)
                print(new_user_cant_visitas)
                
                user = User.objects.get(id=new_user_id)
                user.nombre = new_user_nombre
                user.apellidos = new_user_apellidos
                user.edad = new_user_edad
                user.fecha_nacimiento = new_user_fecha_nacimiento
                user.telefono = new_user_telefono
                user.email = new_user_email
                user.cant_visitas = new_user_cant_visitas
                user.save()
                messages.success(request, 'Usuario modificado exitosamente!')
        
        except Exception as e:
            print(e)
            messages.error(request, 'Hubo un error!')

    users = requests.get('http://localhost:8001/api/pacientes/')
    users_to_json = users.json()
    users_data = []
    print(users_to_json)
    for paciente in users_to_json:
        nuevo_usuario = User(
            id = paciente['id'],
            nombre = paciente['nombre'],
            apellidos = paciente['apellidos'],
            edad = paciente['edad'],
            fecha_nacimiento = paciente['fecha_nacimiento'],
            telefono = paciente['telefono'],
            email = paciente['email'],
            cant_visitas = paciente['cant_visitas'],
        )
        users_data.append(nuevo_usuario)
    print(users_data)
    return render(request, 'users_list.html', {'users': users_data, 'users_to_json': users_to_json})
