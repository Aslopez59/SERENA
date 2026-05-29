from datetime import datetime
from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombres: str = Field(index=True)
    correo: str = Field(index=True, unique=True)
    carrera: str
    semestre: int
    cedula: str = Field(index=True, unique=True)
    celular: str
    password: str
    fecha_registro: datetime = Field(default_factory=datetime.now)


class EntradaDiario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    estado_animo: str
    contenido: str
    fecha: datetime = Field(default_factory=datetime.now)


class MensajeChat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    mensaje_usuario: str
    respuesta_bot: str
    fecha: datetime = Field(default_factory=datetime.now)


class SolicitudBienestar(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    nivel_urgencia: str
    mensaje: str
    enviado_a: str
    fecha: datetime = Field(default_factory=datetime.now)


class RecuperacionClave(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    codigo: str
    usado: bool = False
    fecha: datetime = Field(default_factory=datetime.now)
