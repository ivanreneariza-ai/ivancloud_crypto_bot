import time
import os
import json
try:
    import config
except ImportError:
    config = None
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.liquidity_agent import LiquidityAgent
from agents.leverage_agent import LeverageAgent
from agents.deepseek_agent import DeepSeekAgent
from utils.notifier import TelegramNotifier

def main():
    print("==================================================")
    print(" INICIANDO CLOUD CRYPTO BOT (Analisis Inteligente)")
    print("==================================================")

    # Inicializar Notificador (Prioridad: Config local -> Env Var)
    token = getattr(config, 'TELEGRAM_TOKEN', os.environ.get('TELEGRAM_TOKEN'))
    chat_id = getattr(config, 'TELEGRAM_CHAT_ID', os.environ.get('TELEGRAM_CHAT_ID'))
    notifier = TelegramNotifier(token, chat_id)

    # Inicializar agentes recolectores
    collectors = [
        TechnicalAgent(),
        SentimentAgent(),
        LiquidityAgent(),
        LeverageAgent()
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

    # --- LOGICA DE MEMORIA Y VALIDACION ---
    memory_file = "memory.json"
    last_data = {}
    if os.path.exists(memory_file):
        try:
            with open(memory_file, 'r') as f:
                last_data = json.load(f)
        except: pass

    # Extraer precio preciso del reporte del Agente Tecnico
    import re
    current_price = 0
    match = re.search(r'\$(\d+,?\d*\.?\d*)', report_summary)
    if match:
        current_price = float(match.group(1).replace(',', ''))

    validation_msg = ""
    if last_data and current_price > 0:
        last_price = last_data.get('price', 0)
        last_rec = last_data.get('recommendation', 'N/A')
        
        if last_price > 0:
            diff_pct = ((current_price - last_price) / last_price) * 100
            trend_emoji = "🟢" if diff_pct > 0 else "🔴"
            
            success = False
            if "COMPRA" in last_rec and diff_pct > 0: success = True
            elif "VENTA" in last_rec and diff_pct < 0: success = True
            elif "NEUTRAL" in last_rec and abs(diff_pct) < 0.05: success = True
            
            status_emoji = "✅" if success else "❌"
            validation_msg = f"🎯 {last_price:,.0f} | {trend_emoji} {abs(diff_pct):.4f}% | {current_price:,.0f} {status_emoji}\n"

    # Guardar memoria para la proxima ejecucion
    with open(memory_file, 'w') as f:
        json.dump({'price': current_price, 'recommendation': decision_text}, f)

    # Construir reporte FINAL (VISUAL DASHBOARD)
    telegram_report = f"🚀 {emoji} {decision_text}\n"
    telegram_report += validation_msg
    telegram_report += f"{ai_analysis}"

    print("\n==================================================")
    print(f" Sugerencia: {decision_text}")
    print("==================================================")

    # Enviar a Telegram
    notifier.send_message(telegram_report)

if __name__ == '__main__':
    main()
