from flask import Flask, render_template, request, redirect, url_for, session
import os 
import database as db
from notifypy import Notify

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder= template_dir)

#LOGIN Y REGISTER
@app.route('/')
def home():
    return render_template('layout.html')    


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        correo = request.form['correo']
        admin_password = request.form['admin_password']

        cursor = db.database.cursor()
        cursor.execute("SELECT * FROM Administrador WHERE correo=%s",(correo,))
        admin = cursor.fetchone()
        cursor.close()

        if len(admin)>0:
            if admin_password == admin["admin_password"]:
                session['nombre'] = admin['nombre']
                session['correo'] = admin['correo']


            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template("login.html")
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template("login.html")
    else:
        
        return render_template("login.html")


@app.route('/registro', methods =['POST'])
def registro():
     cursor = db.database.cursor()
     cursor.execute("SELECT * FROM Administrador")
     myresult = cursor.fetchall()
     cursor.close()        

     if request.method == 'GET':
        return render_template("registro.html" )
    
     else:
        nombre = request.form['nombre']
        correo = request.form['correo']
        admin_password = request.form['admin_password']
        documento = request.form['documento']

        cur = db.database.cursor()
        cur.execute("INSERT INTO users (nombre, correo, admin_password, documento) VALUES (%s,%s,%s,%s)", (nombre, correo, admin_password,documento))
        db.database.commit()
        return redirect(url_for('login'))



#esta ruta que esta abajo es la principal
"""@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM Productos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario para obtener las keys de ellos
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObject)"""

#Ruta pa guardar productos
@app.route('/products', methods=['POST'])
def addProduct():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']

    if nombre and descripcion and precio and cantidad and imagen:
        cursor = db.database.cursor()
        sql = "insert into Productos (nombre, descripcion, precio, cantidad, imagen) values (%s, %s, %s, %s, %s)"
        data = (nombre, descripcion, precio, cantidad, imagen)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>' )
def deleteProduct(id):
        cursor = db.database.cursor()
        sql = "delete from Productos where id=%s "
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']


    if nombre and descripcion and precio and cantidad and imagen:
        cursor = db.database.cursor()
        sql = "update Productos set nombre= %s, descripcion= %s, precio= %s, cantidad= %s, imagen= %s where id= %s"
        data = (nombre, descripcion, precio, cantidad, imagen, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True, port=4000)


    
