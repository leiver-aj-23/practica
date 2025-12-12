
from django.http import HttpResponse
import unicodedata

# Create your views here.
from django.shortcuts import render, redirect
from .models import Practica
from .models import Prestamo, Libro

def saludo(request):
    return HttpResponse("Hola Mundo")

def vista(request):
    return render(request, "anime.html")

def lala(request):
    return render(request, "index.html")

def home_biblioteca(request):
    # Verificar si el usuario está logueado
    if 'user_id' not in request.session:
        return redirect("login")

    # Obtener datos de libros desde la base de datos
    libros_qs = Libro.objects.all()

    # Convertir a lista de dicts compatible con plantillas existentes
    libros = [
        {
            'id': b.id,
            'titulo': b.titulo,
            'autor': b.autor or '',
            'descripcion': b.descripcion or b.resumen or '',
            'resumen': b.resumen or '',
            'editorial': b.editorial or '',
            'año': b.año,
            'categoria': b.categoria or 'Libros',
            'imagen_url': b.imagen_url or '',
            'stock': b.stock or 0,
        }
        for b in libros_qs
    ]

    # Obtener categoría seleccionada
    categoria_seleccionada = request.GET.get('categoria', 'Libros')

    # Normalizador para búsqueda insensible a mayúsculas y acentos
    def _normalize(text):
        if not text:
            return ''
        try:
            s = str(text)
        except Exception:
            s = ''
        s = unicodedata.normalize('NFKD', s)
        s = s.encode('ASCII', 'ignore').decode('ASCII')
        return s.lower()

    # Manejar búsqueda (parámetro `q`). Si se provee `q`, buscar en TODOS los libros
    # (no limitar por categoría). Si no hay `q`, filtrar por categoría seleccionada.
    q = request.GET.get('q', '').strip()
    if q:
        q_norm = _normalize(q)
        libros_filtrados = [
            l for l in libros
            if q_norm in _normalize(l.get('titulo', ''))
            or q_norm in _normalize(l.get('autor', ''))
            or q_norm in _normalize(l.get('descripcion', ''))
        ]
    else:
        # Filtrar libros por categoría cuando no hay búsqueda
        libros_filtrados = [l for l in libros if l['categoria'] == categoria_seleccionada]

    # Obtener categorías únicas
    categorias = ['Libros', 'Carrera laboral', 'Matemáticas', 'Tecnología e informática', 
                  'Arte y humanidades', 'Música', 'Educación y pedagogía', 
                  'Religión y espiritualismo', 'Administración y gestión personal']

    username = request.session.get('username', 'Usuario')
    primera_letra = username[0].upper() if username else 'U'

    info = {
        'libros': libros_filtrados,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'username': username,
        'primera_letra': primera_letra
    }

    return render(request, "home_biblioteca.html", info)


