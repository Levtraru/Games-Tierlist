from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

# app
app = Flask(__name__)
app.secret_key        = "ClaveSecreta"
# conexion mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = ''
app.config['MYSQL_DATABASE_DB']         = 'netflax'
mysql.init_app(app)

# MySQL Cursor
conn         = mysql.connect()
cursor       = conn.cursor()

# Referencia a la carpeta de subida de imagenes
CARPETA               = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

# Upload imagen
@app.route('/uploads/<nombreImagen>')
def uploads(nombreImagen):
    return send_from_directory(app.config['CARPETA'], nombreImagen)

# Routing Landing
@app.route("/")
def landing():
    # Renderiza la pagina principal
    return render_template('juegos/landing.html')

# Routing Index
@app.route('/index')
def index():
    # Titulo de la pagina
    titulo = 'Index'
    # Muestra todos los datos de la tabla juegos
    sql          = "SELECT * FROM netflax.juegos ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)

# Routing Destroy
@app.route('/destroy/<int:id>')
def destroy(id):
    # Elimina uno de los juegos segun su id
    cursor.execute("SELECT imagen FROM netflax.juegos WHERE id=%s", (id))
    fila         = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM netflax.juegos WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

# Routing Edit
@app.route('/edit/<int:id>')
def edit(id):
    # Renderiza la pagina de edicion de datos de juegos
    cursor.execute("SELECT * FROM netflax.juegos WHERE id=%s", (id))
    juegos       = cursor.fetchall()
    conn.commit()
    return render_template('juegos/edit.html', juegos=juegos)

# Routing Create
@app.route('/create')
def create():
    # Renderiza la pagina de creado de juegos
    return render_template('juegos/create.html')

# Routing Store
@app.route('/store', methods=['POST'])
def storage():
    # postea los datos ingresados en create.html
    try:
        _nombre      = request.form['txtNombre']
        _tier = request.form['txtTier']
        _genero      = request.form['txtGenero']
        _imagen      = request.files['txtImagen']
    except:
        flash("You must fill-in all the fields!", "flash-error")
        return redirect(url_for('create'))

    # Validar datos
    if _nombre == '' or _tier == '' or _genero == '' or _imagen == '':
        flash("You must fill-in all the fields.")
        return redirect(url_for('create'))

    # guarda imagen con datetime en el nombre para que no se pisen dos imgs con mismo nombre
    now          = datetime.now()
    tiempo       = now.strftime("%Y%H%M%S")
    if _imagen.filename!='':
        nuevoNombreImagen = tiempo + _imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
    # inyecta SQL Query
    sql          = "INSERT INTO netflax.juegos (nombre, imagen, tier, genero) VALUES (%s, %s, %s, %s);"
    datos        = (_nombre, nuevoNombreImagen, _tier, _genero)
    conn         = mysql.connect()
    # cursor permite ejecutar codigo sql
    cursor       = conn.cursor()
    # ejecuta la instruccion
    cursor.execute(sql, datos)
    # commitea la instruccion
    conn.commit()
    flash("Game added succesfully!", "flash-success")
    return redirect('/create')

# Routing Update
@app.route('/update', methods=['POST'])
def update():
    # codigo para editar los datos de los juegos
    _nombre      = request.form['txtNombre']
    _tier = request.form['txtTier']
    _genero      = request.form['txtGenero']
    _imagen      = request.files['txtImagen']
    id           = request.form['txtID']

    sql          = "UPDATE netflax.juegos SET nombre=%s, tier=%s, genero=%s WHERE id=%s;"
    datos        = (_nombre, _tier, _genero, id)


    # Edicion de la imagen
    now          = datetime.now()
    tiempo       = now.strftime("%Y%H%M%S")
    if _imagen.filename != '':
        nuevoNombreImagen = tiempo + _imagen.filename
        _imagen.save('uploads/'+nuevoNombreImagen)
        cursor.execute("SELECT imagen FROM netflax.juegos WHERE id=%s", id)
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE netflax.juegos SET imagen=%s WHERE id=%s", (nuevoNombreImagen, id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

# Routing Tier_S
@app.route("/tier_S")
def tier_S():
    # Titulo de la pagina
    titulo = 'S Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'S' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
    
# Routing Tier_A
@app.route("/tier_A")
def tier_A():
    # Titulo de la pagina
    titulo = 'A Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'A' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
# Routing Tier_B
@app.route("/tier_B")
def tier_B():
    # Titulo de la pagina
    titulo = 'B Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'B' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
# Routing Tier_C
@app.route("/tier_C")
def tier_C():
    # Titulo de la pagina
    titulo = 'C Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'C' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
# Routing Tier_D
@app.route("/tier_D")
def tier_D():
    # Titulo de la pagina
    titulo = 'D Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'D' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
# Routing Tier_E
@app.route("/tier_E")
def tier_E():
    # Titulo de la pagina
    titulo = 'E Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'E' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)
# Routing Tier_F
@app.route("/tier_F")
def tier_F():
    # Titulo de la pagina
    titulo = 'F Tier'

    # Muestra todos los datos de la tabla juegos de tier S
    sql          = "SELECT * FROM netflax.juegos WHERE tier = 'F' ORDER BY nombre;"
    cursor.execute(sql)
    juegos       = cursor.fetchall()
    print(juegos)
    conn.commit()

    # Renderiza la pagina principal
    return render_template('juegos/index.html', juegos=juegos, titulo=titulo)

if __name__ == '__main__':
    app.run(debug=True)