from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    nombres: str = Field(min_length=3)
    correo: str
    carrera: str
    semestre: int = Field(ge=1, le=10)
    cedula: str
    celular: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=8)


class UsuarioRead(BaseModel):
    id: int
    nombres: str
    correo: str
    carrera: str
    semestre: int
    cedula: str
    celular: str


class UsuarioUpdate(BaseModel):
    nombres: str | None = None
    carrera: str | None = None
    semestre: int | None = Field(default=None, ge=1, le=10)
    celular: str | None = Field(default=None, min_length=3, max_length=10)


class DiarioCreate(BaseModel):
    estado_animo: str
    contenido: str = Field(min_length=3)


class DiarioRead(BaseModel):
    id: int
    usuario_id: int
    estado_animo: str
    contenido: str


class BienestarCreate(BaseModel):
    nivel_urgencia: str
    mensaje: str = Field(min_length=5)
