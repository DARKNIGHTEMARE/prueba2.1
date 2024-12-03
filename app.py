from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"  

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="universidad2"
)



# Inicio formulario/Reportes de estudiantes

@app.route('/formulario')
def formulario():
    return render_template('formu.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    nif = request.form.get('nif')
    nombre = request.form.get('nombre')  
    apellido = request.form.get('apellido') 
    direccion_postal = request.form.get('direccion_postal') 
    telefono = request.form.get('telefono') 
    direccion_electronica = request.form.get('direccion_electronica') 
    beca = request.form.get('beca') 

    cursor = db.cursor()
    sql = """
    INSERT INTO alumno (nif, nombre, apellido, direccion_postal, telefono, direccion_electronica, beca)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nif, nombre, apellido, direccion_postal, telefono, direccion_electronica, beca)

    try:
        cursor.execute(sql, valores)
        db.commit()  
        return redirect(url_for('formulario'))
    except mysql.connector.Error as err:
        db.rollback()  
        return f"Error al guardar los datos: {err}"
    finally:
        cursor.close()  

@app.route('/reporte')
def reporte():
    try:
        cursor = db.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM alumno")
        alumnos = cursor.fetchall()  
        cursor.close()
        return render_template('reporte.html', alumnos=alumnos)
    except mysql.connector.Error as err:
        print(f"Error al consultar los datos: {err}")
        return "Error al consultar los datos"

@app.route('/eliminar_alumno/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM alumno WHERE id = %s", (id,))
        db.commit()
        return redirect(url_for('reporte'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al eliminar el alumno: {err}"
    finally:
        cursor.close()

@app.route('/editar_alumno/<int:id>', methods=['POST'])
def editar_alumno(id):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    direccion_postal = request.form.get('direccion_postal')
    telefono = request.form.get('telefono')
    direccion_electronica = request.form.get('direccion_electronica')
    beca = request.form.get('beca')

    sql = """
    UPDATE alumno SET nombre = %s, apellido = %s, direccion_postal = %s, telefono = %s,
    direccion_electronica = %s, beca = %s WHERE id = %s
    """
    valores = (nombre, apellido, direccion_postal, telefono, direccion_electronica, beca, id)

    cursor = db.cursor()
    try:
        cursor.execute(sql, valores)
        db.commit()
        return redirect(url_for('reporte'))  
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al actualizar los datos: {err}"
    finally:
        cursor.close()

# Fin formulario/Reportes de estudiantes

# Inicio formulario/Reportes de profesor

@app.route('/formulario_profesor')
def formulario_profesor():
    return render_template('formuprofe.html')

@app.route('/submit_profesor', methods=['POST'])
def submit_profesor():
    id_p = request.form.get('id_p')  
    nombre_p = request.form.get('nombre_p')  
    apellido_p = request.form.get('apellido_p') 
    ocupacion_p = request.form.get('ocupacion_p') 
    direccion_postal_p = request.form.get('direccion_postal_p') 
    telefono_p = request.form.get('telefono_p') 
    direccion_electronica_p = request.form.get('direccion_electronica_p') 

    cursor = db.cursor()
    sql = """
    INSERT INTO profesores (id_p, nombre_p, apellido_p, ocupacion_p, direccion_postal_p, telefono_p, direccion_electronica_p)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valoresp = (id_p, nombre_p, apellido_p, ocupacion_p, direccion_postal_p, telefono_p, direccion_electronica_p)

    try:
        cursor.execute(sql, valoresp)
        db.commit()  
        return redirect(url_for('formulario_profesor'))
    except mysql.connector.Error as err:
        db.rollback()  
        return f"Error al guardar los datos: {err}"
    finally:
        cursor.close()

@app.route('/reporte_profesor')
def reporte_profesor():
    try:
        cursor = db.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM profesores")
        profesoress = cursor.fetchall()  
        cursor.close()
        return render_template('reporteprofe.html', profesoress=profesoress)
    except mysql.connector.Error as err:
        print(f"Error al consultar los datos: {err}")
        return "Error al consultar los datos"

# Eliminar Profesor
@app.route('/eliminar_profesor/<int:id>', methods=['POST'])
def eliminar_profesor(id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM profesores WHERE id_p = %s", (id,))
        db.commit()
        return redirect(url_for('reporte_profesor'))  
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al eliminar el profesor: {err}"
    finally:
        cursor.close()

# Editar Profesor
@app.route('/editar_profesor/<int:id>', methods=['GET', 'POST'])
def editar_profesor(id):
    if request.method == 'POST':
        nombre_p = request.form.get('nombre_p')
        apellido_p = request.form.get('apellido_p')
        ocupacion_p = request.form.get('ocupacion_p')
        direccion_postal_p = request.form.get('direccion_postal_p')
        telefono_p = request.form.get('telefono_p')
        direccion_electronica_p = request.form.get('direccion_electronica_p')

        sql = """
        UPDATE profesores SET nombre_p = %s, apellido_p = %s, ocupacion_p = %s, direccion_postal_p = %s, 
        telefono_p = %s, direccion_electronica_p = %s WHERE id_p = %s
        """
        valores_p = (nombre_p, apellido_p, ocupacion_p, direccion_postal_p, telefono_p, direccion_electronica_p, id)

        cursor = db.cursor()
        try:
            cursor.execute(sql, valores_p)
            db.commit()
            return redirect(url_for('reporte_profesor'))
        except mysql.connector.Error as err:
            db.rollback()
            return f"Error al actualizar los datos: {err}"
        finally:
            cursor.close()

    else:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM profesores WHERE id_p = %s", (id,))
        profesor = cursor.fetchone()
        cursor.close()

        if profesor:
            return render_template('editar_profesor.html', profesor=profesor)
        else:
            return "Profesor no encontrado", 404

# Fin formulario/Reportes de profesor

# Inicio formulario/Reportes de asignatura

@app.route('/formulario_asignatura')
def formulario_asignatura():
    return render_template('formuasig.html')

@app.route('/submit_asignatura', methods=['POST'])
def submit_asignatura():
    id_a = request.form.get('id_a')
    codigo_a = request.form.get('codigo_a')
    nombre_a = request.form.get('nombre_a')
    creditos_a = request.form.get('creditos_a')
    cuatrimestre_a = request.form.get('cuatrimestre_a')
    caracter_a = request.form.get('caracter_a')

    cursor = db.cursor()
    sql = """
    INSERT INTO asignatura (id_a, codigo_a, nombre_a, creditos_a, cuatrimestre_a, caracter_a)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valoresa = (id_a, codigo_a, nombre_a, creditos_a, cuatrimestre_a, caracter_a)

    try:
        cursor.execute(sql, valoresa)
        db.commit()
        return redirect(url_for('formulario_asignatura'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al guardar los datos: {err}"
    finally:
        cursor.close()

# Reporte de asignatura
@app.route('/reporte_asignatura')
def reporte_asignatura():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM asignatura")
        asignaturas = cursor.fetchall()
        cursor.close()
        return render_template('reporteasig.html', asignaturas=asignaturas)
    except mysql.connector.Error as err:
        print(f"Error al consultar los datos: {err}")
        return "Error al consultar los datos"

# Eliminar la asignatura
@app.route('/eliminar_asignatura/<int:id>', methods=['POST'])
def eliminar_asignatura(id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM asignatura WHERE id_a = %s", (id,))
        db.commit()
        return redirect(url_for('reporte_asignatura'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al eliminar la asignatura: {err}"
    finally:
        cursor.close()

# Editar la asignatura
@app.route('/editar_asignatura/<int:id>', methods=['GET', 'POST'])
def editar_asignatura(id):
    if request.method == 'POST':
        codigo_a = request.form.get('codigo_a')
        nombre_a = request.form.get('nombre_a')
        creditos_a = request.form.get('creditos_a')
        cuatrimestre_a = request.form.get('cuatrimestre_a')
        caracter_a = request.form.get('caracter_a')

        sql = """
        UPDATE asignatura
        SET codigo_a = %s, nombre_a = %s, creditos_a = %s, cuatrimestre_a = %s, caracter_a = %s
        WHERE id_a = %s
        """
        valores_a = (codigo_a, nombre_a, creditos_a, cuatrimestre_a, caracter_a, id)

        cursor = db.cursor()
        try:
            cursor.execute(sql, valores_a)
            db.commit()
            cursor.close()
            return redirect(url_for('reporte_asignatura'))
        except mysql.connector.Error as err:
            db.rollback()
            cursor.close()
            return f"Error al actualizar los datos: {err}"
    else:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM asignatura WHERE id_a = %s", (id,))
        asignatura = cursor.fetchone()
        cursor.close()

        if asignatura:
            return render_template('editar_asignatura.html', asignatura=asignatura)
        else:
            return "Asignatura no encontrada", 404

# Fin formulario/Reportes de asignatura

# Inicio formulario/Reportes de curso

@app.route('/formulario_curso')
def formulario_curso():
    return render_template('formcurso.html')

@app.route('/submit_curso', methods=['POST'])
def submit_curso():
    id_c = request.form.get('id_c')
    codigo_c = request.form.get('codigo_c')
    nombre_c = request.form.get('nombre_c')

    cursor = db.cursor()
    sql = """
    INSERT INTO curso (id_c, codigo_c, nombre_c)
    VALUES (%s, %s, %s)
    """
    valores_c = (id_c, codigo_c, nombre_c)

    try:
        cursor.execute(sql, valores_c)
        db.commit()
        return redirect(url_for('formulario_curso'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al guardar los datos: {err}"
    finally:
        cursor.close()

@app.route('/reporte_curso')
def reporte_curso():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curso")
        cursos = cursor.fetchall() 
        cursor.close()
        return render_template('reportecurso.html', cursos=cursos)
    except mysql.connector.Error as err:
        print(f"Error al consultar los datos: {err}")
        return "Error al consultar los datos"

@app.route('/eliminar_curso/<int:id>', methods=['POST'])
def eliminar_curso(id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM curso WHERE id_c = %s", (id,))
        db.commit()
        return redirect(url_for('reporte_curso'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al eliminar el curso: {err}"
    finally:
        cursor.close()

@app.route('/editar_curso/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    if request.method == 'POST':
        codigo_c = request.form.get('codigo_c')
        nombre_c = request.form.get('nombre_c')

        sql = """
        UPDATE curso
        SET codigo_c = %s, nombre_c = %s
        WHERE id_c = %s
        """
        valores_c = (codigo_c, nombre_c, id)

        cursor = db.cursor()
        try:
            cursor.execute(sql, valores_c)
            db.commit()
            cursor.close()
            return redirect(url_for('reporte_curso'))
        except mysql.connector.Error as err:
            db.rollback()
            cursor.close()
            return f"Error al actualizar los datos: {err}"
    else:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curso WHERE id_c = %s", (id,))
        curso = cursor.fetchone()
        cursor.close()

        if curso:
            return render_template('editar_curso.html', curso=curso)
        else:
            return "Curso no encontrado", 404

# Fin formulario/Reportes de curso




# inicio de matricula





@app.route('/add_matricula', methods=['GET', 'POST'])
def add_matricula():
    # Obtener todos los alumnos para mostrar en el formulario
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, apellido FROM alumno")
        alumnos = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as err:
        return redirect(url_for('index'))

    # Obtener todos los cursos para mostrarlos en el formulario
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id_c, nombre_c FROM curso")
        cursos = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as err:
        return redirect(url_for('index'))

    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        curso_id = request.form['curso_id']  # Asegúrate de que el nombre del campo sea 'curso_id'
        fecha_matricula = request.form['fecha_matricula']

        try:
            # Insertar la matrícula en la base de datos
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO matricula (alumno_id, curso_id, fecha_matricula)
                VALUES (%s, %s, %s)
            """, (alumno_id, curso_id, fecha_matricula))
            db.commit()
            cursor.close()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            db.rollback()
            return redirect(url_for('index'))

    return render_template('matricula.html', alumnos=alumnos, cursos=cursos)



@app.route('/reportematri')
def reportematri():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT matricula.id, alumno.nombre AS alumno_nombre, alumno.apellido AS alumno_apellido, 
                   curso.nombre_c AS curso_nombre, matricula.fecha_matricula
            FROM matricula 
            JOIN alumno ON matricula.alumno_id = alumno.id
            JOIN curso ON matricula.curso_id = curso.id_c
        """)
        matriculas = cursor.fetchall()
        cursor.close()
        return render_template('reportematri.html', matriculas=matriculas)
    except mysql.connector.Error as err:
        print(f"Error al consultar las matrículas: {err}")
        return f"Error al consultar las matrículas: {err}"



@app.route('/eliminar_matricula/<int:id>', methods=['POST'])
def eliminar_matricula(id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM matricula WHERE id = %s", (id,))
        db.commit()
        return redirect(url_for('reportematri'))
    except mysql.connector.Error as err:
        db.rollback()
        return f"Error al eliminar la matrícula: {err}"
    finally:
        cursor.close()







# fin de matricula





# Ruta principal para el login y registro
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'txtCorreo' in request.form and 'txtPassword' in request.form:
            # Registro de usuario
            correo = request.form.get('txtCorreo')
            password = request.form.get('txtPassword')

            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO usuarios (correo, password) VALUES (%s, %s)", (correo, password))  # Guardar la contraseña tal cual
                db.commit()
                cursor.close()
                return redirect(url_for('bienvenido'))  # Redirigir a la página de bienvenida
            except mysql.connector.IntegrityError:
                mensaje = "El correo ya está registrado"
                return render_template('index.html', mensaje=mensaje)

        elif 'txtCorreoLogin' in request.form and 'txtPasswordLogin' in request.form:
            # Login de usuario
            correo = request.form.get('txtCorreoLogin')
            password = request.form.get('txtPasswordLogin')

            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario = cursor.fetchone()
            cursor.close()

            # Verificar si la contraseña coincide exactamente con la almacenada
            if usuario and usuario['password'] == password:
                # Si la contraseña es correcta, redirigir a la página de bienvenida
                return redirect(url_for('bienvenido'))  
            else:
                mensaje = "Usuario o contraseña incorrectos"
                return render_template('index.html', mensaje=mensaje)
    
    return render_template('index.html')

# Ruta de bienvenida después de iniciar sesión
@app.route('/bienvenido')
def bienvenido():
    correo = request.args.get('correo')  # Obtener el correo desde los parámetros de la URL
    return render_template('bienvenido.html', correo=correo)  # Pasar el correo a la plantilla


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    return redirect(url_for('index'))  # Redirigir al login, sin usar sesión




@app.route('/reporte_usuarios')
def reporte_usuarios():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id_u, correo, password FROM usuarios")  # Consulta para obtener los usuarios
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('reporte_usuarios.html', usuarios=usuarios)  # Pasa los usuarios a la plantilla
    except mysql.connector.Error as err:
        print(f"Error al consultar los usuarios: {err}")
        return f"Error al consultar los usuarios: {err}"


@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_u = %s", (id,))
        db.commit()  # Confirmar la eliminación en la base de datos
        cursor.close()
        return redirect(url_for('reporte_usuarios'))  # Redirigir a la página de reporte de usuarios
    except mysql.connector.Error as err:
        print(f"Error al eliminar el usuario: {err}")
        return f"Error al eliminar el usuario: {err}"





if __name__ == '__main__':
    app.run(debug=True)