# Make an in-memory books store that persists while the server runs.
# This is temporary; for production add a `Libro` model and persist to DB.
BOOKS = [
    {
        'id': 1,
        'titulo': 'Cien años de soledad',
        'autor': 'Gabriel García Márquez',
        'descripcion': 'La novela que revolucionó la literatura mundial. Una historia épica de varias generaciones en el mítico pueblo de Macondo.',
        'resumen': 'La novela sigue la historia de la familia Buendía a lo largo de siete generaciones en Macondo.',
        'editorial': 'Editorial Sudamericana',
        'año': 1967,
        'categoria': 'Libros',
        'imagen_url': '/static/img/cien_anos.jpg',
        'stock': 3
    },
    {
        'id': 2,
        'titulo': '1984',
        'autor': 'George Orwell',
        'descripcion': 'Una distopía que nos hace reflexionar sobre el futuro de la humanidad y la libertad en una sociedad totalitaria.',
        'resumen': 'Sociedad totalitaria controlada por el Gran Hermano.',
        'editorial': 'Secker & Warburg',
        'año': 1949,
        'categoria': 'Libros',
        'imagen_url': '/static/img/1984.jpg',
        'stock': 0
    },
    {
        'id': 3,
        'titulo': 'Don Quijote',
        'autor': 'Miguel de Cervantes',
        'descripcion': 'La obra maestra de la literatura española. Las aventuras del caballero más famoso de la literatura mundial.',
        'resumen': 'Las aventuras del ingenioso hidalgo Don Quijote y su escudero Sancho.',
        'editorial': 'Francisco de Robles',
        'año': 1605,
        'categoria': 'Libros',
        'imagen_url': '',
        'stock': 2
    },
    {
        'id': 4,
        'titulo': 'El Principito',
        'autor': 'Antoine de Saint-Exupéry',
        'descripcion': 'Una fábula poética sobre la amistad, el amor y la importancia de lo esencial en la vida.',
        'resumen': 'Un piloto perdido conoce a un pequeño príncipe que viene de otro planeta.',
        'editorial': 'Reynal & Hitchcock',
        'año': 1943,
        'categoria': 'Arte y humanidades',
        'imagen_url': '/static/img/principito.jpg',
        'stock': 1
    },
    {
        'id': 5,
        'titulo': 'Orgullo y Prejuicio',
        'autor': 'Jane Austen',
        'descripcion': 'Una novela de romance y crítica social ambientada en la Inglaterra georgiana con personajes memorables.',
        'resumen': 'La relación entre Elizabeth Bennet y el señor Darcy.',
        'editorial': 'T. Egerton',
        'año': 1813,
        'categoria': 'Libros',
        'imagen_url': '',
        'stock': 1
    },
    {
        'id': 6,
        'titulo': 'Crimen y Castigo',
        'autor': 'Fiódor Dostoyevski',
        'descripcion': 'Una exploración profunda de la psicología humana y la moral en la Rusia del siglo XIX.',
        'resumen': 'La historia de Raskólnikov, un joven que comete un crimen y enfrenta las consecuencias morales.',
        'editorial': 'The Russian Messenger',
        'año': 1866,
        'categoria': 'Carrera laboral',
        'imagen_url': '',
        'stock': 0
    },
    {
        'id': 7,
        'titulo': 'Cálculo Integral',
        'autor': 'James Stewart',
        'descripcion': 'Tratado completo sobre cálculo integral con ejercicios prácticos y aplicaciones reales.',
        'resumen': 'Libro de texto de cálculo con teoria y ejercicios.',
        'editorial': 'Cengage Learning',
        'año': 2015,
        'categoria': 'Matemáticas',
        'imagen_url': '',
        'stock': 2
    },
    {
        'id': 8,
        'titulo': 'Python para Principiantes',
        'autor': 'Mark Lutz',
        'descripcion': 'Guía completa para aprender programación en Python desde cero con ejemplos prácticos.',
        'resumen': 'Guía de introducción a Python con ejemplos y ejercicios.',
        'editorial': "O'Reilly Media",
        'año': 2020,
        'categoria': 'Tecnología e informática',
        'imagen_url': '',
        'stock': 1
    },
]


def get_libros():
    return BOOKS


def detalle_libro(request, book_id):
    if 'user_id' not in request.session:
        return redirect('login')

    libros = get_libros()
    libro = next((l for l in libros if l['id'] == book_id), None)
    if not libro:
        return redirect('home_biblioteca')

    return render(request, 'detalle_libro.html', {'libro': libro})


def prestar_libro(request, book_id):
    # Mostrar formulario de préstamo y procesar la solicitud
    if 'user_id' not in request.session:
        return redirect('login')

    libros = get_libros()
    libro = next((l for l in libros if l['id'] == book_id), None)
    if not libro:
        return redirect('home_biblioteca')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        documento = request.POST.get('documento')
        dias = request.POST.get('dias')

        # Validaciones sencillas
        error = None
        if not nombre or not telefono or not documento or not dias:
            error = 'Todos los campos son obligatorios.'
            return render(request, 'prestar_libro.html', {'libro': libro, 'error': error, 'form': request.POST})

        # Comprobar disponibilidad (stock)
        try:
            stock = int(libro.get('stock', 0))
        except Exception:
            stock = 0

        if stock > 0:
            # Aprobado
            return redirect('/home-biblioteca/?prestamo=aprobado')
        else:
            # Denegado por material insuficiente
            return redirect('/home-biblioteca/?prestamo=denegado')

    return render(request, 'prestar_libro.html', {'libro': libro})


def prestar_libro(request, book_id):
    if 'user_id' not in request.session:
        return redirect('login')

    libros = get_libros()
    libro = next((l for l in libros if l['id'] == book_id), None)
    if not libro:
        return redirect('home_biblioteca')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        documento = request.POST.get('documento')
        dias = request.POST.get('dias')

        # Validaciones básicas
        if not nombre or not telefono or not documento or not dias:
            error = 'Por favor completa todos los campos.'
            return render(request, 'prestar_libro.html', {'libro': libro, 'error': error, 'form': request.POST})

        try:
            dias_int = int(dias)
            if dias_int <= 0:
                raise ValueError()
        except Exception:
            error = 'Ingresa un número válido de días.'
            return render(request, 'prestar_libro.html', {'libro': libro, 'error': error, 'form': request.POST})

        # Guardar préstamo
        prestamo = Prestamo.objects.create(
            book_id=libro['id'],
            book_title=libro['titulo'],
            borrower_name=nombre,
            phone=telefono,
            document_number=documento,
            days=dias_int
        )

        return redirect('confirmar_prestamo', prestamo_id=prestamo.id)

    return render(request, 'prestar_libro.html', {'libro': libro})


