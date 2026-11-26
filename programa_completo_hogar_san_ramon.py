# Hogar San Ramón - Login y 7 ventanas (residentes, cuidados, plan de atención, personal, turnos,
# asistencia y usuarios) con registrar, modificar, mostrar, eliminar y buscar,
# más una pestaña de Matemáticas (porcentajes, matrices de turnos, promedio y derivada)
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib
import re
from datetime import datetime, timedelta


# ---------------------- CONEXIÓN ----------------------
# Base de datos en TiDB Cloud (compatible con MySQL). El servidor exige conexión segura (TLS).
# RUTA_CA es opcional: si descargó el certificado "CA cert", escriba aquí su ruta
# (ejemplo: r"C:\certificados\isrgrootx1.pem") para verificar el servidor.
RUTA_CA = ""


def conectar():
    opciones = dict(
        host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="4PpZhUJ3CTg9bgu.root",
        password="MLqTAeg962j1lpCF",
        database="hogar_san_ramon",
        connection_timeout=10,
        use_pure=True,
        ssl_disabled=False,        
    )
    if RUTA_CA:
        opciones.update(ssl_ca=RUTA_CA, ssl_verify_cert=True, ssl_verify_identity=True)
    return mysql.connector.connect(**opciones)


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
    detalle = str(getattr(e, "msg", e))
    if codigo == 1062:
        if "ci_residente" in detalle:
            mensaje = "Ya existe un residente con ese CI."
        elif "nombre_usuario" in detalle:
            mensaje = "Ese nombre de usuario ya existe."
        elif "usuario.id_personal" in detalle:
            mensaje = "Esa persona del personal ya tiene un usuario."
        elif "turno.id_personal" in detalle:
            mensaje = "Esa persona ya tiene un turno que empieza ese día a esa hora."
        elif "id_turno" in detalle:
            mensaje = "Ese turno ya tiene una asistencia registrada."
        else:
            mensaje = "Ya existe un registro con ese dato."
    elif codigo == 1451:
        mensaje = "No se puede eliminar: tiene registros relacionados (cuidados, planes, turnos, usuario, etc.)."
    elif codigo == 1452:
        mensaje = "El registro relacionado (residente, personal, cargo, rol o turno) no existe."
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


def fecha_valida(texto):
    # devuelve la fecha o None si el formato AAAA-MM-DD es incorrecto
    try:
        return datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        return None


def hora_valida(texto):
    # devuelve la hora o None si el formato HH:MM es incorrecto
    try:
        return datetime.strptime(texto, "%H:%M")
    except ValueError:
        return None


# Cada validar_xxx recibe la lista de valores del formulario (en el mismo orden de los campos)
# y devuelve un texto con el error, o None si todo está bien. "nuevo" es True al registrar.
def validar_plan(v, nuevo):
    descripcion, inicio, fin, residente = v
    if not 5 <= len(descripcion) <= 200:
        return "La descripción debe tener entre 5 y 200 caracteres."
    f_ini = fecha_valida(inicio)
    if f_ini is None:
        return "Fecha de inicio inválida. Use el formato AAAA-MM-DD."
    if fin:
        f_fin = fecha_valida(fin)
        if f_fin is None:
            return "Fecha de fin inválida. Use AAAA-MM-DD o déjela vacía."
        if f_fin < f_ini:
            return "La fecha de fin no puede ser anterior a la fecha de inicio."
    if not residente:
        return "Elija un residente."
    return None


def validar_personal(v, nuevo):
    nombres, apellidos, telefono, cargo = v
    if not 3 <= len(nombres) <= 40:
        return "Los nombres deben tener entre 3 y 40 caracteres."
    if not 3 <= len(apellidos) <= 30:
        return "Los apellidos deben tener entre 3 y 30 caracteres."
    if re.fullmatch(r"[67][0-9]{7}", telefono) is None:
        return "El teléfono debe tener 8 números y empezar con 6 o 7."
    if not cargo:
        return "Elija un cargo."
    return None


def validar_turno(v, nuevo):
    fecha, inicio, fin, personal = v
    if fecha_valida(fecha) is None:
        return "Fecha inválida. Use el formato AAAA-MM-DD."
    h_ini = hora_valida(inicio)
    h_fin = hora_valida(fin)
    if h_ini is None or h_fin is None:
        return "Las horas deben tener el formato HH:MM (ejemplo 08:30)."
    if h_ini == h_fin:
        return "La hora de inicio debe ser diferente a la hora de fin."
    if not personal:
        return "Elija una persona del personal."
    return None


