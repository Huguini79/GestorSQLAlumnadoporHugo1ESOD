import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import subprocess
import sys
import platform

try:
    import mysql.connector
except ImportError:
    pregunta = messagebox.askyesno('Alerta', 'Actualmente mysql.connector no está instalado en tu sistema operativo, ¿quieres que el programa te lo instale automáticamente con la librería subprocess y con pip?', icon='warning')
    if pregunta:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
        import mysql.connector
    else:
        messagebox.showinfo('Ok', 'Ok, instálala manualmente tú mismo.')
        sys.exit(1)

try:
    sistema_operativo = platform.system()  # Detecta el sistema operativo
    if sistema_operativo == "Linux":
        pregunta2 = messagebox.askyesno('Pregunta', '¿Permites al programa que instale mysql en tu ordenador?')
        if pregunta2:
            subprocess.check_call(["sudo", "apt", "install", "-y", "mysql-server"])
            messagebox.showinfo("Instalación completa", "MySQL se ha instalado correctamente.")
            
            pregunta3 = messagebox.askyesno('Pregunta', '¿Ahora quieres que te abra la terminal para que se termine de configurar mysql?')

            if pregunta3:
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'mysql -u root -p; exec bash'])
                messagebox.showinfo("Mensaje", "La terminal se ha abierto. Por favor, ingresa tu contraseña(DEJÁLALA EN BLANCO).")
            else:
                messagebox.showinfo('Ok', 'Ok, hazlo tú mismo.')

        else:
            messagebox.showinfo('Ok', 'Ok, hazlo tú mismo.')

    elif sistema_operativo == "Windows":
        messagebox.showinfo('Información', 'Por favor, visita la siguiente URL para descargar MySQL: https://dev.mysql.com/downloads/mysql/.')
        
    else:
        messagebox.showwarning('Advertencia', 'Sistema operativo no soportado para la instalación automática de MySQL.')

except Exception as e:
    messagebox.showerror('Error', 'Hubo un error al intentar ejecutar los comandos.')

def conexion():
    try:
        conexionn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='elgranhuguini79123@#@#',
            database='basededatosprograma'
        )
        return conexionn
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"Error al conectar con la base de datos: {err}")
        return None

