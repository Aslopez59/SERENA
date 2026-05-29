import random

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from auth import cerrar_sesion, guardar_usuario_en_sesion, obtener_usuario_actual
from chatbot import responder_chatbot
from database import SessionDep
from email_service import BIENESTAR_EMAIL, enviar_correo
from models import EntradaDiario, MensajeChat, RecuperacionClave, SolicitudBienestar, Usuario
from validators import CARRERAS, SEMESTRES, validar_registro


router = APIRouter(tags=["Páginas HTML"])
templates = Jinja2Templates(directory="templates")


def volver_login_si_no_hay_usuario(request: Request, session: SessionDep):
    usuario = obtener_usuario_actual(request, session)
    if not usuario:
        return None
    return usuario


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/registro")
def registro_form(request: Request):
    return templates.TemplateResponse(
        "registro.html",
        {
            "request": request,
            "errores": [],
            "form_data": {},
            "carreras": CARRERAS,
            "semestres": SEMESTRES,
        },
    )


@router.post("/registro")
def registrar_usuario(
    request: Request,
    session: SessionDep,
    nombres: str = Form(...),
    correo: str = Form(...),
    carrera: str = Form(...),
    semestre: str = Form(...),
    cedula: str = Form(...),
    celular: str = Form(...),
    password: str = Form(...),
):
    datos = {
        "nombres": nombres.strip(),
        "correo": correo.strip().lower(),
        "carrera": carrera,
        "semestre": semestre,
        "cedula": cedula.strip(),
        "celular": celular.strip(),
        "password": password,
    }

    errores = validar_registro(datos)

    existe_correo = session.exec(
        select(Usuario).where(Usuario.correo == datos["correo"])
    ).first()

    if existe_correo:
        errores.append("Ya existe un usuario registrado con ese correo.")

    existe_cedula = session.exec(
        select(Usuario).where(Usuario.cedula == datos["cedula"])
    ).first()

    if existe_cedula:
        errores.append("Ya existe un usuario registrado con esa cédula.")

    if errores:
        return templates.TemplateResponse(
            "registro.html",
            {
                "request": request,
                "errores": errores,
                "form_data": datos,
                "carreras": CARRERAS,
                "semestres": SEMESTRES,
            },
        )

    usuario = Usuario(
        nombres=datos["nombres"],
        correo=datos["correo"],
        carrera=datos["carrera"],
        semestre=int(datos["semestre"]),
        cedula=datos["cedula"],
        celular=datos["celular"],
        password=datos["password"],
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    guardar_usuario_en_sesion(request, usuario)

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "errores": [],
        },
    )


@router.post("/login")
def login(
    request: Request,
    session: SessionDep,
    correo: str = Form(...),
    password: str = Form(...),
):
    usuario = session.exec(
        select(Usuario).where(Usuario.correo == correo.strip().lower())
    ).first()

    if not usuario or usuario.password != password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "errores": ["Correo o contraseña incorrectos."],
            },
        )

    guardar_usuario_en_sesion(request, usuario)

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/logout")
def logout(request: Request):
    cerrar_sesion(request)
    return RedirectResponse(url="/", status_code=303)


@router.get("/dashboard")
def dashboard(request: Request, session: SessionDep):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
        },
    )


@router.get("/chatbot")
def chatbot_form(request: Request, session: SessionDep):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    mensajes = session.exec(
        select(MensajeChat)
        .where(MensajeChat.usuario_id == usuario.id)
        .order_by(MensajeChat.fecha.desc())
        .limit(8)
    ).all()

    return templates.TemplateResponse(
        "chatbot.html",
        {
            "request": request,
            "usuario": usuario,
            "mensajes": mensajes,
        },
    )


@router.post("/chatbot")
def enviar_mensaje_chatbot(
    request: Request,
    session: SessionDep,
    estado_animo: str = Form(...),
    mensaje: str = Form(...),
):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    respuesta = responder_chatbot(mensaje, estado_animo)

    mensaje_completo = f"Estado de ánimo: {estado_animo}. Mensaje: {mensaje}"

    chat = MensajeChat(
        usuario_id=usuario.id,
        mensaje_usuario=mensaje_completo,
        respuesta_bot=respuesta,
    )

    session.add(chat)
    session.commit()

    return RedirectResponse(url="/chatbot", status_code=303)

@router.get("/diario")
def diario_form(request: Request, session: SessionDep):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    entradas = session.exec(
        select(EntradaDiario)
        .where(EntradaDiario.usuario_id == usuario.id)
        .order_by(EntradaDiario.fecha.desc())
    ).all()

    return templates.TemplateResponse(
        "diario.html",
        {
            "request": request,
            "usuario": usuario,
            "entradas": entradas,
        },
    )


@router.post("/diario")
def guardar_diario(
    request: Request,
    session: SessionDep,
    estado_animo: str = Form(...),
    contenido: str = Form(...),
):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    entrada = EntradaDiario(
        usuario_id=usuario.id,
        estado_animo=estado_animo,
        contenido=contenido,
    )

    session.add(entrada)
    session.commit()

    return RedirectResponse(url="/diario", status_code=303)