def validar_asistencia(v, nuevo):
    ingreso, salida, turno = v
    if hora_valida(ingreso) is None:
        return "La hora de ingreso debe tener el formato HH:MM (ejemplo 08:30)."
    if salida and hora_valida(salida) is None:
        return "La hora de salida debe tener el formato HH:MM o quedar vacía."
    if not turno:
        return "Elija un turno."
    return None


def validar_usuario(v, nuevo):
    usuario, clave, estado, rol, personal = v
    if not 4 <= len(usuario) <= 15:
        return "El usuario debe tener entre 4 y 15 caracteres."
    # al modificar, si la contraseña queda vacía se conserva la actual
    if (nuevo or clave) and len(clave) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not estado:
        return "Elija el estado."
    if not rol:
        return "Elija un rol."
    if not personal:
        return "Elija una persona del personal."
    return None


# ---------------------- FUNCIONES PARA LA INTERFAZ GRAFICA ----------------------
def crear_pestana(cuaderno, titulo, campos, columnas, combos=(), claves=()):
    # combos = posiciones de los campos que son lista desplegable; claves = campos de contraseña
    marco = tk.Frame(cuaderno, padx=10, pady=10)
    cuaderno.add(marco, text=titulo)
    entradas = []
    for i, texto in enumerate(campos):
        tk.Label(marco, text=texto).grid(row=i, column=0, sticky="w")
        if i in combos:
            e = ttk.Combobox(marco, width=37, state="readonly")
        else:
            e = tk.Entry(marco, width=40, show="*" if i in claves else "")
        e.grid(row=i, column=1, pady=2, sticky="w")
        entradas.append(e)
    botones = tk.Frame(marco)
    botones.grid(row=len(campos), column=0, columnspan=2, pady=8)
    # cuadro de búsqueda
    fila_buscar = tk.Frame(marco)
    fila_buscar.grid(row=len(campos) + 1, column=0, columnspan=2, sticky="w", pady=(0, 5))
    tk.Label(fila_buscar, text="Buscar:").pack(side="left")
    caja_buscar = tk.Entry(fila_buscar, width=40)
    caja_buscar.pack(side="left", padx=5)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=8)
    tabla.busqueda = caja_buscar
    for c in columnas:
        tabla.heading(c, text=c)
        tabla.column(c, width=120)
    tabla.grid(row=len(campos) + 2, column=0, columnspan=2)
    return entradas, botones, tabla


def poner_botones(marco, lista):
    for texto, funcion in lista:
        tk.Button(marco, text=texto, width=10, command=funcion).pack(side="left", padx=3)


def llenar(entradas, valores):
    for e, v in zip(entradas, valores):
        if isinstance(e, ttk.Combobox):
            e.set(v)
        else:
            e.delete(0, tk.END)
            e.insert(0, v)


def limpiar(entradas):
    for e in entradas:
        if isinstance(e, ttk.Combobox):
            e.set("")
        else:
            e.delete(0, tk.END)


# ---------------------- BÚSQUEDA ----------------------
def llenar_tabla(tabla, datos):
    # muestra solo las filas que contienen el texto del cuadro "Buscar" (en cualquier columna)
    texto = tabla.busqueda.get().strip().lower()
    tabla.delete(*tabla.get_children())
    for iid, f in datos.items():
        if texto in " ".join(str(x) for x in f[1:]).lower():
            tabla.insert("", tk.END, iid=iid, values=f[1:])


def activar_busqueda(tabla, datos):
    # cada vez que se suelta una tecla en el cuadro de búsqueda se vuelve a filtrar la tabla
    tabla.busqueda.bind("<KeyRelease>", lambda evento: llenar_tabla(tabla, datos))


