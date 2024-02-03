from django.db.models import Count
from django.db.models.functions import TruncHour

from Aplication.models import Historial

def obtener_datos_para_grafico():
    # Agrupa los datos por tipo y hora (en horas)
    datos = Historial.objects.annotate(
        hora=TruncHour('fecha_movimiento')
    ).values('hora', 'tipo').annotate(
        cantidad=Count('id')
    )

    # Estructura de datos para el gráfico
    historial_series = {
        'labels': [],
        'datasets': []
    }

    tipos_movimientos = Historial.objects.values_list('tipo', flat=True).distinct()

    for tipo in tipos_movimientos:
        datos_tipo = datos.filter(tipo=tipo)

        dataset = {
            'label': tipo,
            'data': [],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',  # Ajusta según tus preferencias
            'borderColor': 'rgba(75, 192, 192, 1)',  # Ajusta según tus preferencias
            'borderWidth': 1,
        }

        for hora in datos_tipo:
            # Formatear la fecha correctamente
            fecha_formateada = hora['hora'].strftime("%Y-%m-%d %H:%M:%S")
            historial_series['labels'].append(fecha_formateada)
            dataset['data'].append(hora['cantidad'])

        historial_series['datasets'].append(dataset)

    return historial_series
