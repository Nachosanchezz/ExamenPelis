# 🚀 Proyecto: Nacho's Netflix

## 🌟 Descripción
Este proyecto es una plataforma que permite a los usuarios explorar contenido dinámico y gestionar listas personalizadas.

## ⚙️ Funcionalidades
- Buscar contenido de manera rápida.
- Sistema de autenticación para usuarios.
- Agregar y gestionar listas personalizadas.

## 🛠️ Tecnologías utilizadas
- **Backend**: Django
- **Frontend**: HTML5, CSS3
- **Base de datos**: SQLite
- **API**: TMDB (The Movie Database)

## 🛠️ Instalación
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/Nachosanchezz/ExamenPelis.git
   cd netflix

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Instala las dependencias:
  ```bash
     pip install -r requirements.txt
```

4. Configura las variables de entorno .env:
  ```plaintext
     TMDB_API_KEY = tu_api_key
     SECRET_KEY = tu_clave_secreta
```
5. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
6. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```
   
7. Accede al proyecto:
   Abre tu navegador y ve a ```http://127.0.0.1:8000 ```

## 📋 Funcionalidades implementadas
- Registro e inicio de sesión.
- Visualización de contenido popular desde TMBD.
- Agregar listas personalizadas

## 👤 Autor
- Github: Nachosanchezz
- Link repositorio: https://github.com/Nachosanchezz/ExamenPelis.git