def crear_tabla():
    conexionn = conexion()
    if conexionn is not None:
        cursor = conexionn.cursor()
        try:
            cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS datos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                datos TEXT
            )
            """)
            conexionn.commit()
            messagebox.showinfo("Éxito", "Tabla creada exitosamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error al crear tabla", f"Error: {err}")
        finally:
            cursor.close()
            conexionn.close()

def obtener_registros():
    conexionnn = conexion()
    if conexionnn is not None:
        cursor = conexionnn.cursor()
        try:
            cursor.execute("SELECT * FROM datos")
            registros = cursor.fetchall()
            return registros
        except mysql.connector.Error as err:
            messagebox.showerror("Error al obtener registros", f"Error: {err}")
            return []
        finally:
            cursor.close()
            conexionnn.close()

def mostrar_registros():

    root2 = tk.Tk()
    root2.configure(bg='yellow')
    root2.geometry('660x550')

    registros = obtener_registros()
    
    canvas = tk.Canvas(root2, bg='white')
    scroll_y = tk.Scrollbar(root2, orient="vertical", command=canvas.yview)
    scroll_x = tk.Scrollbar(root2, orient="horizontal", command=canvas.xview)

    frame = tk.Frame(canvas, bg='white')
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    for registro in registros:
        id_label = tk.Label(frame, text=f"ID: {registro[0]}", wraplength=500)
        nombre_label = tk.Label(frame, text=f"Nombre: {registro[1]}", wraplength=500)
        datos_label = tk.Label(frame, text=f"Datos: {registro[2]}", wraplength=500)
        
        id_label.pack(padx=10, pady=5)
        nombre_label.pack(padx=10, pady=5)
        datos_label.pack(padx=10, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    
        

def insertar_registro():
    root3 = tk.Tk()
    root3.configure(bg='yellow')
    root3.geometry('660x550')

    def envi():
        # Obtén los valores de los campos de entrada en el momento de hacer clic en el botón
        nombre = nombree.get('1.0', 'end-1c').strip()  # Eliminar espacios en blanco adicionales
        datos = datoss.get('1.0', 'end-1c').strip()  # Eliminar espacios en blanco adicionales

        # Validar si los campos no están vacíos
        if nombre and datos:
            conexionnnn = conexion()
            if conexionnnn is not None:
                cursor = conexionnnn.cursor()
                try:
                    cursor.execute("INSERT INTO datos (nombre, datos) VALUES (%s, %s)", (nombre, datos))
                    conexionnnn.commit()
                    messagebox.showinfo("Éxito", "Registro añadido exitosamente.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error al añadir registro", f"Error: {err}")
                finally:
                    cursor.close()
                    conexionnnn.close()
        else:
            messagebox.showwarning("Advertencia", "El nombre y los datos no pueden estar vacíos.")

    # Interfaz para insertar el registro
    label = tk.Label(root3, text='Introduce el nombre del alumno que quieres añadir', wraplength=400)
    nombree = tk.Text(root3, height='2', width='25')
    label2 = tk.Label(root3, text='Introduce los datos que quieras añadir a ese alumno', wraplength=400)
    datoss = tk.Text(root3, height='2', width='25')

    botónenvi = tk.Button(root3, text='Enviar', height='2', width='10', command=envi)

    # Colocar los elementos en la interfaz
    label.grid(row=0, column=0, padx=10, pady=10)
    nombree.grid(row=1, column=0, padx=10, pady=10)
    label2.grid(row=2, column=0, padx=10, pady=10)
    datoss.grid(row=3, column=0, padx=10, pady=10)
    botónenvi.grid(row=4, column=0, padx=10, pady=10)



def modificar_datos():
    root5 = tk.Tk()
    root5.configure(bg='yellow')
    root5.geometry('660x550')

    def envi3():
        # Retrieve the value of id_registro from the text widget
        id_registro = id_registroo.get('1.0', 'end-1c').strip()
        datos_nuevos = datos_adicionaless.get('1.0', 'end-1c').strip()
        
        if not id_registro:
            messagebox.showwarning("Advertencia", "Por favor, introduce un ID.")
            return
        
        if not id_registro.isdigit():
            messagebox.showwarning("Advertencia", "Por favor, introduce un ID válido (número).")
            return
        
        # Convert id_registro to an integer
        id_registro = int(id_registro)
        
        if datos_nuevos:
            conexionnnnn = conexion()
            if conexionnnnn is not None:
                cursor = conexionnnnn.cursor()
                try:
                    cursor.execute("UPDATE datos SET datos = %s WHERE id = %s", (datos_nuevos, id_registro))
                    if cursor.rowcount == 0:
                        messagebox.showwarning("Advertencia", "No se encontró ningún registro con ese ID.")
                    else:
                        conexionnnnn.commit()
                        messagebox.showinfo("Éxito", "Datos del alumno modificados exitosamente.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error al modificar datos", f"Error: {err}")
                finally:
                    cursor.close()
                    conexionnnnn.close()
        else:
            messagebox.showwarning("Advertencia", "Los nuevos datos no pueden estar vacíos.")

    # Create UI components
    labell = tk.Label(root5, text='Introduce el ID del alumno:', wraplength=400)
    labell.pack(pady=10)

    id_registroo = tk.Text(root5, height='2', width='25')
    id_registroo.pack(pady=10)

    tk.Label(root5, text='Introduce los nuevos datos para el alumnado', wraplength=400).pack(pady=10)
    
    datos_adicionaless = tk.Text(root5, height='2', width='25')
    datos_adicionaless.pack(pady=10)

    tk.Button(root5, text='Enviar', height='2', width='10', command=envi3).pack(pady=10)




def añadir_datos():
    root4 = tk.Tk()
    root4.configure(bg='yellow')
    root4.geometry('660x550')

    def envi2():
        # Get the ID from the text widget
        id_registro = id_registroo.get('1.0', 'end-1c').strip()  # Strip any extra whitespace
        
        if not id_registro:
            messagebox.showwarning("Advertencia", "Por favor, introduce un ID.")
            return
        
        if not id_registro.isdigit():
            messagebox.showwarning("Advertencia", "Por favor, introduce un ID válido (número).")
            return

        # Convert the ID to an integer
        id_registro = int(id_registro)

        # Get the new data
        datos_adicionales = datos_adicionaless.get('1.0', 'end-1c').strip()  # Strip any extra whitespace
        
        if not datos_adicionales:
            messagebox.showwarning("Advertencia", "Los datos adicionales no pueden estar vacíos.")
            return

        # Perform the database update
        conexionnnnn = conexion()
        if conexionnnnn is not None:
            cursor = conexionnnnn.cursor()
            try:
                # First, get the existing data
                cursor.execute("SELECT datos FROM datos WHERE id = %s", (id_registro,))
                resultado = cursor.fetchone()
                
                if resultado:
                    # Combine the existing data with the new data
                    nuevos_datos = resultado[0] + " " + datos_adicionales
                    cursor.execute("UPDATE datos SET datos = %s WHERE id = %s", (nuevos_datos, id_registro))
                    conexionnnnn.commit()
                    messagebox.showinfo("Éxito", "Datos añadidos exitosamente.")
                else:
                    messagebox.showwarning("Advertencia", "No se encontró ningún registro con ese ID.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error al añadir datos", f"Error: {err}")
            finally:
                cursor.close()
                conexionnnnn.close()

    # Create UI components
    labell = tk.Label(root4, text='Introduce el ID del alumno:', wraplength=400)
    labell.pack(pady=10)

    id_registroo = tk.Text(root4, height='2', width='25')
    id_registroo.pack(pady=10)

    tk.Label(root4, text='Introduce los datos para el alumnado', wraplength=400).pack(pady=10)
    
    datos_adicionaless = tk.Text(root4, height='2', width='25')
    datos_adicionaless.pack(pady=10)

    tk.Button(root4, text='Enviar', height='2', width='10', command=envi2).pack(pady=10)




def eliminar_registro():
    id_registro = simpledialog.askstring("Eliminar Registro", "Introduce el ID del registro a eliminar:")
    
    if id_registro is None:
        return  

    if not id_registro.isdigit():
        messagebox.showwarning("Advertencia", "Por favor, introduce un ID válido (número).")
        return

    id_registro = int(id_registro)

    conexionnnnn = conexion()
    if conexionnnnn is not None:
        cursor = conexionnnnn.cursor()
        try:
            cursor.execute("DELETE FROM datos WHERE id = %s", (id_registro,))
            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", "No se encontró ningún registro con ese ID.")
            else:
                conexionnnnn.commit()
                messagebox.showinfo("Éxito", "Registro eliminado exitosamente.")
                mostrar_registros()  # Actualizar la lista de registros
        except mysql.connector.Error as err:
            messagebox.showerror("Error al eliminar registro", f"Error: {err}")
        finally:
            cursor.close()
            conexionnnnn.close()

def eliminar_datos():
    id_registro = simpledialog.askstring("Eliminar Datos", "Introduce el ID del alumno para eliminar sus datos:")
    
    if id_registro is None:
        return  

    if not id_registro.isdigit():
        messagebox.showwarning("Advertencia", "Por favor, introduce un ID válido (número).")
        return

    id_registro = int(id_registro)

    conexionnnnn = conexion()
    if conexionnnnn is not None:
        cursor = conexionnnnn.cursor()
        try:
            cursor.execute("UPDATE datos SET datos = NULL WHERE id = %s", (id_registro,))
            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", "No se encontró ningún registro con ese ID.")
            else:
                conexionnnnn.commit()
                messagebox.showinfo("Éxito", "Datos del alumno eliminados exitosamente.")
                mostrar_registros()  # Actualizar la lista de registros después de eliminar los datos
        except mysql.connector.Error as err:
            messagebox.showerror("Error al eliminar datos", f"Error: {err}")
        finally:
            cursor.close()
            conexionnnnn.close()


def autent():
    while True:
        entrada = simpledialog.askstring('Credenciales', 'Por favor, introduce las credenciales para acceder al Gestor SQL')
        if entrada is None:
            break

        elif entrada == 'adminsql12345@#':
            mostrar_ventana_principal()
        else:
            retry = messagebox.askretrycancel('Error', 'Las credenciales son incorrectas, te voy a llevar de nuevo a las credenciales(no cierres el programa, automáticamente te va a llevar).')
            if not retry:
                break

def mostrar_ventana_principal():
    messagebox.showinfo('Bienvenido', 'Bienvenido al Gestor SQL por Hugo para el Alumnado')
    root = tk.Tk()
    root.title('Gestor del Alumnado por Hugo de 1 ESO D')
    root.configure(bg='yellow')
    root.geometry('660x550')

    tk.Button(root, text="Insertar Alumno", command=insertar_registro).pack(pady=10)
    tk.Button(root, text="Modificar Datos de Alumno", command=modificar_datos).pack(pady=10)
    tk.Button(root, text="Añadir Datos de Alumno", command=añadir_datos).pack(pady=10)
    tk.Button(root, text="Eliminar Alumno", command=eliminar_registro).pack(pady=10)
    tk.Button(root, text="Eliminar Datos de Alumno", command=eliminar_datos).pack(pady=10)
    tk.Button(root, text="Mostrar Alumnos y datos", command=mostrar_registros).pack(pady=10)

    def cerrar():
        root.destroy()
        sys.exit(1)

    root.protocol('WM_DELETE_WINDOW', cerrar)


    root.mainloop()

autent()