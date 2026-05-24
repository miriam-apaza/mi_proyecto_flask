import markdown
from flask_appbuilder import BaseView, ModelView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func

# Importación core de la app
from app import appbuilder, db

# Importación de servicios y esquemas del sistema
from .ia_service import consultar_ia
from .models import Curso, Estudiante, Inscripcion, Instructor, Modulo


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
        "creado_en": "Creado en",
    }

    list_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    add_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    edit_columns = ["nombres", "apellidos", "ci", "correo", "telefono", "estado"]
    show_columns = [
        "nombres",
        "apellidos",
        "ci",
        "correo",
        "telefono",
        "estado",
        "creado_en",
    ]


# ==========================================
# VIEW INSTRUCTOR
# ==========================================
class InstructorModelView(ModelView):
    datamodel = SQLAInterface(Instructor)

    label_columns = {
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "especialidad": "Especialidad",
        "correo": "Correo",
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
        "instructor": "Instructor",
    }

    list_columns = [
        "nombre",
        "fecha_inicio",
        "fecha_fin",
        "carga_horaria",
        "instructor",
    ]
    add_columns = [
        "nombre",
        "descripcion",
        "fecha_inicio",
        "fecha_fin",
        "carga_horaria",
        "instructor",
    ]
    edit_columns = [
        "nombre",
        "descripcion",
        "fecha_inicio",
        "fecha_fin",
        "carga_horaria",
        "instructor",
    ]
    show_columns = [
        "nombre",
        "descripcion",
        "fecha_inicio",
        "fecha_fin",
        "carga_horaria",
        "instructor",
    ]


# ==========================================
# VIEW MODULO
# ==========================================
class ModuloModelView(ModelView):
    datamodel = SQLAInterface(Modulo)

    label_columns = {"nombre": "Nombre", "descripcion": "Descripción", "curso": "Curso"}

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
        "estado": "Estado",
    }

    list_columns = ["estudiante", "curso", "nota_final", "estado"]
    add_columns = [
        "estudiante",
        "curso",
        "fecha_inscripcion",
        "nota_final",
        "estado",
    ]
    edit_columns = [
        "estudiante",
        "curso",
        "fecha_inscripcion",
        "nota_final",
        "estado",
    ]
    show_columns = [
        "estudiante",
        "curso",
        "fecha_inscripcion",
        "nota_final",
        "estado",
    ]


