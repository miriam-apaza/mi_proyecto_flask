from flask_appbuilder import ModelView, BaseView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func

# IMPORTANTE: Asegúrate de que este import coincida con la forma en que
# inicializaste appbuilder y db en el archivo __init__.py de tu app.
from app import appbuilder, db

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
# VIEW REPORTES
# ==========================================
class ReportesView(BaseView):
    route_base = '/reportes'

    # 1. PANEL PRINCIPAL
    @expose("/principal")
    def panel_principal(self):
        """Muestra un resumen general del estado académico de la institución."""
        total_estudiantes = db.session.query(Estudiante).filter_by(estado=True).count()
        total_cursos = db.session.query(Curso).count()
        total_inscripciones = db.session.query(Inscripcion).count()
        
        return self.render_template(
            "reportes/index.html",
            total_estudiantes=total_estudiantes,
            total_cursos=total_cursos,
            total_inscripciones=total_inscripciones
        )

    # 2. REPORTE: ESTUDIANTES POR CURSO
    @expose("/estudiantes-por-curso")
    def estudiantes_por_curso(self):
        """Devuelve la lista de cursos junto con la cantidad de alumnos inscritos en cada uno."""
        reporte_datos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.count(Inscripcion.id).label("total_inscritos")
            )
            .outerjoin(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        return self.render_template(
            "reportes/estudiantes_por_curso.html",
            datos=reporte_datos
        )

    # 3. REPORTE: RENDIMIENTO DE NOTAS POR CURSO
    @expose("/rendimiento-cursos")
    def rendimiento_cursos(self):
        """Muestra el promedio de notas, la nota más alta y la más baja de cada curso."""
        reporte_datos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.avg(Inscripcion.nota_final).label("promedio_notas"),
                func.max(Inscripcion.nota_final).label("nota_maxima"),
                func.min(Inscripcion.nota_final).label("nota_minima")
            )
            .join(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        return self.render_template(
            "reportes/rendimiento_cursos.html",
            datos=reporte_datos
        )

    # 4. REPORTE: CARGA HORARIA POR INSTRUCTOR
    @expose("/carga-instructores")
    def carga_instructores(self):
        """Suma la carga horaria total de todos los cursos asignados a cada instructor."""
        reporte_datos = (
            db.session.query(
                Instructor.nombres,
                Instructor.apellidos,
                func.sum(Curso.carga_horaria).label("total_horas"),
                func.count(Curso.id).label("total_cursos")
            )
            .join(Curso, Instructor.id == Curso.instructor_id)
            .group_by(Instructor.id)
            .all()
        )

        return self.render_template(
            "reportes/carga_instructores.html",
            datos=reporte_datos
        )

    # 5. REPORTE: ESTADO DE APROBACIÓN GLOBAL
    @expose("/estado-aprobaciones")
    def estado_aprobaciones(self):
        """Muestra cuántos alumnos están en estado APROBADO o REPROBADO."""
        reporte_datos = (
            db.session.query(
                Inscripcion.estado.label("estado_inscripcion"),
                func.count(Inscripcion.id).label("total")
            )
            .group_by(Inscripcion.estado)
            .all()
        )

        return self.render_template(
            "reportes/estado_aprobaciones.html",
            datos=reporte_datos
        )


# ==========================================
# REGISTRO DE TODAS LAS VISTAS
# ==========================================

# MENÚ: Academico
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

# MENÚ: Reportes
appbuilder.add_view(
    ReportesView,
    "Panel de Control",
    icon="fa-chart-pie",
    href="/reportes/principal",
    category="Reportes",
    category_icon="fa-file-alt"
)

appbuilder.add_link(
    "Estudiantes por Curso",
    href="/reportes/estudiantes-por-curso",
    icon="fa-graduation-cap",
    category="Reportes"
)

appbuilder.add_link(
    "Rendimiento Académico",
    href="/reportes/rendimiento-cursos",
    icon="fa-trophy",
    category="Reportes"
)

appbuilder.add_link(
    "Carga de Instructores",
    href="/reportes/carga-instructores",
    icon="fa-clock",
    category="Reportes"
)

appbuilder.add_link(
    "Estado de Aprobaciones",
    href="/reportes/estado-aprobaciones",
    icon="fa-check-circle",
    category="Reportes"
)