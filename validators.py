import re

CARRERAS = [
    "Administración de Empresas",
    "Arquitectura",
    "Contaduría Pública",
    "Derecho",
    "Economía",
    "Ingeniería Civil",
    "Ingeniería de Sistemas",
    "Ingeniería Electrónica",
    "Ingeniería Industrial",
    "Psicología",
]

SEMESTRES = list(range(1, 11))


def validar_correo_institucional(correo: str) -> bool:
    return correo.endswith("@ucatolica.edu.co") or correo.endswith("@ucatolica.edu.co.co") or correo.endswith("@ucatolica.edu.co")


def solo_numeros(texto: str) -> bool:
    return texto.isdigit()


def validar_registro(datos: dict) -> list[str]:
    errores = []

    campos = ["nombres", "correo", "carrera", "semestre", "cedula", "celular", "password"]
    for campo in campos:
        if not datos.get(campo):
            errores.append(f"El campo {campo} es obligatorio.")

    correo = datos.get("correo", "")
    if correo and not validar_correo_institucional(correo):
        errores.append("El correo debe ser institucional y terminar en @ucatolica.edu.co.")

    if datos.get("carrera") and datos["carrera"] not in CARRERAS:
        errores.append("Debe seleccionar una carrera válida.")

    try:
        semestre = int(datos.get("semestre", 0))
        if semestre < 1 or semestre > 10:
            errores.append("El semestre debe estar entre 1 y 10.")
    except ValueError:
        errores.append("El semestre debe ser un número válido.")

    cedula = datos.get("cedula", "")
    if cedula and not solo_numeros(cedula):
        errores.append("La cédula solo debe contener números.")

    celular = datos.get("celular", "")
    if celular:
        if not solo_numeros(celular):
            errores.append("El celular solo debe contener números.")
        if len(celular) < 3 or len(celular) > 10:
            errores.append("El celular debe tener mínimo 3 dígitos y máximo 10.")

    password = datos.get("password", "")
    if password:
        errores_pw = []
        if len(password) < 8:
            errores_pw.append("mínimo 8 caracteres")
        if not re.search(r"[A-Za-z]", password):
            errores_pw.append("al menos una letra")
        if not re.search(r"\d", password):
            errores_pw.append("al menos un número")
        if not re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?`~\\|]", password):
            errores_pw.append("al menos un carácter especial (ej: !@#$%)")
        if errores_pw:
            errores.append("La contraseña debe tener: " + ", ".join(errores_pw) + ".")

    return errores
