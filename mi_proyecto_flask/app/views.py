from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

# IMPORTANTE: Debes importar la instancia de appbuilder desde tu app. 
# Por ejemplo: desde tu paquete raíz o donde lo hayas inicializado.
from app import appbuilder 

from .models import (
    Estudiante,
    Instructor,
    Curso,
    Modulo,
    Inscripcion
)


# ==========================================
# VIEW ESTUDIANTE
# ==========================================
class EstudianteModelView(ModelView):
    datamodel = SQLAInterface(Estudiante)

    label_columns = {
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "ci": "CI",
        "correo": "Correo",
        "telefono": "Teléfono",
        "estado": "Estado",
        "creado_en": "Creado en"
    }

    list_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    add_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    edit_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    show_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado", "creado_en"]


# ==========================================
# VIEW INSTRUCTOR
# ==========================================
class InstructorModelView(ModelView):
    datamodel = SQLAInterface(Instructor)

    label_columns = {
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "especialidad": "Especialidad",
        "correo": "Correo"
    }

    list_columns = ["nombres", "apellidos", "especialidad", "correo"]
    add_columns = ["nombres", "apellidos", "especialidad", "correo"]
    edit_columns = ["nombres", "apellidos", "especialidad", "correo"]
    show_columns = ["nombres", "apellidos", "especialidad", "correo"]


# ==========================================
# VIEW CURSO
# ==========================================
class CursoModelView(ModelView):
    datamodel = SQLAInterface(Curso)

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "fecha_inicio": "Fecha Inicio",
        "fecha_fin": "Fecha Fin",
        "carga_horaria": "Carga Horaria",
        "instructor": "Instructor"
    }

    list_columns = ["nombre", "fecha_inicio", "fecha_fin", "carga_horaria", "instructor"]
    add_columns = ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "carga_horaria", "instructor"]
    edit_columns = ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "carga_horaria", "instructor"]
    show_columns = ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "carga_horaria", "instructor"]


# ==========================================
# VIEW MODULO
# ==========================================
class ModuloModelView(ModelView):
    datamodel = SQLAInterface(Modulo)

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "curso": "Curso"
    }

    list_columns = ["nombre", "curso"]
    add_columns = ["nombre", "descripcion", "curso"]
    edit_columns = ["nombre", "descripcion", "curso"]
    show_columns = ["nombre", "descripcion", "curso"]


# ==========================================
# VIEW INSCRIPCION
# ==========================================
class InscripcionModelView(ModelView):
    datamodel = SQLAInterface(Inscripcion)

    label_columns = {
        "estudiante": "Estudiante",
        "curso": "Curso",
        "fecha_inscripcion": "Fecha Inscripción",
        "nota_final": "Nota Final",
        "estado": "Estado"
    }

    list_columns = ["estudiante", "curso", "nota_final", "estado"]
    add_columns = ["estudiante", "curso", "fecha_inscripcion", "nota_final", "estado"]
    edit_columns = ["estudiante", "curso", "fecha_inscripcion", "nota_final", "estado"]
    show_columns = ["estudiante", "curso", "fecha_inscripcion", "nota_final", "estado"]


# ==========================================
# REGISTRO DE VISTAS
# ==========================================

appbuilder.add_view(
    EstudianteModelView,
    "Estudiantes",
    icon="fa-user",
    category="Academico",
    category_icon="fa-graduation-cap"
)

appbuilder.add_view(
    InstructorModelView,
    "Instructores",
    icon="fa-users",
    category="Academico",
    category_icon="fa-graduation-cap"
)

appbuilder.add_view(
    CursoModelView,
    "Cursos",
    icon="fa-book",
    category="Academico",
    category_icon="fa-graduation-cap"
)

appbuilder.add_view(
    ModuloModelView,
    "Módulos",
    icon="fa-list",
    category="Academico",
    category_icon="fa-graduation-cap"
)

appbuilder.add_view(
    InscripcionModelView,
    "Inscripciones",
    icon="fa-edit",
    category="Academico",
    category_icon="fa-graduation-cap"
)