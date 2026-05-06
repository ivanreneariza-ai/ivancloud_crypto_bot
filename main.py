import time
import config
from agents.whale_agent import WhaleAgent
from agents.sentiment_agent import SentimentAgent
from agents.liquidity_agent import LiquidityAgent
from agents.deepseek_agent import DeepSeekAgent
from utils.notifier import TelegramNotifier

def main():
    print("==================================================")
    print(" INICIANDO CLOUD CRYPTO BOT (Analisis Inteligente)")
    print("==================================================")

    # Inicializar Notificador
    notifier = TelegramNotifier(config.TELEGRAM_TOKEN, config.TELEGRAM_CHAT_ID)

    # Inicializar agentes recolectores
    collectors = [
        WhaleAgent(),
        SentimentAgent(),
        LiquidityAgent()
    ]
    
    # Inicializar Agente Cerebro (DeepSeek)
    brain = DeepSeekAgent()

    total_score = 0
    max_possible_score = len(collectors)
    report_summary = ""

    print("\nConsultando a los agentes del mercado...")
    for agent in collectors:
        score, reason = agent.analyze()
        total_score += score
        line = f"[{agent.name}] Voto: {score:+} -> {reason}"
        print(line.encode('ascii', 'ignore').decode()) # Evitar errores de emoji en consola
        report_summary += f"- {line}\n"

    print("\nInvocando al Analista DeepSeek para la decision final...")
    ai_analysis = brain.analyze_confluence(report_summary)
    print(f"\nAnalisis DeepSeek:\n{ai_analysis.encode('ascii', 'ignore').decode()}")

    # Decision basada en puntos
    if total_score >= 2: 
        decision_text = "COMPRA FUERTE"; emoji = "🟢"
    elif total_score == 1: 
        decision_text = "COMPRA LEVE"; emoji = "🟢"
    elif total_score <= -2: 
        decision_text = "VENTA FUERTE"; emoji = "🔴"
    elif total_score == -1: 
        decision_text = "VENTA LEVE"; emoji = "🔴"
    else: 
        decision_text = "MERCADO NEUTRAL"; emoji = "⚪"

    # Construir reporte OPTIMIZADO para Telegram (Recomendacion ARRIBA)
    telegram_report = f"🚀 *RECOMENDACION:* {emoji} {decision_text}\n\n"
    telegram_report += f"🧠 *IA:* {ai_analysis}\n\n"
    telegram_report += f"📊 *DETALLE:*\n{report_summary}"

    print("\n==================================================")
    print(f" Sugerencia: {decision_text}")
    print("==================================================")

    # Enviar a Telegram
    notifier.send_message(telegram_report)

if __name__ == '__main__':
    main()
