# Hogar San Ramón - Login, residentes y cuidados (registrar, modificar, mostrar, eliminar)
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib
import re
from datetime import datetime


# ---------------------- CONEXIÓN ----------------------
def conectar():
    return mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        port=3306,
        user="sql10841006",
        password="mymKMsTsga",
        database="sql10841006",
        connection_timeout=10,   
        use_pure=True,
    )


def ejecutar(sql, datos=(), leer=False):
    db = conectar()
    try:
        cur = db.cursor()
        cur.execute(sql, datos)
        if leer:
            return cur.fetchall()
        db.commit()
    finally:
        db.close()


def mostrar_error(e):
    # traduce los errores de las restricciones de la base de datos
    codigo = getattr(e, "errno", None)
    if codigo == 1062:
        mensaje = "Ya existe un registro con ese dato (CI repetido)."
    elif codigo == 1451:
        mensaje = "No se puede eliminar: tiene registros relacionados (por ejemplo cuidados)."
    elif codigo == 3819:
        mensaje = "Hay un dato que no cumple las restricciones de la base de datos."
    else:
        mensaje = str(e)
    messagebox.showerror("Error", mensaje)


# ---------------------- VALIDACIONES ----------------------
def ci_valido(ci):
    # 6 a 8 números (0-9) y al final una extensión opcional de hasta 3 caracteres
    return re.fullmatch(r"[0-9]{6,8}[A-Za-z0-9]{0,3}", ci) is not None


MENSAJE_CI = ("El CI debe empezar con 6 a 8 números (0-9) y puede terminar con una "
              "extensión de hasta 3 caracteres (ejemplo: 1234567 o 1234567A).")


def validar_residente(ci, nombres, apellidos, fecha, hab):
    if not ci_valido(ci):
        return MENSAJE_CI
    if not 3 <= len(nombres) <= 40:
        return "Los nombres deben tener entre 3 y 40 caracteres."
    if not 3 <= len(apellidos) <= 30:
        return "Los apellidos deben tener entre 3 y 30 caracteres."
    try:
        f = datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return "Fecha inválida. Use el formato AAAA-MM-DD."
    if f >= datetime(2000, 1, 1):
        return "La fecha de nacimiento debe ser anterior al 2000-01-01."
    if not hab.isdigit() or not 1 <= int(hab) <= 300:
        return "La habitación debe ser un número entre 1 y 300."
    return None


def validar_cuidado(ci, descripcion, horario):
    if not ci_valido(ci):
        return MENSAJE_CI
    if not 10 <= len(descripcion) <= 250:
        return "La descripción debe tener entre 10 y 250 caracteres."
    try:
        datetime.strptime(horario, "%H:%M")
    except ValueError:
        return "Horario inválido. Use el formato HH:MM (ejemplo 08:30)."
    return None


# ---------------------- FUNCIONES PARA LA INTERFAZ GRAFICA ----------------------
def crear_pestana(cuaderno, titulo, campos, columnas):
    marco = tk.Frame(cuaderno, padx=10, pady=10)
    cuaderno.add(marco, text=titulo)
    entradas = []
    for i, texto in enumerate(campos):
        tk.Label(marco, text=texto).grid(row=i, column=0, sticky="w")
        e = tk.Entry(marco, width=40)
        e.grid(row=i, column=1, pady=2, sticky="w")
        entradas.append(e)
    botones = tk.Frame(marco)
    botones.grid(row=len(campos), column=0, columnspan=2, pady=8)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=8)
    for c in columnas:
        tabla.heading(c, text=c)
        tabla.column(c, width=120)
    tabla.grid(row=len(campos) + 1, column=0, columnspan=2)
    return entradas, botones, tabla


def poner_botones(marco, lista):
    for texto, funcion in lista:
        tk.Button(marco, text=texto, width=10, command=funcion).pack(side="left", padx=3)


def llenar(entradas, valores):
    for e, v in zip(entradas, valores):
        e.delete(0, tk.END)
        e.insert(0, v)


def limpiar(entradas):
    for e in entradas:
        e.delete(0, tk.END)


# ---------------------- LOGIN ----------------------
def login():
    usuario = entry_user.get().strip()
    clave = entry_pass.get().strip()
    if usuario == "" or clave == "":
        messagebox.showwarning("Aviso", "Escriba usuario y contraseña")
        return
    # la contraseña se guarda encriptada con sha2, por eso la encriptamos igual
    clave_hash = hashlib.sha256(clave.encode()).hexdigest()
    try:
        fila = ejecutar("select id_personal, estado from usuario "
                        "where nombre_usuario = %s and contrasena = %s",
                        (usuario, clave_hash), True)
    except Exception as e:
        messagebox.showerror("Error", "No se pudo conectar: " + str(e))
        return

    if not fila:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    elif fila[0][1] != "activo":
        messagebox.showerror("Error", "El usuario está inactivo")
    else:
        ventana_login.destroy()
        abrir_principal(fila[0][0])


