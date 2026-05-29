from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from database import SessionDep
from email_service import BIENESTAR_EMAIL
from models import EntradaDiario, SolicitudBienestar, Usuario
from schemas import BienestarCreate, DiarioCreate, DiarioRead, UsuarioCreate, UsuarioRead, UsuarioUpdate
from validators import validar_registro

router = APIRouter(prefix="/api", tags=["API SERENA"])


@router.get("/")
def api_home():
    return {"mensaje": "API de SERENA funcionando correctamente"}


@router.post("/usuarios/", response_model=UsuarioRead, status_code=201)
def crear_usuario(usuario: UsuarioCreate, session: SessionDep):
    datos = usuario.model_dump()
    errores = validar_registro(datos)
    if errores:
        raise HTTPException(status_code=400, detail=errores)

    usuario_existente = session.exec(select(Usuario).where(Usuario.correo == usuario.correo)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo.")

    db_usuario = Usuario(**datos)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


@router.get("/usuarios/", response_model=list[UsuarioRead])
def listar_usuarios(session: SessionDep, offset: int = 0, limit: int = Query(default=20, le=100)):
    usuarios = session.exec(select(Usuario).offset(offset).limit(limit)).all()
    return usuarios


@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    datos_actualizar = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizar.items():
        setattr(usuario, campo, valor)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()
    return {"ok": True, "mensaje": "Usuario eliminado"}


@router.post("/usuarios/{usuario_id}/diario", response_model=DiarioRead, status_code=201)
def crear_entrada_diario(usuario_id: int, datos: DiarioCreate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    entrada = EntradaDiario(usuario_id=usuario_id, estado_animo=datos.estado_animo, contenido=datos.contenido)
    session.add(entrada)
    session.commit()
    session.refresh(entrada)
    return entrada


@router.get("/usuarios/{usuario_id}/diario", response_model=list[DiarioRead])
def listar_diario_usuario(usuario_id: int, session: SessionDep, limit: int = Query(default=10, le=50)):
    entradas = session.exec(
        select(EntradaDiario)
        .where(EntradaDiario.usuario_id == usuario_id)
        .order_by(EntradaDiario.fecha.desc())
        .limit(limit)
    ).all()
    return entradas


@router.delete("/diario/{entrada_id}")
def eliminar_entrada_diario(entrada_id: int, session: SessionDep):
    entrada = session.get(EntradaDiario, entrada_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")

    session.delete(entrada)
    session.commit()
    return {"ok": True, "mensaje": "Entrada eliminada"}


@router.post("/usuarios/{usuario_id}/bienestar")
def crear_solicitud_bienestar(usuario_id: int, datos: BienestarCreate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    solicitud = SolicitudBienestar(
        usuario_id=usuario_id,
        nivel_urgencia=datos.nivel_urgencia,
        mensaje=datos.mensaje,
        enviado_a=BIENESTAR_EMAIL,
    )
    session.add(solicitud)
    session.commit()
    session.refresh(solicitud)

    return {"ok": True, "mensaje": "Solicitud registrada para Bienestar", "enviado_a": BIENESTAR_EMAIL}
