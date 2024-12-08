from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import json, requests

# Vista de la página principal
def index(request):
    return render(request, 'index.html')

def procesar_error(error):
    print("Error:")
    print(error)
    errores_data = json.loads(error)
    print(errores_data)
    mensajes_error = []
    for campo, errores in errores_data.items():
        for error in errores:
            mensajes_error.append(f"{campo.capitalize()}: {error}")

    mensaje_final = "Error en campo(s):\n" + "\n".join(f"[{msj}]" for msj in mensajes_error)
    print(mensaje_final)
    return mensaje_final
    
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
        
        if req.status_code != 200 and req.status_code != 201 and req.status_code != 204:
            print("Error al registrar paciente")
            messages.error(request, f'No se puede registrar este paciente. ({procesar_error(req.text)})')
            return redirect('register')
        else:
            print("Paciente registrado")
            messages.success(request, 'Paciente registrado exitosamente!')
        
        redirect('users_list')
        
    
    return render(request, 'register.html')

# Vista de la lista de usuarios
def users_list(request):
    
    # Capturar los parámetros de la URL
    query_params = request.GET.urlencode() 
        
    if request.method == 'POST': 
        try:
            eliminar = request.POST.get('deleteUser')
                
            if eliminar:        
                req = requests.delete(f'http://localhost:8001/api/pacientes/{eliminar}/')
        
                if req.status_code != 200 and req.status_code != 201 and req.status_code != 204:
                    print("Error al eliminar paciente")
                    messages.error(request, f'No se puede eliminar este paciente. ({procesar_error(req.text)})')
                else:
                    print("Paciente eliminado")
                    messages.success(request, 'Paciente eliminado exitosamente!')
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
                
                req = requests.put(f'http://localhost:8001/api/pacientes/{new_user_id}/', data = {
                    "nombre":new_user_nombre,
                    "apellidos":new_user_apellidos,
                    "edad":new_user_edad,
                    "fecha_nacimiento":new_user_fecha_nacimiento,
                    "telefono":new_user_telefono,
                    "email":new_user_email,
                    "cant_visitas":new_user_cant_visitas,
                })
        
                if req.status_code != 200 and req.status_code != 201 and req.status_code != 204:
                    print("Error al modificar paciente")
                    messages.error(request, f'No se puede modificar este paciente. ({procesar_error(req.text)})')
                else:
                    print("Paciente modificado")
                    messages.success(request, 'Paciente modificado exitosamente!')
        
        except Exception as e:
            print(e)
            messages.error(request, 'Hubo un error!')
            
    # Construir la URL de la API con filtros si los hay
    api_url = 'http://localhost:8001/api/pacientes/'
    if query_params:
        api_url += f'?{query_params}'
        
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        users_to_json = response.json()
        users_data = []

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
            
  
    except requests.exceptions.RequestExeption as e:
        print(f"Error al consultar la API: {e}")
        messages.error(request, 'Hubo un error al consultar la lista de pacientes.')
        users_data = []
        users_to_json = []
    
    print(users_data)
    return render(request, 'users_list.html', {'users': users_data, 'users_to_json': users_to_json})
