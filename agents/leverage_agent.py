from .base_agent import BaseAgent
import urllib.request
import json

class LeverageAgent(BaseAgent):
    def __init__(self, symbol="BTCUSDT"):
        super().__init__("Bybit (Leverage)")
        self.symbol = symbol
        # Usamos Bybit para obtener el Funding Rate en tiempo real
        self.url = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={self.symbol}"

    def get_funding_rate(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                # El funding rate esta en data['result']['list'][0]['fundingRate']
                rate = float(data['result']['list'][0]['fundingRate'])
                return rate
        except Exception as e:
            print(f"Error en Bybit: {e}")
            return None

    def analyze(self):
        rate = self.get_funding_rate()
        if rate is None:
            return (0, "Error al obtener datos de apalancamiento.")
        
        score = 0
        rate_pct = rate * 100
        msg = f"Funding: {rate_pct:.4f}% | "
        
        # Logica de Apalancamiento:
        # > 0.01% : Mercado sobrecalentado (riesgo de caída)
        # < 0.00% : Mercado pesimista (oportunidad de rebote)
        if rate_pct > 0.01:
            score = -1
            msg += "Apalancamiento ALTO (Riesgo de Long Squeeze)"
        elif rate_pct < 0:
            score = 1
            msg += "Shorts dominando (Posible rebote alcista)"
        else:
            score = 0
            msg += "Apalancamiento Saludable"
            
        return (score, msg)
