from .base_agent import BaseAgent
import urllib.request
import json

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agente de Sentimiento (Fear & Greed API)")

    def analyze(self):
        # API REAL Y GRATUITA
        try:
            req = urllib.request.Request('https://api.alternative.me/fng/?limit=1', headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            
            fng_value = int(data['data'][0]['value'])
            fng_classification = data['data'][0]['value_classification']

            # Lógica: "Sé codicioso cuando otros tienen miedo"
            if fng_value <= 35:
                return (1, f"Miedo Extremo ({fng_value}). Excelente oportunidad de compra (pánico del mercado).")
            elif fng_value >= 75:
                return (-1, f"Codicia Extrema ({fng_value}). Mercado sobrecomprado, prepararse para posible caída.")
            else:
                return (0, f"Mercado Neutral ({fng_value}). Sentimiento: {fng_classification}.")
        except Exception as e:
            return (0, f"Error al conectar con la API de sentimiento: {str(e)}")
