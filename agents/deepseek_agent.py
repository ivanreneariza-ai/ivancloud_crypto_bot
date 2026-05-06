from utils.deepseek_bridge import ask_deepseek

class DeepSeekAgent:
    def __init__(self):
        self.system_prompt = """
        Eres un analista senior de criptomonedas. Genera un reporte VISUAL y DINÁMICO.
        
        REGLAS PARA CADA AGENTE RECIBIDO:
        1. Formato: [Icono] [Nombre del Agente] | [Tendencia] / [Acción] / [Riesgo] / [Sentimiento]
        2. Usa estos iconos según el nombre:
           - Si es Técnico: 📊
           - Si es Sentimiento: 🧠
           - Si es Liquidez: 💧
           - Para otros: 🤖
        3. PROHIBIDO usar palabras en los valores. Usa EXCLUSIVAMENTE estos emojis:
           - Tendencia: 📈, 📉, ➡️
           - Acción: 🛒, 💸, ⏳
           - Riesgo: 🟢, 🟡, 🔴
           - Sentimiento: 😄, 😨, 😐
        4. Si un valor no aplica, deja el espacio vacío entre slashes / /.
        5. Comentario Final: Solo si es extremadamente relevante.
        6. NO uses las palabras 'Recomendación' ni 'Precise'.
        """

    def analyze_confluence(self, agent_reports):
        # Ahora el prompt le pide a la IA que procese TODOS los reportes que reciba
        prompt = f"{self.system_prompt}\n\nProcesa todos estos agentes uno por uno:\n{agent_reports}"
        return ask_deepseek(prompt)