@router.get("/bienestar")
def bienestar_form(request: Request, session: SessionDep):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "bienestar.html",
        {
            "request": request,
            "usuario": usuario,
            "mensaje_ok": None,
        },
    )


@router.post("/bienestar")
def enviar_bienestar(
    request: Request,
    session: SessionDep,
    nivel_urgencia: str = Form(...),
    mensaje: str = Form(...),
):
    usuario = volver_login_si_no_hay_usuario(request, session)

    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    solicitud = SolicitudBienestar(
        usuario_id=usuario.id,
        nivel_urgencia=nivel_urgencia,
        mensaje=mensaje,
        enviado_a=BIENESTAR_EMAIL,
    )

    session.add(solicitud)
    session.commit()

    contenido_correo = f"""
Solicitud de apoyo desde SERENA

Nombre: {usuario.nombres}
Correo institucional: {usuario.correo}
Carrera: {usuario.carrera}
Semestre: {usuario.semestre}
Celular: {usuario.celular}
Nivel de urgencia: {nivel_urgencia}

Mensaje:
{mensaje}
"""

    enviado = enviar_correo(
        BIENESTAR_EMAIL,
        "Solicitud de apoyo SERENA",
        contenido_correo,
    )

    texto = "Solicitud registrada."

    if enviado:
        texto += " También fue enviada al correo de Bienestar SERENA."
    else:
        texto += " El correo no se envió porque falta configurar SMTP, pero quedó guardada en la base de datos."

    return templates.TemplateResponse(
        "bienestar.html",
        {
            "request": request,
            "usuario": usuario,
            "mensaje_ok": texto,
        },
    )


@router.get("/reportes", response_class=HTMLResponse)
def ver_reportes(request: Request, session: SessionDep):
    total_usuarios = len(session.exec(select(Usuario)).all())
    total_diarios = len(session.exec(select(EntradaDiario)).all())
    total_chats = len(session.exec(select(MensajeChat)).all())
    total_bienestar = len(session.exec(select(SolicitudBienestar)).all())

    solicitudes = session.exec(select(SolicitudBienestar)).all()

    urgencia_baja = 0
    urgencia_media = 0
    urgencia_alta = 0

    for solicitud in solicitudes:
        if solicitud.nivel_urgencia == "Baja":
            urgencia_baja += 1
        elif solicitud.nivel_urgencia == "Media":
            urgencia_media += 1
        elif solicitud.nivel_urgencia == "Alta":
            urgencia_alta += 1

    porcentaje_baja = urgencia_baja * 20
    porcentaje_media = urgencia_media * 20
    porcentaje_alta = urgencia_alta * 20

    if porcentaje_baja > 100:
        porcentaje_baja = 100

    if porcentaje_media > 100:
        porcentaje_media = 100

    if porcentaje_alta > 100:
        porcentaje_alta = 100

    return templates.TemplateResponse(
        "reportes.html",
        {
            "request": request,
            "total_usuarios": total_usuarios,
            "total_diarios": total_diarios,
            "total_chats": total_chats,
            "total_bienestar": total_bienestar,
            "urgencia_baja": urgencia_baja,
            "urgencia_media": urgencia_media,
            "urgencia_alta": urgencia_alta,
            "porcentaje_baja": porcentaje_baja,
            "porcentaje_media": porcentaje_media,
            "porcentaje_alta": porcentaje_alta,
        },
    )


@router.get("/recuperar-clave")
def recuperar_clave_form(request: Request):
    return templates.TemplateResponse(
        "recuperar_clave.html",
        {
            "request": request,
            "mensaje": None,
            "errores": [],
        },
    )


@router.post("/recuperar-clave")
def recuperar_clave(
    request: Request,
    session: SessionDep,
    correo: str = Form(...),
):
    usuario = session.exec(
        select(Usuario).where(Usuario.correo == correo.strip().lower())
    ).first()

    if not usuario:
        return templates.TemplateResponse(
            "recuperar_clave.html",
            {
                "request": request,
                "mensaje": None,
                "errores": ["No existe un usuario con ese correo."],
            },
        )

    codigo = str(random.randint(100000, 999999))

    recuperacion = RecuperacionClave(
        usuario_id=usuario.id,
        codigo=codigo,
    )

    session.add(recuperacion)
    session.commit()

    enviado = enviar_correo(
        usuario.correo,
        "Código de recuperación SERENA",
        f"Tu código de recuperación es: {codigo}",
    )

    if enviado:
        mensaje = "Se envió un código al correo institucional registrado."
    else:
        mensaje = f"SMTP no está configurado. Para prueba académica, el código generado es: {codigo}"

    return templates.TemplateResponse(
        "recuperar_clave.html",
        {
            "request": request,
            "mensaje": mensaje,
            "errores": [],
        },
    )