# ---------------------- VENTANA PRINCIPAL ----------------------
def abrir_principal(id_personal):
    ventana = tk.Tk()
    ventana.title("Hogar San Ramón")
    cuaderno = ttk.Notebook(ventana)
    cuaderno.pack(padx=20, pady=20)

    sel = {"res": None, "cui": None}     
    datos_res = {}
    datos_cui = {}

    # ================= RESIDENTES =================
    ent_res, bot_res, tabla_res = crear_pestana(
        cuaderno, "Residentes",
        ["CI", "Nombres", "Apellidos", "Fecha nac. (AAAA-MM-DD)", "N° habitación"],
        ["CI", "Nombres", "Apellidos", "Fecha nac.", "Habitación"])

    def mostrar_residentes():
        tabla_res.delete(*tabla_res.get_children())
        datos_res.clear()
        try:
            filas = ejecutar("select r.id_residente, r.ci_residente, r.nombres, r.apellidos, "
                             "r.fecha_nac, h.numero from residente r "
                             "join habitacion h on r.id_habitacion = h.id_habitacion", (), True)
        except Exception as e:
            mostrar_error(e)
            return
        for f in filas:
            datos_res[str(f[0])] = f
            tabla_res.insert("", tk.END, iid=str(f[0]), values=f[1:])

    def limpiar_residente():
        limpiar(ent_res)
        sel["res"] = None

    def elegir_residente(evento):
        item = tabla_res.selection()
        if item:
            fila = datos_res[item[0]]
            sel["res"] = fila[0]
            llenar(ent_res, [str(x) for x in fila[1:]])

    def buscar_habitacion(numero):
        fila = ejecutar("select id_habitacion from habitacion where numero = %s", (numero,), True)
        if not fila:
            messagebox.showerror("Error", "Esa habitación no existe")
            return None
        return fila[0][0]

    def registrar_residente():
        datos = [e.get().strip() for e in ent_res]
        error = validar_residente(*datos)
        if error:
            messagebox.showwarning("Validación", error)
            return
        try:
            id_hab = buscar_habitacion(datos[4])
            if id_hab is None:
                return
            ejecutar("insert into residente (ci_residente, nombres, apellidos, fecha_nac, id_habitacion) "
                     "values (%s, %s, %s, %s, %s)", (*datos[:4], id_hab))
            messagebox.showinfo("Listo", "Residente registrado")
            limpiar_residente()
            mostrar_residentes()
        except Exception as e:
            mostrar_error(e)

    def modificar_residente():
        if sel["res"] is None:
            messagebox.showwarning("Aviso", "Primero elija un residente de la tabla")
            return
        datos = [e.get().strip() for e in ent_res]
        error = validar_residente(*datos)
        if error:
            messagebox.showwarning("Validación", error)
            return
        try:
            id_hab = buscar_habitacion(datos[4])
            if id_hab is None:
                return
            ejecutar("update residente set ci_residente=%s, nombres=%s, apellidos=%s, "
                     "fecha_nac=%s, id_habitacion=%s where id_residente=%s",
                     (*datos[:4], id_hab, sel["res"]))
            messagebox.showinfo("Listo", "Residente modificado")
            limpiar_residente()
            mostrar_residentes()
        except Exception as e:
            mostrar_error(e)

    def eliminar_residente():
        if sel["res"] is None:
            messagebox.showwarning("Aviso", "Primero elija un residente de la tabla")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que quiere eliminar este residente?"):
            return
        try:
            ejecutar("delete from residente where id_residente=%s", (sel["res"],))
            messagebox.showinfo("Listo", "Residente eliminado")
            limpiar_residente()
            mostrar_residentes()
        except Exception as e:
            mostrar_error(e)

    tabla_res.bind("<<TreeviewSelect>>", elegir_residente)
    poner_botones(bot_res, [("Registrar", registrar_residente), ("Modificar", modificar_residente),
                            ("Eliminar", eliminar_residente), ("Mostrar", mostrar_residentes),
                            ("Limpiar", limpiar_residente)])

    # ================= CUIDADOS =================
    ent_cui, bot_cui, tabla_cui = crear_pestana(
        cuaderno, "Cuidados",
        ["CI del residente", "Descripción", "Horario (HH:MM)"],
        ["CI", "Residente", "Descripción", "Horario", "Registrado por"])

    def mostrar_cuidados():
        tabla_cui.delete(*tabla_cui.get_children())
        datos_cui.clear()
        try:
            filas = ejecutar("select c.id_cuidado, r.ci_residente, concat(r.nombres,' ',r.apellidos), "
                             "c.descripcion, time_format(c.horario,'%H:%i'), "
                             "concat(p.nombres,' ',p.apellidos) from cuidado c "
                             "join residente r on c.id_residente = r.id_residente "
                             "join personal p on c.id_personal = p.id_personal", (), True)
        except Exception as e:
            mostrar_error(e)
            return
        for f in filas:
            datos_cui[str(f[0])] = f
            tabla_cui.insert("", tk.END, iid=str(f[0]), values=f[1:])

    def limpiar_cuidado():
        limpiar(ent_cui)
        sel["cui"] = None

    def elegir_cuidado(evento):
        item = tabla_cui.selection()
        if item:
            fila = datos_cui[item[0]]
            sel["cui"] = fila[0]
            llenar(ent_cui, [fila[1], fila[3], fila[4]])

    def buscar_residente(ci):
        fila = ejecutar("select id_residente from residente where ci_residente = %s", (ci,), True)
        if not fila:
            messagebox.showerror("Error", "No existe un residente con ese CI")
            return None
        return fila[0][0]

    def registrar_cuidado():
        ci, descripcion, horario = [e.get().strip() for e in ent_cui]
        error = validar_cuidado(ci, descripcion, horario)
        if error:
            messagebox.showwarning("Validación", error)
            return
        try:
            id_res = buscar_residente(ci)
            if id_res is None:
                return
            # el personal responsable es quien inició sesión
            ejecutar("insert into cuidado (descripcion, horario, id_residente, id_personal) "
                     "values (%s, %s, %s, %s)", (descripcion, horario, id_res, id_personal))
            messagebox.showinfo("Listo", "Cuidado registrado")
            limpiar_cuidado()
            mostrar_cuidados()
        except Exception as e:
            mostrar_error(e)

    def modificar_cuidado():
        if sel["cui"] is None:
            messagebox.showwarning("Aviso", "Primero elija un cuidado de la tabla")
            return
        ci, descripcion, horario = [e.get().strip() for e in ent_cui]
        error = validar_cuidado(ci, descripcion, horario)
        if error:
            messagebox.showwarning("Validación", error)
            return
        try:
            id_res = buscar_residente(ci)
            if id_res is None:
                return
            ejecutar("update cuidado set descripcion=%s, horario=%s, id_residente=%s "
                     "where id_cuidado=%s", (descripcion, horario, id_res, sel["cui"]))
            messagebox.showinfo("Listo", "Cuidado modificado")
            limpiar_cuidado()
            mostrar_cuidados()
        except Exception as e:
            mostrar_error(e)

    def eliminar_cuidado():
        if sel["cui"] is None:
            messagebox.showwarning("Aviso", "Primero elija un cuidado de la tabla")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que quiere eliminar este cuidado?"):
            return
        try:
            ejecutar("delete from cuidado where id_cuidado=%s", (sel["cui"],))
            messagebox.showinfo("Listo", "Cuidado eliminado")
            limpiar_cuidado()
            mostrar_cuidados()
        except Exception as e:
            mostrar_error(e)

    tabla_cui.bind("<<TreeviewSelect>>", elegir_cuidado)
    poner_botones(bot_cui, [("Registrar", registrar_cuidado), ("Modificar", modificar_cuidado),
                            ("Eliminar", eliminar_cuidado), ("Mostrar", mostrar_cuidados),
                            ("Limpiar", limpiar_cuidado)])

    # al abrir, se muestran los datos de las dos tablas
    mostrar_residentes()
    mostrar_cuidados()
    ventana.mainloop()


