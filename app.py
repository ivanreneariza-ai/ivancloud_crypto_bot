import os
from flask import Flask
from main import main as run_trading_bot

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

@app.route('/run-bot')
def trigger_bot():
    print("Triggering bot execution...")
    try:
        run_trading_bot()
        return "Bot execution finished successfully", 200
    except Exception as e:
        print(f"Error executing bot: {e}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Cloud Run usa el puerto definido en la variable de entorno PORT, por defecto 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
