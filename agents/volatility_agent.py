from .base_agent import BaseAgent
import urllib.request
import json

class VolatilityAgent(BaseAgent):
    def __init__(self, symbol="bitcoin"):
        super().__init__("Volatilidad")
        self.symbol = symbol
        self.url = f"https://api.coingecko.com/api/v3/coins/{self.symbol}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"

    def analyze(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                # Obtenemos High y Low de 24h
                high_24h = float(data['market_data']['high_24h']['usd'])
                low_24h = float(data['market_data']['low_24h']['usd'])
                current_price = float(data['market_data']['current_price']['usd'])
                
                # Calculamos el rango porcentual (Volatilidad relativa)
                volatility_range = ((high_24h - low_24h) / current_price) * 100
                
                score = 0
                msg = f"Rango 24h: {volatility_range:.2f}% | "
                
                # Logica de Volatilidad:
                # < 2% : Mercado muy quieto (Compresion, posible explosion proxima)
                # > 5% : Mercado muy volatil (Riesgo alto)
                if volatility_range < 2:
                    score = 0 # Neutral pero aviso de compresion
                    msg += "Baja Volatilidad (Compresión)"
                elif volatility_range > 5:
                    score = -1 # Riesgo alto por sacudidas
                    msg += "Alta Volatilidad (Riesgo)"
                else:
                    score = 0
                    msg += "Volatilidad Normal"
                    
                return (score, msg)
                
        except Exception as e:
            return (0, f"Error en Volatilidad: {str(e)}")
