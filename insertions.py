import os
import sys

# Agregar la ruta base del proyecto para que Python encuentre project4.settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE ANTES de importar módulos de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project4.settings')

import django
django.setup()

import random

from network.models import Post, User

# Crear superusuario
if not User.objects.filter(username='Admin').exists():
    User.objects.create_superuser('Admin', 'Admin@gmail.com', '12345678')

# Crear 20 usuarios
users = []
for i in range(1, 21):
    username = f'user{i}'
    email = f'user{i}@example.com'
    password = 'password'
    user = User.objects.create_user(username=username, email=email, password=password)
    users.append(user)

# Crear 20 posts
posts = []
for i in range(1, 21):
    user = random.choice(users)
    content = f'This is post number {i} by {user.username}'
    post = Post.objects.create(user=user, content=content)
    posts.append(post)

# Crear 40 likes (para que se generen duplicados)
for i in range(200):
    user = random.choice(users)
    post = random.choice(posts)
    post.likes.add(user)
    print(f'{user.username} liked post {post.id}')

# Hacer que los usuarios se sigan entre sí aleatoriamente
for user in users:
    following = random.sample(users, k=random.randint(1, 20))
    for follow in following:
        if follow != user:
            user.following.add(follow)

print("Database populated successfully!")