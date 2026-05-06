from utils.deepseek_bridge import ask_deepseek

class DeepSeekAgent:
    def __init__(self):
        self.system_prompt = """
        Eres un analista senior de criptomonedas. Tu objetivo es resumir reportes de agentes en una TABLA técnica para Telegram.
        
        REGLAS DE FORMATO:
        1. NO uses las palabras 'Recomendación' ni 'Precise'.
        2. Crea una TABLA en texto monospaciado (usando triple backtick ```) con estas columnas:
           Agente | Tendencia | Acción | Riesgo | Sentimiento
        3. Si un valor no aplica, déjalo en blanco.
        4. Al final, si hay algún hecho muy significativo, agrégalo como un comentario corto.
        5. La respuesta debe empezar directamente con la tabla.
        6. Sé extremadamente breve.
        """

    def analyze_confluence(self, agent_reports):
        prompt = f"{self.system_prompt}\n\nAnaliza estos reportes y genera la tabla:\n{agent_reports}"
        return ask_deepseek(prompt)
