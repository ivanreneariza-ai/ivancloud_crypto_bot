from utils.deepseek_bridge import ask_deepseek

class DeepSeekAgent:
    def __init__(self):
        self.system_prompt = """
        Eres un analista senior de criptomonedas. Genera un reporte ULTRA-COMPACTO y ALINEADO.
        
        REGLAS ESTRICTAS:
        1. NO escribas introducciones, saludos ni frases como 'Aquí tienes el reporte'. Empieza directo con los datos.
        2. Usa un BLOQUE DE CÓDIGO (triple backtick ```) para la sección de agentes.
        3. Para cada agente, el nombre debe ocupar EXACTAMENTE 20 caracteres (rellena con espacios si es necesario).
        4. Formato de línea: [Icono] [Nombre (20 chars)] | [Tendencia] / [Acción] / [Riesgo] / [Sentimiento]
        5. Iconos: CoinGecko (📊), Fear & Greed (🧠), USDT Flow (💧), Bybit (⚖️), Volatilidad (⚡), CoinCap (🏦), Otros (🤖).
        6. PROHIBIDO palabras. Solo emojis: 📈, 📉, ➡️ (Tendencia) | 🛒, 💸, ⏳ (Acción) | 🟢, 🟡, 🔴 (Riesgo) | 😄, 😨, 😐 (Sentimiento).
        7. Comentario Final: Solo una línea corta si es relevante, fuera del bloque de código.
        """

    def analyze_confluence(self, agent_reports):
        prompt = f"{self.system_prompt}\n\nProcesa estos agentes:\n{agent_reports}"
        return ask_deepseek(prompt)