# ---------------------- VENTANA GENÉRICA (plan, personal, turnos, asistencia, usuarios) ----------------------
def crear_modulo(cuaderno, titulo, campos, consulta, validar, sql_ins, sql_mod, sql_del, armar=None):
    """campos = lista de (etiqueta, tipo, origen, columna)
       tipo: "texto", "clave" (contraseña) o "lista" (desplegable).
       origen: para "lista", un SELECT (id, texto) o una lista fija de textos.
       consulta: SELECT cuya primera columna es el id y las demás siguen el orden de los campos
                 (el campo "clave" no se incluye)."""
    etiquetas = [c[0] for c in campos]
    combos = [i for i, c in enumerate(campos) if c[1] == "lista"]
    claves = [i for i, c in enumerate(campos) if c[1] == "clave"]
    columnas = [c[3] for c in campos if c[1] != "clave"]
    entradas, botones, tabla = crear_pestana(cuaderno, titulo, etiquetas, columnas, combos, claves)
    sel = [None]      # id del registro elegido
    datos = {}

    def cargar_listas():
        for i in combos:
            origen = campos[i][2]
            if isinstance(origen, list):
                entradas[i]["values"] = origen
            else:
                filas = ejecutar(origen, (), True)
                entradas[i]["values"] = [f"{f[0]} - {f[1]}" for f in filas]

    def mostrar():
        datos.clear()
        try:
            cargar_listas()
            filas = ejecutar(consulta, (), True)
        except Exception as e:
            mostrar_error(e)
            return
        for f in filas:
            datos[str(f[0])] = f
        llenar_tabla(tabla, datos)

    def limpiar_form():
        limpiar(entradas)
        sel[0] = None

    def elegir(evento):
        item = tabla.selection()
        if item:
            fila = datos[item[0]]
            sel[0] = fila[0]
            valores = []
            k = 1
            for i in range(len(campos)):
                if i in claves:
                    valores.append("")
                else:
                    valores.append("" if fila[k] is None else str(fila[k]))
                    k += 1
            llenar(entradas, valores)

    def convertir(valores):
        # de la lista desplegable se toma solo el id ("3 - Ana Pérez" -> "3"); un texto vacío pasa a NULL
        res = []
        for i, v in enumerate(valores):
            if i in combos:
                res.append(v.split(" - ")[0])
            else:
                res.append(v if v != "" else None)
        return res

    def guardar(nuevo):
        if not nuevo and sel[0] is None:
            messagebox.showwarning("Aviso", "Primero elija un registro de la tabla")
            return
        valores = [e.get().strip() for e in entradas]
        error = validar(valores, nuevo)
        if error:
            messagebox.showwarning("Validación", error)
            return
        d = convertir(valores)
        id_ = None if nuevo else sel[0]
        if armar:
            sql, params = armar(d, id_)
        elif nuevo:
            sql, params = sql_ins, tuple(d)
        else:
            sql, params = sql_mod, tuple(d) + (id_,)
        try:
            ejecutar(sql, params)
            messagebox.showinfo("Listo", "Registro guardado" if nuevo else "Registro modificado")
            limpiar_form()
            mostrar()
        except Exception as e:
            mostrar_error(e)

    def eliminar():
        if sel[0] is None:
            messagebox.showwarning("Aviso", "Primero elija un registro de la tabla")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que quiere eliminar este registro?"):
            return
        try:
            ejecutar(sql_del, (sel[0],))
            messagebox.showinfo("Listo", "Registro eliminado")
            limpiar_form()
            mostrar()
        except Exception as e:
            mostrar_error(e)

    tabla.bind("<<TreeviewSelect>>", elegir)
    activar_busqueda(tabla, datos)
    poner_botones(botones, [("Registrar", lambda: guardar(True)), ("Modificar", lambda: guardar(False)),
                            ("Eliminar", eliminar), ("Mostrar", mostrar), ("Limpiar", limpiar_form)])

    def refrescar():
        limpiar_form()
        mostrar()
    return refrescar


def armar_usuario(d, id_):
    # la contraseña se guarda encriptada (sha256), igual que la comprueba el login
    usuario, clave, estado, rol, personal = d
    if id_ is None:
        return ("insert into usuario (nombre_usuario, contrasena, estado, id_rol, id_personal) "
                "values (%s, %s, %s, %s, %s)",
                (usuario, hashlib.sha256(clave.encode()).hexdigest(), estado, rol, personal))
    if clave:
        return ("update usuario set nombre_usuario=%s, contrasena=%s, estado=%s, id_rol=%s, id_personal=%s "
                "where id_usuario=%s",
                (usuario, hashlib.sha256(clave.encode()).hexdigest(), estado, rol, personal, id_))
    return ("update usuario set nombre_usuario=%s, estado=%s, id_rol=%s, id_personal=%s "
            "where id_usuario=%s", (usuario, estado, rol, personal, id_))


