from flask_appbuilder import ModelView, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func
import markdown

# Importación de servicios y esquemas del sistema
from .ia_service import consultar_ia  
from . import db
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
# VIEW REPORTES (UNIFICADA Y CORREGIDA)
# ==========================================
class ReportesView(BaseView):
    route_base = '/reportes'

    # 1. PANEL PRINCIPAL
    @expose("/principal")
    @has_access
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
    @has_access
    def estudiantes_por_curso(self):
        """Lista de cursos junto con la cantidad de alumnos inscritos evaluados por IA."""
        reporte_datos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.count(Inscripcion.id).label("total_inscritos")
            )
            .outerjoin(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        # Traducimos los datos a un texto comprensible para el prompt de la IA
        contexto_lineal = ", ".join([f"Curso: {d.curso} ({d.total_inscritos} alumnos)" for d in reporte_datos])

        prompt = (
            f"Actúa como un Director de Planificación Escolar. Analiza la siguiente distribución real de alumnos: {contexto_lineal}. "
            f"Genera un informe analítico estricto en Markdown usando exactamente este formato:\n"
            f"### Balance de Población Estudiantil\n"
            f"Escribe un párrafo analizando qué asignaturas tienen sobrepoblación o abandono.\n"
            f"**Recomendación de Infraestructura:** Agrega 2 sugerencias tácticas sobre el aforo de las aulas."
        )
        
        respuesta_raw = consultar_ia(prompt)
        analisis_html = markdown.markdown(respuesta_raw)

        return self.render_template(
            "reportes/estudiantes_por_curso.html",
            datos=reporte_datos,
            analisis_ia=analisis_html
        )

    # 3. REPORTE: RENDIMIENTO DE NOTAS POR CURSO
    @expose("/rendimiento-cursos")
    @has_access
    def rendimiento_cursos(self):
        """Muestra el promedio de notas de cada curso evaluado por IA."""
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

        contexto_lineal = ", ".join([f"Curso: {d.curso} (Promedio: {d.promedio_notas:.1f}, Max: {d.nota_maxima}, Min: {d.nota_minima})" for d in reporte_datos])

        prompt = (
            f"Actúa como una IA Evaluadora de Rendimiento. Analiza las siguientes calificaciones del sistema académico: {contexto_lineal}. "
            f"Genera un informe analítico estructurado en Markdown usando el formato:\n"
            f"### Auditoría de Promedios Académicos\n"
            f"Escribe un diagnóstico sobre las materias con rendimiento crítico y destacado.\n"
            f"**Plan de Nivelación:** Detalla 2 acciones institucionales para mitigar las notas mínimas encontradas."
        )
        
        respuesta_raw = consultar_ia(prompt)
        analisis_html = markdown.markdown(respuesta_raw)

        return self.render_template(
            "reportes/rendimiento_cursos.html",
            datos=reporte_datos,
            analisis_ia=analisis_html
        )

    # 4. REPORTE: CARGA HORARIA POR INSTRUCTOR
    @expose("/carga-instructores")
    @has_access
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

        contexto_lineal = ", ".join([f"Profesor: {d.nombres} {d.apellidos} ({d.total_horas} hrs totales distribuidas en {d.total_cursos} cursos)" for d in reporte_datos])

        prompt = (
            f"Actúa como un Auditor Académico experto. Evalúa el reparto de horas de los docentes basándote en los siguientes registros: {contexto_lineal}. "
            f"Genera un dictamen en Markdown bajo la estructura:\n"
            f"### Evaluación de Carga Horaria Docente\n"
            f"Escribe un análisis de equilibrio operativo con respecto a las horas académicas asignadas.\n"
            f"**Puntos Críticos:** Genera una lista con dos observaciones enfocadas en evitar el burnout docente."
        )
        
        respuesta_raw = consultar_ia(prompt)
        analisis_html = markdown.markdown(respuesta_raw)

        return self.render_template(
            "reportes/carga_instructores.html",
            datos=reporte_datos,
            analisis_ia=analisis_html
        )

    # 5. REPORTE: ESTADO DE APROBACIÓN GLOBAL
    @expose("/estado-aprobaciones")
    @has_access
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

        contexto_lineal = ", ".join([f"Estado: {d.estado_inscripcion} (Total: {d.total} alumnos)" for d in reporte_datos])

        prompt = (
            f"Actúa como un Analista de Calidad Educativa. Evalúa los índices de aprobación de la institución: {contexto_lineal}. "
            f"Genera un informe estratégico en Markdown usando el formato:\n"
            f"### Diagnóstico de Índices de Aprobación\n"
            f"Escribe una interpretación del porcentaje global de alumnos aprobados frente a los rezagados.\n"
            f"**Estrategias de Retención:** Plantea 2 mecanismos urgentes de tutoría pedagógica."
        )
        
        respuesta_raw = consultar_ia(prompt)
        analisis_html = markdown.markdown(respuesta_raw)

        return self.render_template(
            "reportes/estado_aprobaciones.html",
            datos=reporte_datos,
            analisis_ia=analisis_html
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