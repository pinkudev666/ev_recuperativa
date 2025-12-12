import os
from dotenv import load_dotenv
import requests
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import WeatherSearch
from .serializers import WeatherSearchSerializer

# 1. VISTA DEL BUSCADOR (MODIFICADA: YA NO GUARDA AUTOMÁTICAMENTE)
class WeatherView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        # Ya no mandamos historial aquí, porque eso va en la otra página
        return Response({})

    def post(self, request):
        city = request.data.get('localidad')
        
        # --- CARGAR LA CLAVE SECRETA ---
        load_dotenv() # Carga el archivo .env
        api_key = os.getenv('WEATHER_API_KEY') # Lee la variable
        
        # Validación de seguridad (opcional pero recomendada)
        if not api_key:
            return Response({'error': 'Falta la API Key en el servidor'})  

        # --- LLAMADA A LA API ---
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no&alerts=no&lang=es"
        
        try:
            response = requests.get(url)
            data_json = response.json()

            if 'error' in data_json:
                return Response({'error': 'Ciudad no encontrada'})

            # --- EXTRAER DATOS ---
            location = data_json['location']
            forecast_day = data_json['forecast']['forecastday'][0]['day']

            # Preparamos los datos SOLAMENTE para mostrarlos en el HTML
            result_data = {
                'localidad': location['name'],
                'latitud': location['lat'],
                'longitud': location['lon'],
                'temp_max': forecast_day['maxtemp_c'],
                'temp_min': forecast_day['mintemp_c'],
                'lluvia': forecast_day['daily_chance_of_rain']
            }

            # --- AQUÍ ESTABA EL ERROR ---
            # BORRÉ el bloque "serializer.save()" que tenías aquí.
            # Ahora solo devolvemos los datos al usuario sin tocar la Base de Datos.
            
            return Response({'result': result_data})

        except Exception as e:
            return Response({'error': f"Error de conexión: {str(e)}"})


# 2. VISTA PARA GUARDAR (ESTA ES LA ÚNICA QUE DEBE GUARDAR)
def guardar_clima(request):
    if request.method == 'POST':
        data = {
            'localidad': request.POST.get('localidad'),
            'latitud': request.POST.get('latitud'),
            'longitud': request.POST.get('longitud'),
            'temp_max': request.POST.get('temp_max'),
            'temp_min': request.POST.get('temp_min'),
            'lluvia': request.POST.get('lluvia')
        }
        
        # AQUÍ SÍ GUARDAMOS
        serializer = WeatherSearchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
        return redirect('lista_guardados')


# 3. VISTA DE LA PÁGINA APARTE (Historial)
def lista_guardados(request):
    history = WeatherSearch.objects.all().order_by('-fecha_consulta')
    return render(request, 'guardados.html', {'history': history})