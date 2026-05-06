from .base_agent import BaseAgent
import urllib.request
import json

class LiquidityAgent(BaseAgent):
    def __init__(self):
        super().__init__("USDT Flow")
        self.url = "https://api.coingecko.com/api/v3/coins/tether?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"

    def analyze(self):
        try:
            # Usamos un User-Agent para evitar bloqueos
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                # Obtenemos el cambio en la capitalizacion de mercado en las ultimas 24h
                mkt_cap_change_24h = data['market_data']['market_cap_change_24h']
                mkt_cap_pct_24h = data['market_data']['market_cap_change_percentage_24h']
                
                score = 0
                msg = f"Flujo USDT (24h): {mkt_cap_pct_24h:.2f}% "
                
                # Logica de Liquidez:
                # Si el market cap de USDT crece > 0.1%, es señal de entrada de dinero fuerte
                if mkt_cap_pct_24h > 0.1:
                    score = 1
                    msg += "(Inyección detectada - ALCISTA)"
                elif mkt_cap_pct_24h < -0.1:
                    score = -1
                    msg += "(Retiro detectado - BAJISTA)"
                else:
                    score = 0
                    msg += "(Liquidez Estable)"
                    
                return (score, msg)
                
        except Exception as e:
            return (0, f"Error obteniendo datos de liquidez: {str(e)}")