def confirmar_prestamo(request, prestamo_id):
    if 'user_id' not in request.session:
        return redirect('login')

    try:
        prestamo = Prestamo.objects.get(id=prestamo_id)
    except Prestamo.DoesNotExist:
        return redirect('home_biblioteca')

    return render(request, 'prestar_confirm.html', {'prestamo': prestamo})

def login(request):
    if request.method == "POST":
        usern = request.POST.get("username")
        passw = request.POST.get("password")
        # Shortcut admin user: allow admin/12345 even if not in DB
        if usern == 'admin' and passw == '12345':
            usuario, created = Practica.objects.get_or_create(
                username='admin', defaults={'password': '12345'}
            )
            request.session['user_id'] = usuario.id
            request.session['username'] = usuario.username
            request.session['is_admin'] = True
            return redirect('home_biblioteca')

        try:
            usuario = Practica.objects.get(username=usern, password=passw)
            request.session['user_id'] = usuario.id
            request.session['username'] = usuario.username
            # Mark admin if username matches admin conventions
            is_admin = False
            if usuario.username and (usuario.username == 'admin' or usuario.username.lower().endswith('@administrador.com')):
                is_admin = True
            request.session['is_admin'] = is_admin
            return redirect("home_biblioteca")
        except Practica.DoesNotExist:
            sms = "Usuario o contraseña incorrectos"
            return render(request, "login_nuevo.html", {'error': sms})
    
    return render(request, "login_nuevo.html")


def admin_login(request):
    """Login para administradores. Requiere que el username termine en @administrador.com"""
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        # Validar que el usuario tenga el dominio administrador
        if not usern or not usern.lower().endswith('@administrador.com'):
            return render(request, 'admin_login.html', {'error': 'Credenciales inválidas'})

        try:
            usuario = Practica.objects.get(username=usern, password=passw)
            # Marca la sesión como admin
            request.session['user_id'] = usuario.id
            request.session['username'] = usuario.username
            request.session['is_admin'] = True
            return redirect('home_biblioteca')
        except Practica.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'admin_login.html')


def manage_books(request):
    # Only admins can access management pages
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    libros_qs = Libro.objects.all()
    return render(request, 'manage_books.html', {'libros': libros_qs})


def add_book(request):
    # Only admins can add books
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    if request.method == 'POST':
        imagen_url = request.POST.get('imagen_url', '').strip()
        titulo = request.POST.get('titulo', '').strip()
        autor = request.POST.get('autor', '').strip()
        editorial = request.POST.get('editorial', '').strip()
        resumen = request.POST.get('resumen', '').strip()
        año_str = request.POST.get('año', '').strip()
        categoria = request.POST.get('categoria', 'Libros').strip()
        try:
            año = int(año_str) if año_str else None
        except Exception:
            año = None

        libro = Libro.objects.create(
            titulo=titulo,
            autor=autor,
            descripcion=resumen,
            resumen=resumen,
            editorial=editorial,
            año=año,
            categoria=categoria,
            imagen_url=imagen_url,
            stock=0,
        )
        return redirect('manage_books')

    return render(request, 'add_book.html')


def modify_book(request, book_id):
    # Only admins can modify books
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    try:
        libro_obj = Libro.objects.get(id=book_id)
    except Libro.DoesNotExist:
        return redirect('manage_books')

    if request.method == 'POST':
        libro_obj.titulo = request.POST.get('titulo', libro_obj.titulo)
        libro_obj.autor = request.POST.get('autor', libro_obj.autor)
        libro_obj.descripcion = request.POST.get('descripcion', libro_obj.descripcion)
        libro_obj.editorial = request.POST.get('editorial', libro_obj.editorial)
        año = request.POST.get('año')
        libro_obj.año = int(año) if año and año.isdigit() else libro_obj.año
        libro_obj.categoria = request.POST.get('categoria', libro_obj.categoria)
        libro_obj.imagen_url = request.POST.get('imagen_url', libro_obj.imagen_url)
        try:
            libro_obj.stock = int(request.POST.get('stock', libro_obj.stock))
        except Exception:
            pass
        libro_obj.save()
        return redirect('manage_books')

    return render(request, 'modify_book.html', {'libro': libro_obj})


