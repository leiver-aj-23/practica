from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.saludo, name='saludo'),
    # Main library views
    path('home-biblioteca/', views.home_biblioteca, name='home_biblioteca'),
    path('detalle/<int:book_id>/', views.detalle_libro, name='detalle_libro'),
    path('prestar/<int:book_id>/', views.prestar_libro, name='prestar_libro'),
    path('confirmar-prestamo/<int:prestamo_id>/', views.confirmar_prestamo, name='confirmar_prestamo'),

    # Admin / management
    path('manage-books/', views.manage_books, name='manage_books'),
    path('add-book/', views.add_book, name='add_book'),
    path('modify-book/<int:book_id>/', views.modify_book, name='modify_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),

    # Auth / users
    path('formulario/', views.formulario, name='formulario'),
    path('login/', views.login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),

    # User management
    path('usuarios/', views.usuarios, name='usuarios'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar'),
    path('actualizar/<int:user_id>/', views.actualizar_usuario, name='actualizar'),

    # Utilities
    path('delete-books/', views.delete_books, name='delete_books'),
    path('search-modify-book/', views.search_modify_book, name='search_modify_book'),
]

# Nota: las rutas originales que apuntaban a `views.vista` (anime.html)
# y `views.lala` (index.html) se han retirado porque las plantillas
# `anime.html` y `index.html` no existen en la carpeta `templates`.