# ==========================================
# VIEW REPORTES (BLINDADA INTEGRALMENTE CON PLAN B)
# ==========================================
class ReportesView(BaseView):
    route_base = "/reportes"

    # 1. PANEL PRINCIPAL
    @expose("/principal")
    @has_access
    def panel_principal(self):
        """Muestra un resumen general del estado académico analizado por IA o soporte local."""
        total_estudiantes = db.session.query(Estudiante).filter_by(estado=True).count() or 0
        total_cursos = db.session.query(Curso).count() or 0
        total_inscripciones = db.session.query(Inscripcion).count() or 0

        datos_cursos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.count(Inscripcion.id).label("total_inscritos")
            )
            .outerjoin(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        datos_aprobaciones = (
            db.session.query(
                Inscripcion.estado.label("estado_inscripcion"),
                func.count(Inscripcion.id).label("total")
            )
            .group_by(Inscripcion.estado)
            .all()
        )

        contexto_cursos = ", ".join([f"{c.curso} ({c.total_inscritos} alumnos)" for c in datos_cursos]) if datos_cursos else "Sin registros"
        contexto_aprobaciones = ", ".join([f"{a.estado_inscripcion or 'Sin Estado'}: {a.total} alumnos" for a in datos_aprobaciones]) if datos_aprobaciones else "Sin registros"

        prompt = (
            f"Actúa como un Auditor Académico Institucional de alto nivel. Analiza los siguientes números generales:\n"
            f"- Total de Estudiantes Activos: {total_estudiantes}\n"
            f"- Total de Asignaturas: {total_cursos}\n"
            f"- Inscripciones registradas: {total_inscripciones}\n"
            f"- Alumnos por Curso: {contexto_cursos}\n"
            f"- Balances de Aprobación: {contexto_aprobaciones}\n\n"
            f"Genera un diagnóstico sumamente ejecutivo y estratégico en Markdown utilizando exactamente esta estructura:\n"
            f"### Diagnóstico de Situación Institucional\n"
            f"Escribe un breve párrafo analizando la tracción global de alumnos e inscritos actuales.\n"
            f"**Recomendación de Retención Directa:** Agrega 2 consejos ágiles para mejorar el rendimiento colectivo."
        )

        try:
            respuesta_raw = consultar_ia(prompt)
            # Forzamos fallo si la IA devuelve un string vacío o mensaje de error simulado
            if not respuesta_raw or "Error" in respuesta_raw:
                raise ValueError("Respuesta nula o errónea de la API externa.")
            analisis_html = markdown.markdown(respuesta_raw)
        except Exception:
            # PLAN B AUTOMÁTICO LOCAL
            resp_local = (
                f"### Diagnóstico de Situación Institucional (Soporte Local)\n"
                f"El ecosistema académico cuenta actualmente con un total de **{total_estudiantes} estudiantes activos** distribuidos en **{total_cursos} asignaturas**, "
                f"acumulando **{total_inscripciones} registros de inscripción** históricos. Los gráficos superiores muestran el balance actual del aforo académico.\n\n"
                f"**Recomendación de Retención Directa:**\n"
                f"1. Monitorear los cursos con mayor afluencia estudiantil para equilibrar la carga de usuarios.\n"
                f"2. Establecer esquemas de acompañamiento preventivo en las asignaturas con menor tasa de aprobación."
            )
            analisis_html = markdown.markdown(resp_local)

        return self.render_template(
            "reportes/index.html",
            total_estudiantes=total_estudiantes,
            total_cursos=total_cursos,
            total_inscripciones=total_inscripciones,
            datos_cursos=datos_cursos,
            datos_aprobaciones=datos_aprobaciones,
            analisis_ia=analisis_html
        )

    # 2. REPORTE: ESTUDIANTES POR CURSO
    @expose("/estudiantes-por-curso")
    @has_access
    def estudiantes_por_curso(self):
        """Lista de cursos junto con la cantidad de alumnos inscritos evaluados por IA o soporte local."""
        reporte_datos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.count(Inscripcion.id).label("total_inscritos"),
            )
            .outerjoin(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        contexto_lineal = ", ".join(
            [f"Curso: {d.curso} ({d.total_inscritos or 0} alumnos)" for d in reporte_datos]
        ) if reporte_datos else "Sin cursos registrados"

        prompt = (
            f"Actúa como un Director de Planificación Escolar. Analiza la siguiente distribución real de alumnos: {contexto_lineal}. "
            f"Genera un informe analítico estricto en Markdown usando exactamente este formato:\n"
            f"### Balance de Población Estudiantil\n"
            f"Escribe un párrafo analizando qué asignaturas tienen sobrepoblación o abandono.\n"
            f"**Recomendación de Infraestructura:** Agrega 2 sugerencias tácticas sobre el aforo de las aulas."
        )

        try:
            respuesta_raw = consultar_ia(prompt)
            if not respuesta_raw or "Error" in respuesta_raw:
                raise ValueError()
            analisis_html = markdown.markdown(respuesta_raw)
        except Exception:
            resp_local = (
                f"### Balance de Población Estudiantil (Soporte Local)\n"
                f"El análisis de distribución de matrícula indica que las asignaturas integradas cuentan con una carga de aforo "
                f"que requiere supervisión continua. Las métricas actuales se encuentran listadas detalladamente en el cuadro analítico.\n\n"
                f"**Recomendación de Infraestructura:**\n"
                f"1. Evaluar la capacidad física de las aulas asignadas a las asignaturas de alta demanda.\n"
                f"2. Fomentar la apertura de paralelos virtuales si la densidad por aula supera el óptimo recomendado."
            )
            analisis_html = markdown.markdown(resp_local)

        return self.render_template(
            "reportes/estudiantes_por_curso.html",
            datos=reporte_datos,
            analisis_ia=analisis_html,
        )

    # 3. REPORTE: RENDIMIENTO DE NOTAS POR CURSO
    @expose("/rendimiento-cursos")
    @has_access
    def rendimiento_cursos(self):
        """Muestra el promedio de notas de cada curso evaluado por IA o soporte local."""
        reporte_datos = (
            db.session.query(
                Curso.nombre.label("curso"),
                func.avg(Inscripcion.nota_final).label("promedio_notas"),
                func.max(Inscripcion.nota_final).label("nota_maxima"),
                func.min(Inscripcion.nota_final).label("nota_minima"),
            )
            .join(Inscripcion, Curso.id == Inscripcion.curso_id)
            .group_by(Curso.id)
            .all()
        )

        contexto_lineal = ", ".join(
            [
                f"Curso: {d.curso} (Promedio: {d.promedio_notas:.1f} o 0.0 si no aplica, Max: {d.nota_maxima or 0}, Min: {d.nota_minima or 0})"
                if d.promedio_notas is not None else
                f"Curso: {d.curso} (Promedio: 0.0, Max: 0, Min: 0)"
                for d in reporte_datos
            ]
        ) if reporte_datos else "Sin calificaciones"

        prompt = (
            f"Actúa como una IA Evaluadora de Rendimiento. Analiza las siguientes calificaciones del sistema académico: {contexto_lineal}. "
            f"Genera un informe analítico estructurado en Markdown usando el formato:\n"
            f"### Auditoría de Promedios Académicos\n"
            f"Escribe un diagnóstico sobre las materias con rendimiento crítico y destacado.\n"
            f"**Plan de Nivelación:** Detalla 2 acciones institucionales para mitigar las notas mínimas encontradas."
        )

        try:
            respuesta_raw = consultar_ia(prompt)
            if not respuesta_raw or "Error" in respuesta_raw:
                raise ValueError()
            analisis_html = markdown.markdown(respuesta_raw)
        except Exception:
            resp_local = (
                f"### Auditoría de Promedios Académicos (Soporte Local)\n"
                f"Los promedios y calificaciones calculadas reflejan el estado dinámico del rendimiento por asignatura. Se detectan brechas "
                f"estándar entre las calificaciones máximas y mínimas de los periodos evaluados.\n\n"
                f"**Plan de Nivelación:**\n"
                f"1. Implementar un banco de talleres complementarios antes de los cierres parciales de ciclo.\n"
                f"2. Uniformar los criterios de evaluación entre asignaturas correlativas para asegurar equidad."
            )
            analisis_html = markdown.markdown(resp_local)

        return self.render_template(
            "reportes/rendimiento_cursos.html",
            datos=reporte_datos,
            analisis_ia=analisis_html,
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
                func.count(Curso.id).label("total_cursos"),
            )
            .join(Curso, Instructor.id == Curso.instructor_id)
            .group_by(Instructor.id)
            .all()
        )

        contexto_lineal = ", ".join(
            [
                f"Profesor: {d.nombres} {d.apellidos} ({d.total_horas or 0} hrs totales en {d.total_cursos or 0} cursos)"
                for d in reporte_datos
            ]
        ) if reporte_datos else "Sin asignación docente"

        prompt = (
            f"Actúa como un Auditor Académico experto. Evalúa el reparto de horas de los docentes basándote en los siguientes registros: {contexto_lineal}. "
            f"Genera un dictamen en Markdown bajo la estructura:\n"
            f"### Evaluación de Carga Horaria Docente\n"
            f"Escribe un análisis de equilibrio operativo con respecto a las horas académicas asignadas.\n"
            f"**Puntos Críticos:** Genera una lista con dos observaciones enfocadas en evitar el burnout docente."
        )

        try:
            respuesta_raw = consultar_ia(prompt)
            if not respuesta_raw or "Error" in respuesta_raw:
                raise ValueError()
            analisis_html = markdown.markdown(respuesta_raw)
        except Exception:
            resp_local = (
                f"### Evaluación de Carga Horaria Docente (Soporte Local)\n"
                f"La distribución de la carga horaria acumulada indica un despliegue operativo estable en los departamentos analizados. "
                f"Se visualiza la distribución individualizada de asignaciones en las gráficas superiores.\n\n"
                f"**Puntos Críticos:**\n"
                f"1. Monitorear los topes de horas semanales para asegurar la calidad de preparación de las clases.\n"
                f"2. Balancear la asignación de nuevas asignaturas de manera equitativa basándose en la especialidad técnica."
            )
            analisis_html = markdown.markdown(resp_local)

        return self.render_template(
            "reportes/carga_instructores.html",
            datos=reporte_datos,
            analisis_ia=analisis_html,
        )

    # 5. REPORTE: ESTADO DE APROBACIÓN GLOBAL
    @expose("/estado-aprobaciones")
    @has_access
    def estado_aprobaciones(self):
        """Muestra cuántos alumnos están en estado APROBADO o REPROBADO."""
        reporte_datos = (
            db.session.query(
                Inscripcion.estado.label("estado_inscripcion"),
                func.count(Inscripcion.id).label("total"),
            )
            .group_by(Inscripcion.estado)
            .all()
        )

        contexto_lineal = ", ".join(
            [
                f"Estado: {d.estado_inscripcion or 'Indefinido'} (Total: {d.total or 0} alumnos)"
                for d in reporte_datos
            ]
        ) if reporte_datos else "Sin estados registrados"

        prompt = (
            f"Actúa como un Analista de Calidad Educativa. Evalúa los índices de aprobación de la institución: {contexto_lineal}. "
            f"Genera un informe estratégico en Markdown usando el formato:\n"
            f"### Diagnóstico de Índices de Aprobación\n"
            f"Escribe una interpretación del porcentaje global de alumnos aprobados frente a los rezagados.\n"
            f"**Estrategias de Retención:** Plantea 2 mecanismos urgentes de tutoría pedagógica."
        )

        try:
            respuesta_raw = consultar_ia(prompt)
            if not respuesta_raw or "Error" in respuesta_raw:
                raise ValueError()
            analisis_html = markdown.markdown(respuesta_raw)
        except Exception:
            resp_local = (
                f"### Diagnóstico de Índices de Aprobación (Soporte Local)\n"
                f"Los índices consolidados expresan una proporción directa entre el alumnado en estado Aprobado frente a las tasas de rezago. "
                f"Los gráficos circulares superiores ilustran el porcentaje proporcional neto del presente ciclo.\n\n"
                f"**Estrategias de Retención:**\n"
                f"1. Habilitar mentorías guiadas por alumnos de semestres avanzados en favor de estudiantes en estado de riesgo.\n"
                f"2. Programar revisiones de avance de notas en la mitad del ciclo para implementar ajustes pedagógicos a tiempo."
            )
            analisis_html = markdown.markdown(resp_local)

        return self.render_template(
            "reportes/estado_aprobaciones.html",
            datos=reporte_datos,
            analisis_ia=analisis_html,
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
    category_icon="fa-graduation-cap",
)

