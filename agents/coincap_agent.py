from .base_agent import BaseAgent
import urllib.request
import json

class CoinCapAgent(BaseAgent):
    def __init__(self, symbol="bitcoin"):
        super().__init__("CoinCap")
        self.symbol = symbol
        self.url = f"https://api.coincap.io/v2/assets/{self.symbol}"

    def analyze(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                price = float(data['data']['priceUsd'])
                change = float(data['data']['changePercent24Hr'])
                
                score = 0
                msg = f"BTC: ${price:,.2f} | Var: {change:+.2f}% | "
                
                if change < -3:
                    score = 1
                    msg += "Señal de Rebote"
                elif change > 3:
                    score = -1
                    msg += "Señal de Retroceso"
                else:
                    msg += "Consolidación"
                    
                return (score, msg)
                
        except Exception as e:
            return (0, f"Error en CoinCap: {str(e)}")
