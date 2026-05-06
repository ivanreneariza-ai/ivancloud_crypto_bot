from .base_agent import BaseAgent
import random

class WhaleAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agente Ballenas (Whale Alert)")

    def analyze(self):
        # TODO: Fase 2 - Conectar a API real de Whale Alert
        # Por ahora simularemos la respuesta para probar el motor
        simulated_scenario = random.choice([
            (1, "Grandes retiros de Binance hacia billeteras frías detectados (Acumulación)."),
            (-1, "Ballenas moviendo 10,000 BTC hacia Coinbase (Posible venta masiva)."),
            (0, "Actividad de ballenas dentro del promedio diario (Neutral).")
        ])
        return simulated_scenario
