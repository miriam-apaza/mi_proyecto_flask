from datetime import datetime, timezone
from flask_appbuilder import Model
# Todos los tipos de datos requeridos importados correctamente
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Date
from sqlalchemy.orm import relationship


# =========================
# TABLA ESTUDIANTE
# =========================
class Estudiante(Model):
    __tablename__ = "estudiante"

    id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    ci = Column(String(20), unique=True, nullable=False)
    correo = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    estado = Column(Boolean, default=True)

    # Uso correcto de timezone.utc para evitar desfases de región
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    inscripciones = relationship(
        "Inscripcion",
        back_populates="estudiante"
    )

    def __repr__(self):
        return f"{self.nombres} {self.apellidos}"


# =========================
# TABLA INSTRUCTOR
# =========================
class Instructor(Model):
    __tablename__ = "instructor"

    id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=True)
    correo = Column(String(100), nullable=True)

    cursos = relationship(
        "Curso",
        back_populates="instructor"
    )

    def __repr__(self):
        return f"{self.nombres} {self.apellidos}"


# =========================
# TABLA CURSO (CORREGIDA)
# =========================
class Curso(Model):
    __tablename__ = "curso"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    # CORRECCIÓN: Se cambió nullable=False a True para limpiar los valores '0000-00-00'
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    
    carga_horaria = Column(Integer, nullable=False)

    instructor_id = Column(
        Integer,
        ForeignKey("instructor.id"),
        nullable=False
    )

    instructor = relationship(
        "Instructor",
        back_populates="cursos"
    )

    modulos = relationship(
        "Modulo",
        back_populates="curso"
    )

    inscripciones = relationship(
        "Inscripcion",
        back_populates="curso"
    )

    def __repr__(self):
        return self.nombre


# =========================
# TABLA MODULO
# =========================
class Modulo(Model):
    __tablename__ = "modulo"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    curso_id = Column(
        Integer,
        ForeignKey("curso.id"),
        nullable=False
    )

    curso = relationship(
        "Curso",
        back_populates="modulos"
    )

    def __repr__(self):
        return self.nombre


# =========================
# TABLA INSCRIPCION
# =========================
class Inscripcion(Model):
    __tablename__ = "inscripcion"

    id = Column(Integer, primary_key=True)

    estudiante_id = Column(
        Integer,
        ForeignKey("estudiante.id"),
        nullable=False
    )

    curso_id = Column(
        Integer,
        ForeignKey("curso.id"),
        nullable=False
    )

    fecha_inscripcion = Column(Date, nullable=False)
    nota_final = Column(Integer, nullable=True)
    estado = Column(String(20), nullable=False)  # APROBADO / REPROBADO

    estudiante = relationship(
        "Estudiante",
        back_populates="inscripciones"
    )

    curso = relationship(
        "Curso",
        back_populates="inscripciones"
    )

    def __repr__(self):
        return f"{self.estudiante} - {self.curso}"