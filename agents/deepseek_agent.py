from .base_agent import BaseAgent
from utils.deepseek_bridge import load_env, ask_deepseek

class DeepSeekAgent(BaseAgent):
    def __init__(self):
        super().__init__("Analista Inteligente (DeepSeek)")

    def analyze_confluence(self, all_reports):
        """
        Este agente recibe el reporte de los demás y genera una conclusión de alto nivel.
        """
        prompt = f"""Analiza esta confluencia de datos cripto y dame un resumen ejecutivo MUY CORTO (máximo 200 caracteres):
{all_reports}

Estructura: 
1. Tendencia. 2. Acción sugerida. 3. Riesgo.
Sé ultra-directo y profesional."""
        
        try:
            load_env() # Carga la API KEY desde el .env que copiamos a la carpeta utils
            response = ask_deepseek(prompt)
            return response
        except Exception as e:
            return f"Error al consultar al analista DeepSeek: {str(e)}"