appbuilder.add_view(
    InstructorModelView,
    "Instructores",
    icon="fa-users",
    category="Academico",
    category_icon="fa-graduation-cap",
)

appbuilder.add_view(
    CursoModelView,
    "Cursos",
    icon="fa-book",
    category="Academico",
    category_icon="fa-graduation-cap",
)

appbuilder.add_view(
    ModuloModelView,
    "Módulos",
    icon="fa-list",
    category="Academico",
    category_icon="fa-graduation-cap",
)

appbuilder.add_view(
    InscripcionModelView,
    "Inscripciones",
    icon="fa-edit",
    category="Academico",
    category_icon="fa-graduation-cap",
)


# MENÚ: Reportes
appbuilder.add_view(
    ReportesView,
    "Panel de Control",
    icon="fa-chart-pie",
    href="/reportes/principal",
    category="Reportes",
    category_icon="fa-file-alt",
)

appbuilder.add_link(
    "Estudiantes por Curso",
    href="/reportes/estudiantes-por-curso",
    icon="fa-graduation-cap",
    category="Reportes",
)

appbuilder.add_link(
    "Rendimiento Académico",
    href="/reportes/rendimiento-cursos",
    icon="fa-trophy",
    category="Reportes",
)

appbuilder.add_link(
    "Carga de Instructores",
    href="/reportes/carga-instructores",
    icon="fa-clock",
    category="Reportes",
)

appbuilder.add_link(
    "Estado de Aprobaciones",
    href="/reportes/estado-aprobaciones",
    icon="fa-check-circle",
    category="Reportes",
)