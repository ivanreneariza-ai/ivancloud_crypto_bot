from .base_agent import BaseAgent
import urllib.request
import json

class TechnicalAgent(BaseAgent):
    def __init__(self, symbol="BTCUSDT"):
        super().__init__("Agente Tecnico (Binance Real-Time)")
        self.symbol = symbol
        self.base_url = "https://api.binance.com/api/v3/klines"

    def get_market_data(self):
        """Obtiene las ultimas 100 velas de 1 hora de Binance"""
        url = f"{self.base_url}?symbol={self.symbol}&interval=1h&limit=100"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                closes = [float(candle[4]) for candle in data]
                return closes
        except Exception as e:
            return None

    def calculate_rsi(self, prices, periods=14):
        if len(prices) < periods + 1:
            return 50
        deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        seed = deltas[:periods]
        up = sum([d for d in seed if d >= 0]) / periods
        down = -sum([d for d in seed if d < 0]) / periods
        rs = up / down if down != 0 else 0
        rsi = 100. - 100. / (1. + rs)
        for d in deltas[periods:]:
            gain = d if d > 0 else 0
            loss = -d if d < 0 else 0
            up = (up * (periods - 1) + gain) / periods
            down = (down * (periods - 1) + loss) / periods
            rs = up / down if down != 0 else 0
            rsi = 100. - 100. / (1. + rs)
        return rsi

    def analyze(self):
        prices = self.get_market_data()
        if not prices:
            return (0, "Error al obtener datos reales de Binance.")
        
        current_price = prices[-1]
        rsi = self.calculate_rsi(prices)
        ema_200_approx = sum(prices) / len(prices)
        
        score = 0
        msg = f"BTC: ${current_price:,.0f} | RSI: {rsi:.0f} | "
        
        if rsi < 30:
            score += 1
            msg += "SOBREVENTA (Oportunidad). "
        elif rsi > 70:
            score -= 1
            msg += "SOBRECOMPRA (Cuidado). "
            
        if current_price > ema_200_approx:
            score += 1
            msg += "Tendencia Alcista (Bullish)."
        else:
            score -= 1
            msg += "Tendencia Bajista (Bearish)."
            
        return (score, msg)