# ---------------------- VENTANA DE LOGIN ----------------------
ventana_login = tk.Tk()
ventana_login.title("Hogar San Ramón")
ventana_login.geometry("900x600")
ventana_login.configure(bg="#F4F4F4")

contenedor = tk.Frame(ventana_login, bg="#F4F4F4")
contenedor.place(relx=0.5, rely=0.5, anchor="center")

# Títulos principal y subtítulo
tk.Label(
    contenedor,
    text="Hogar San Ramón",
    font=("Segoe UI", 24),
    bg="#F4F4F4",
    fg="#222222"
).pack(pady=(0, 2))

tk.Label(
    contenedor,
    text="Casa de albergue de abuelitos y abuelitas",
    font=("Segoe UI", 15),
    bg="#F4F4F4",
    fg="#666666"
).pack(pady=(0, 25))

tk.Label(
    contenedor,
    text="Usuario",
    font=("Segoe UI", 10),
    bg="#F4F4F4",
    fg="#444444",
    anchor="w"
).pack(fill="x", pady=(0, 4))

entry_user = ttk.Entry(contenedor, width=38, font=("Segoe UI", 11))
entry_user.pack(ipady=3)

# Campo Contraseña (etiqueta arriba, caja abajo)
tk.Label(
    contenedor,
    text="Contraseña",
    font=("Segoe UI", 10),
    bg="#F4F4F4",
    fg="#444444",
    anchor="w"
).pack(fill="x", pady=(14, 4))

entry_pass = ttk.Entry(contenedor, width=38, font=("Segoe UI", 11), show="*")
entry_pass.pack(ipady=3)

# Botón Ingresar centrado
ttk.Button(
    contenedor,
    text="Ingresar",
    command=login
).pack(pady=(22, 0), ipadx=14, ipady=4)


ventana_login.mainloop()
