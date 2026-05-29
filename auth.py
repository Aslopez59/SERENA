from fastapi import Request
from sqlmodel import Session

from models import Usuario


def guardar_usuario_en_sesion(request: Request, usuario: Usuario):
    request.session["usuario_id"] = usuario.id
    request.session["usuario_nombre"] = usuario.nombres


def cerrar_sesion(request: Request):
    request.session.clear()


def obtener_usuario_actual(request: Request, session: Session) -> Usuario | None:
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    return session.get(Usuario, usuario_id)
