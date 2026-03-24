from .models import RegistroDiario
from django.db.models import Sum


class PontuacaoService:
    @staticmethod
    def calcular_pontos(registro):
        # Pesos iguais: Meta batida = 100 pontos
        pts_academia = 100 if registro.academia else 0
        pts_doce = 100 if not registro.doce else 0
        pts_agua = min(100, (registro.agua / 3.0) * 100)
        # 100km/mês = ~3.33km/dia. 1km = 30 pontos (3000 pts/mês)
        pts_corrida = registro.corrida * 30

        return round(pts_academia + pts_doce + pts_agua + pts_corrida, 2)

    @classmethod
    def get_ranking_mensal(cls, mes, ano):
        registros = RegistroDiario.objects.filter(data__month=mes, data__year=ano)
        # Aqui você pode iterar e criar um dicionário de ranking para o Chart.js
        # ... lógica de agregação ...
        return ranking