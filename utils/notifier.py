import urllib.request
import urllib.parse
import urllib.error

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.enabled = True if token and "TU_TOKEN" not in token else False

    def send_message(self, text):
        if not self.enabled:
            print("[Telegram] Notificaciones desactivadas.")
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            params = {
                'chat_id': self.chat_id,
                'text': text
            }
            data = urllib.parse.urlencode(params).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req)
            print("[Telegram] Notificacion enviada con exito.")
        except urllib.error.HTTPError as e:
            # Esto nos dira la razon exacta del error 400
            error_msg = e.read().decode()
            print(f"[Telegram] Error HTTP {e.code}: {error_msg}")
        except Exception as e:
            print(f"[Telegram] Error inesperado: {e}")
