# contenido de app/ia_service.py

def consultar_ia(prompt):
    """
    Función puente para interactuar con el modelo de Inteligencia Artificial.
    Por ahora devuelve una respuesta simulada para que tu app funcione.
    """
    print(f"[IA Service] Procesando el prompt: {prompt}")
    
    # Aquí irá tu lógica real con requests o el SDK correspondiente.
    # Por ahora simulamos una respuesta exitosa en dos líneas:
    return (
        "La institución muestra un crecimiento sostenido con un óptimo balance entre el "
        "volumen de matrículas y la distribución de la carga horaria de los instructores."
    )