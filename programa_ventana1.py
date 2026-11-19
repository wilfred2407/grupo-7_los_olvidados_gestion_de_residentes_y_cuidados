# Registrar residente - Hogar San Ramón
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root",
                              password="patito123", database="hogar_san_ramon")
cursor = con.cursor()


def guardar():
    ci = entrada_ci.get()
    nombres = entrada_nombres.get()
    apellidos = entrada_apellidos.get()
    fecha = entrada_fecha.get()
    habitacion = entrada_habitacion.get()

    # error si falta algun dato
    if ci == "" or nombres == "" or apellidos == "" or fecha == "" or habitacion == "":
        messagebox.showerror("Error", "Complete todos los campos")
        return

    # error si la fecha esta mal escrita
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "La fecha debe ser AAAA-MM-DD (ejemplo: 1945-03-10)")
        return

    # error si la habitacion no es un numero
    if not habitacion.isdigit():
        messagebox.showerror("Error", "La habitación debe ser un número (ejemplo: 101)")
        return

    # guardar en la base de datos
    try:
        # buscamos la habitacion, si no existe la creamos
        cursor.execute("SELECT id_habitacion FROM habitacion WHERE numero = %s", (habitacion,))
        fila = cursor.fetchone()
        if fila is None:
            cursor.execute("INSERT INTO habitacion (numero) VALUES (%s)", (habitacion,))
            id_habitacion = cursor.lastrowid
        else:
            id_habitacion = fila[0]

        cursor.execute("INSERT INTO residente (ci_residente, nombres, apellidos, fecha_nac, id_habitacion) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (ci, nombres, apellidos, fecha, id_habitacion))
        con.commit()
        messagebox.showinfo("Éxito", "El residente se guardó correctamente")
        # limpiar los campos
        entrada_ci.delete(0, tk.END)
        entrada_nombres.delete(0, tk.END)
        entrada_apellidos.delete(0, tk.END)
        entrada_fecha.delete(0, tk.END)
        entrada_habitacion.delete(0, tk.END)
    except mysql.connector.IntegrityError:
        con.rollback()
        messagebox.showerror("Error", "Ese carnet ya está registrado")
    except mysql.connector.Error as error:
        con.rollback()
        messagebox.showerror("Error", "No se pudo guardar:\n" + str(error))


# ventana
ventana = tk.Tk()
ventana.title("Registrar residente")
ventana.geometry("350x420")

tk.Label(ventana, text="Registrar residente", font=("Arial", 14)).pack(pady=10)

tk.Label(ventana, text="Carnet de identidad:").pack()
entrada_ci = tk.Entry(ventana)
entrada_ci.pack(pady=3)

tk.Label(ventana, text="Nombres:").pack()
entrada_nombres = tk.Entry(ventana)
entrada_nombres.pack(pady=3)

tk.Label(ventana, text="Apellidos:").pack()
entrada_apellidos = tk.Entry(ventana)
entrada_apellidos.pack(pady=3)

tk.Label(ventana, text="Fecha de nacimiento (AAAA-MM-DD):").pack()
entrada_fecha = tk.Entry(ventana)
entrada_fecha.pack(pady=3)

tk.Label(ventana, text="Número de habitación:").pack()
entrada_habitacion = tk.Entry(ventana)
entrada_habitacion.pack(pady=3)

tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

ventana.mainloop()
