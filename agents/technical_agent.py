from .base_agent import BaseAgent
import urllib.request
import json

class TechnicalAgent(BaseAgent):
    def __init__(self, symbol="bitcoin"):
        super().__init__("Agente Tecnico (CoinGecko Real-Time)")
        self.symbol = symbol
        self.url = f"https://api.coingecko.com/api/v3/coins/{self.symbol}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"

    def get_market_data(self):
        """Obtiene precio y variacion real desde CoinGecko"""
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                price = float(data['market_data']['current_price']['usd'])
                change = float(data['market_data']['price_change_percentage_24h'])
                return price, change
        except Exception as e:
            return None, None

    def analyze(self):
        price, change = self.get_market_data()
        if price is None:
            return (0, "Error al obtener datos reales.")
        
        score = 0
        msg = f"BTC: ${price:,.2f} | Var 24h: {change:+.2f}% | "
        
        # Logica basada en volatilidad real
        if change < -3:
            score += 1
            msg += "SOBREVENTA detectada. "
        elif change > 3:
            score -= 1
            msg += "SOBRECOMPRA detectada. "
        else:
            msg += "Precio Estable."
            
        return (score, msg)