# ---------------------- MATEMÁTICAS ----------------------
# Solo LEE datos (select), por eso no puede romper ninguna restricción del SQL.
# La tabla turno no guarda "mañana/tarde/noche": se deduce de hora_inicio.
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
DIAS_LARGO = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
FRANJAS = ["Mañana", "Tarde", "Noche"]


def franja_de(segundos):
    # mañana 06:00-13:59, tarde 14:00-21:59, noche 22:00-05:59
    hora = segundos // 3600
    if 6 <= hora < 14:
        return 0
    if 14 <= hora < 22:
        return 1
    return 2


def horas_de(seg_ini, seg_fin):
    # el CHECK de turno garantiza hora_inicio <> hora_fin; si fin < inicio el turno pasa de medianoche
    if seg_fin < seg_ini:
        seg_fin += 24 * 3600
    return (seg_fin - seg_ini) / 3600


def calcular_semana(filas, requeridas):
    # filas = (fecha, seg_inicio, seg_fin, id_personal, nombre) de los turnos de la semana
    D = [[0] * 7 for _ in range(3)]               # asignado: personas por franja y día
    personal = {}                                  # id -> [nombre, trabaja(0/1) por día, horas por día, turnos]
    for fecha, ini, fin, id_p, nombre in filas:
        ini, fin = int(ini), int(fin)
        d = fecha.weekday()                        # 0 = lunes ... 6 = domingo
        D[franja_de(ini)][d] += 1
        p = personal.setdefault(id_p, [str(nombre), [0] * 7, [0.0] * 7, 0])
        p[1][d] = 1
        p[2][d] += horas_de(ini, fin)
        p[3] += 1
    B = [[requeridas] * 7 for _ in range(3)]       # cobertura requerida
    A = [[D[i][j] - B[i][j] for j in range(7)] for i in range(3)]   # A = D - B
    return B, D, A, personal


def texto_matriz(titulo, filas, datos, signo=False):
    ancho = 18
    lineas = [titulo, "-" * (ancho + 6 * 7 + 7)]
    lineas.append("".ljust(ancho) + "".join(d.rjust(6) for d in DIAS) + "Suma".rjust(7))
    for nombre, fila in zip(filas, datos):
        celdas = "".join((f"{x:+g}" if signo and x else f"{x:g}").rjust(6) for x in fila)
        lineas.append(nombre[:ancho - 1].ljust(ancho) + celdas + f"{sum(fila):g}".rjust(7))
    sumas = [sum(f[j] for f in datos) for j in range(7)]
    lineas.append("Suma".ljust(ancho) + "".join(f"{x:g}".rjust(6) for x in sumas)
                  + f"{sum(sumas):g}".rjust(7))
    return "\n".join(lineas)


def grupos_edad(fechas, hoy):
    grupos = {"Menos de 65 años": 0, "65 a 79 años": 0, "80 años o más": 0}
    for f in fechas:
        edad = hoy.year - f.year - ((hoy.month, hoy.day) < (f.month, f.day))
        if edad < 65:
            grupos["Menos de 65 años"] += 1
        elif edad < 80:
            grupos["65 a 79 años"] += 1
        else:
            grupos["80 años o más"] += 1
    return grupos