def delete_book(request, book_id):
    # Only admins can delete books
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    try:
        libro = Libro.objects.get(id=book_id)
        libro.delete()
    except Libro.DoesNotExist:
        pass
    return redirect('manage_books')

def usuarios(request):
    if 'user_id' not in request.session:
        return redirect("login")
    
    todos_usuarios = Practica.objects.all()
    info = {
        'usuarios': todos_usuarios,
        'username_actual': request.session.get('username')
    }
    return render(request, "usuarios.html", info)

def eliminar_usuario(request, user_id):
    if 'user_id' not in request.session:
        return redirect("login")
    
    try:
        usuario = Practica.objects.get(id=user_id)
        usuario.delete()
    except Practica.DoesNotExist:
        pass
    
    return redirect("usuarios")

def actualizar_usuario(request, user_id):
    if 'user_id' not in request.session:
        return redirect("login")
    
    try:
        usuario = Practica.objects.get(id=user_id)
    except Practica.DoesNotExist:
        return redirect("usuarios")
    
    if request.method == "POST":
        username = request.POST.get("username")
        imagen_url = request.POST.get("imagen_url")
        
        if username and username != usuario.username:
            if Practica.objects.filter(username=username).exists():
                info = {
                    'usuario': usuario,
                    'error': 'El nombre de usuario ya existe'
                }
                return render(request, "actualizar.html", info)
        
        usuario.username = username
        usuario.imagen_url = imagen_url
        usuario.save()
        return redirect("usuarios")
    
    info = {'usuario': usuario}
    return render(request, "actualizar.html", info)

def formulario(request):
    if request.method == "POST":
        usern = request.POST.get("username")
        passw1 = request.POST.get("password1")
        passw2 = request.POST.get("password2")

        if Practica.objects.filter(username=usern).exists():
            sms = "El nombre de usuario ya existe"
            sms2 = "Por favor, elige otro nombre de usuario"
            
            info = {
                  'infosms':sms,
                  'infosms2':sms2
            }
            return render(request, "register.html", info)
        # Validación básica
        if passw1 == passw2:
            # Guardar en la base de datos
            imagen_url = request.POST.get("imagen_url", "")
            Practica.objects.create(
                username=usern,
                password=passw2,
                imagen_url=imagen_url
            )
            # Redirigir al login para que el usuario inicie sesión manualmente
            return redirect("login")
    return render(request, "register.html")


def delete_books(request):
    """List all books with delete option"""
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    libros_qs = Libro.objects.all()
    return render(request, 'delete_books.html', {'libros': libros_qs})


def search_modify_book(request):
    """Search for a book to modify, then edit the 5 fields"""
    if 'user_id' not in request.session or not request.session.get('is_admin'):
        return redirect('home_biblioteca')
    libro_obj = None
    search_query = request.GET.get('q', '').strip()

    # If search query provided, find the first matching Libro by title or author
    if search_query:
        libros_found = Libro.objects.filter(titulo__icontains=search_query) | Libro.objects.filter(autor__icontains=search_query)
        libro_obj = libros_found.first()

    # If POST (editing the book)
    if request.method == 'POST' and libro_obj:
        libro_id = request.POST.get('id')
        if libro_id and str(libro_obj.id) == str(libro_id):
            libro_obj.imagen_url = request.POST.get('imagen_url', libro_obj.imagen_url).strip()
            libro_obj.titulo = request.POST.get('titulo', libro_obj.titulo).strip()
            libro_obj.autor = request.POST.get('autor', libro_obj.autor).strip()
            libro_obj.editorial = request.POST.get('editorial', libro_obj.editorial).strip()
            libro_obj.categoria = request.POST.get('categoria', libro_obj.categoria).strip()
            libro_obj.resumen = request.POST.get('resumen', libro_obj.resumen).strip()
            libro_obj.descripcion = libro_obj.resumen
            libro_obj.save()
        return redirect('search_modify_book')

    return render(request, 'search_modify_book.html', {'libro': libro_obj, 'search_query': search_query})


def logout_view(request):
    # Eliminar la sesión del usuario y redirigir al login nuevo
    try:
        request.session.flush()
    except Exception:
        pass
    return redirect('login')