def armar_reporte(filas, fechas_nac, lunes, requeridas, hoy):
    B, D, A, personal = calcular_semana(filas, requeridas)
    domingo = lunes + timedelta(days=6)
    out = [f"SEMANA DEL {lunes} AL {domingo}  (personas requeridas por turno: {requeridas})", ""]

    # 1. Porcentajes
    out.append("1. PORCENTAJES")
    total = len(fechas_nac)
    if total:
        out.append(f"Residentes por edad (total {total}): porcentaje = parte ÷ total × 100")
        for nombre, n in grupos_edad(fechas_nac, hoy).items():
            out.append(f"   {nombre}: {n} ÷ {total} × 100 = {n / total * 100:.1f} %")
    else:
        out.append("No hay residentes registrados.")
    completos = sum(1 for i in range(3) for j in range(7) if D[i][j] >= B[i][j])
    out.append(f"Cobertura de la semana: {completos} de 21 turnos completos = {completos / 21 * 100:.1f} %")
    out.append("")

    # 2. Matrices de turnos
    out.append("2. MATRICES DE TURNOS (3 horarios × 7 días = 21 turnos)")
    out.append(texto_matriz("Matriz B (cobertura requerida)", FRANJAS, B))
    out.append("")
    out.append(texto_matriz("Matriz D (asignado según la tabla turno)", FRANJAS, D))
    out.append("")
    out.append(texto_matriz("Matriz A = D - B  (0 = completo, negativo = falta personal)", FRANJAS, A, signo=True))
    faltas = [f"   - {DIAS_LARGO[j]} {lunes + timedelta(days=j)}, {FRANJAS[i].lower()}: "
              f"faltan {-A[i][j]} persona(s)" for i in range(3) for j in range(7) if A[i][j] < 0]
    out.append("")
    out.append("AVISO: turnos sin personal suficiente:" if faltas else "Todos los turnos tienen el personal requerido.")
    out.extend(faltas)
    out.append("")

    if not personal:
        out.append("No hay turnos registrados en esa semana, por eso no se calculan las matrices T y H.")
        return "\n".join(out)

    ids = sorted(personal)
    nombres = [personal[i][0] for i in ids]
    out.append(texto_matriz("Matriz T (1 = trabaja ese día, 0 = descansa)", nombres, [personal[i][1] for i in ids]))
    out.append("(la suma de cada fila son los días que trabaja la persona)")
    out.append("")

    # 3. Horas, promedio y derivada
    out.append("3. HORAS, PROMEDIO Y DERIVADA")
    out.append(texto_matriz("Matriz H (horas trabajadas, según hora_inicio y hora_fin)", nombres,
                            [personal[i][2] for i in ids]))
    horas = [sum(personal[i][2]) for i in ids]
    n = len(ids)
    prom = sum(horas) / n
    out.append("")
    out.append(f"Promedio por persona = {sum(horas):g} ÷ {n} = {prom:.1f} horas")
    out.append("f(h) = (h - promedio)²      f'(h) = 2·(h - promedio)      f'(h) = 0  →  h = promedio")
    out.append("Persona".ljust(18) + "h".rjust(8) + "h-prom".rjust(9) + "f(h)".rjust(10) + "f'(h)".rjust(9))
    for nombre, h in zip(nombres, horas):
        d = h - prom
        out.append(nombre[:17].ljust(18) + f"{h:g}".rjust(8) + f"{d:+.1f}".rjust(9)
                   + f"{d * d:.1f}".rjust(10) + f"{2 * d:+.1f}".rjust(9))
    turnos = sum(personal[i][3] for i in ids)
    base, extra = divmod(turnos, n)
    out.append("")
    out.append(f"Reparto más justo de {turnos} turnos entre {n} personas: "
               + (f"{extra} persona(s) con {base + 1} turnos y {n - extra} con {base} turnos."
                  if extra else f"todas con {base} turnos."))
    return "\n".join(out)


def calcular_matematicas(fecha_txt, req_txt, caja):
    f = fecha_valida(fecha_txt)
    if f is None:
        messagebox.showwarning("Validación", "Fecha inválida. Use el formato AAAA-MM-DD.")
        return
    if not req_txt.isdigit() or int(req_txt) < 1:
        messagebox.showwarning("Validación", "Las personas por turno deben ser un número entero mayor a 0.")
        return
    lunes = f.date() - timedelta(days=f.weekday())      # cualquier fecha sirve: se toma su semana
    try:
        filas = ejecutar("select t.fecha, time_to_sec(t.hora_inicio), time_to_sec(t.hora_fin), "
                         "t.id_personal, concat(p.nombres,' ',p.apellidos) from turno t "
                         "join personal p on t.id_personal = p.id_personal "
                         "where t.fecha between %s and %s",
                         (lunes, lunes + timedelta(days=6)), True)
        fechas_nac = [r[0] for r in ejecutar("select fecha_nac from residente", (), True)]
    except Exception as e:
        mostrar_error(e)
        return
    texto = armar_reporte(filas, fechas_nac, lunes, int(req_txt), datetime.now().date())
    caja.config(state="normal")
    caja.delete("1.0", tk.END)
    caja.insert("1.0", texto)
    caja.config(state="disabled")


def crear_pestana_matematicas(cuaderno):
    marco = tk.Frame(cuaderno, padx=10, pady=10)
    cuaderno.add(marco, text="Matemáticas")
    tk.Label(marco, text="Fecha de la semana (AAAA-MM-DD)").grid(row=0, column=0, sticky="w")
    ent_fecha = tk.Entry(marco, width=20)
    ent_fecha.grid(row=0, column=1, sticky="w", pady=2)
    ent_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
    tk.Label(marco, text="Personas requeridas por turno").grid(row=1, column=0, sticky="w")
    ent_req = tk.Entry(marco, width=20)
    ent_req.grid(row=1, column=1, sticky="w", pady=2)
    ent_req.insert(0, "1")
    caja = tk.Text(marco, width=90, height=24, font=("Courier New", 9), wrap="none", state="disabled")
    barra = ttk.Scrollbar(marco, command=caja.yview)
    caja.configure(yscrollcommand=barra.set)
    caja.grid(row=3, column=0, columnspan=2, sticky="nsew")
    barra.grid(row=3, column=2, sticky="ns")

    def calcular():
        calcular_matematicas(ent_fecha.get().strip(), ent_req.get().strip(), caja)
    tk.Button(marco, text="Calcular", width=10, command=calcular).grid(row=2, column=0, columnspan=2, pady=6)
    return calcular


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
        llenar_tabla(tabla_res, datos_res)

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
    activar_busqueda(tabla_res, datos_res)
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
        llenar_tabla(tabla_cui, datos_cui)

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
    activar_busqueda(tabla_cui, datos_cui)
    poner_botones(bot_cui, [("Registrar", registrar_cuidado), ("Modificar", modificar_cuidado),
                            ("Eliminar", eliminar_cuidado), ("Mostrar", mostrar_cuidados),
                            ("Limpiar", limpiar_cuidado)])

    # al cambiar de pestaña se recargan sus datos (así las listas desplegables siempre están actualizadas)
    refrescar = {"Residentes": lambda: (limpiar_residente(), mostrar_residentes()),
                 "Cuidados": lambda: (limpiar_cuidado(), mostrar_cuidados())}

    # ================= PLAN DE ATENCIÓN =================
    refrescar["Plan de atención"] = crear_modulo(
        cuaderno, "Plan de atención",
        [("Descripción (5-200)", "texto", None, "Descripción"),
         ("Fecha inicio (AAAA-MM-DD)", "texto", None, "Inicio"),
         ("Fecha fin (opcional)", "texto", None, "Fin"),
         ("Residente", "lista", "select id_residente, concat(nombres,' ',apellidos) from residente order by nombres",
          "Residente")],
        "select pl.id_plan, pl.descripcion, pl.fecha_inicio, ifnull(pl.fecha_fin,''), "
        "concat(r.id_residente,' - ',r.nombres,' ',r.apellidos) from plan_atencion pl "
        "join residente r on pl.id_residente = r.id_residente order by pl.id_plan",
        validar_plan,
        "insert into plan_atencion (descripcion, fecha_inicio, fecha_fin, id_residente) values (%s, %s, %s, %s)",
        "update plan_atencion set descripcion=%s, fecha_inicio=%s, fecha_fin=%s, id_residente=%s where id_plan=%s",
        "delete from plan_atencion where id_plan=%s")

    # ================= PERSONAL =================
    refrescar["Personal"] = crear_modulo(
        cuaderno, "Personal",
        [("Nombres", "texto", None, "Nombres"),
         ("Apellidos", "texto", None, "Apellidos"),
         ("Teléfono (8 dígitos, empieza con 6 o 7)", "texto", None, "Teléfono"),
         ("Cargo", "lista", "select id_cargo, nombre_cargo from cargo order by nombre_cargo", "Cargo")],
        "select p.id_personal, p.nombres, p.apellidos, p.telefono, concat(c.id_cargo,' - ',c.nombre_cargo) "
        "from personal p join cargo c on p.id_cargo = c.id_cargo order by p.id_personal",
        validar_personal,
        "insert into personal (nombres, apellidos, telefono, id_cargo) values (%s, %s, %s, %s)",
        "update personal set nombres=%s, apellidos=%s, telefono=%s, id_cargo=%s where id_personal=%s",
        "delete from personal where id_personal=%s")

    # ================= TURNOS =================
    refrescar["Turnos"] = crear_modulo(
        cuaderno, "Turnos",
        [("Fecha (AAAA-MM-DD)", "texto", None, "Fecha"),
         ("Hora inicio (HH:MM)", "texto", None, "Inicio"),
         ("Hora fin (HH:MM)", "texto", None, "Fin"),
         ("Personal", "lista", "select id_personal, concat(nombres,' ',apellidos) from personal order by nombres",
          "Personal")],
        "select t.id_turno, t.fecha, time_format(t.hora_inicio,'%H:%i'), time_format(t.hora_fin,'%H:%i'), "
        "concat(p.id_personal,' - ',p.nombres,' ',p.apellidos) from turno t "
        "join personal p on t.id_personal = p.id_personal order by t.fecha desc, t.hora_inicio",
        validar_turno,
        "insert into turno (fecha, hora_inicio, hora_fin, id_personal) values (%s, %s, %s, %s)",
        "update turno set fecha=%s, hora_inicio=%s, hora_fin=%s, id_personal=%s where id_turno=%s",
        "delete from turno where id_turno=%s")

    # ================= ASISTENCIA =================
    refrescar["Asistencia"] = crear_modulo(
        cuaderno, "Asistencia",
        [("Hora ingreso (HH:MM)", "texto", None, "Ingreso"),
         ("Hora salida (opcional)", "texto", None, "Salida"),
         ("Turno", "lista",
          "select t.id_turno, concat(t.fecha,' ',time_format(t.hora_inicio,'%H:%i'),'-',"
          "time_format(t.hora_fin,'%H:%i'),' ',p.nombres,' ',p.apellidos) from turno t "
          "join personal p on t.id_personal = p.id_personal order by t.fecha desc, t.hora_inicio", "Turno")],
        "select a.id_asistencia, time_format(a.hora_ingreso,'%H:%i'), ifnull(time_format(a.hora_salida,'%H:%i'),''), "
        "concat(t.id_turno,' - ',t.fecha,' ',time_format(t.hora_inicio,'%H:%i'),'-',"
        "time_format(t.hora_fin,'%H:%i'),' ',p.nombres,' ',p.apellidos) from asistencia a "
        "join turno t on a.id_turno = t.id_turno join personal p on t.id_personal = p.id_personal "
        "order by a.id_asistencia",
        validar_asistencia,
        "insert into asistencia (hora_ingreso, hora_salida, id_turno) values (%s, %s, %s)",
        "update asistencia set hora_ingreso=%s, hora_salida=%s, id_turno=%s where id_asistencia=%s",
        "delete from asistencia where id_asistencia=%s")

    # ================= USUARIOS =================
    refrescar["Usuarios"] = crear_modulo(
        cuaderno, "Usuarios",
        [("Usuario (4-15)", "texto", None, "Usuario"),
         ("Contraseña (mín. 8; vacía = no cambiar)", "clave", None, ""),
         ("Estado", "lista", ["activo", "inactivo"], "Estado"),
         ("Rol", "lista", "select id_rol, nombre_rol from rol order by nombre_rol", "Rol"),
         ("Personal", "lista", "select id_personal, concat(nombres,' ',apellidos) from personal order by nombres",
          "Personal")],
        "select u.id_usuario, u.nombre_usuario, u.estado, concat(r.id_rol,' - ',r.nombre_rol), "
        "concat(p.id_personal,' - ',p.nombres,' ',p.apellidos) from usuario u "
        "join rol r on u.id_rol = r.id_rol join personal p on u.id_personal = p.id_personal "
        "order by u.id_usuario",
        validar_usuario, None, None, "delete from usuario where id_usuario=%s", armar=armar_usuario)

    # ================= MATEMÁTICAS =================
    refrescar["Matemáticas"] = crear_pestana_matematicas(cuaderno)

    def al_cambiar_pestana(evento):
        nombre = cuaderno.tab(cuaderno.select(), "text")
        if nombre in refrescar:
            refrescar[nombre]()
    cuaderno.bind("<<NotebookTabChanged>>", al_cambiar_pestana)

    # al abrir, se muestran los datos de las dos primeras tablas
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

# Campo Usuario (etiqueta arriba, caja abajo)
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
