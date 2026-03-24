from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class RegistroDiario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros')
    data = models.DateField()
    academia = models.BooleanField(default=False)
    doce = models.BooleanField(default=False) # False = Cumpriu a meta (Não comeu)
    agua = models.FloatField(default=0) # Em litros
    corrida = models.FloatField(default=0) # Em KM

    class Meta:
        unique_together = ('usuario', 'data')
        ordering = ['-data']

    def __str__(self):
        return f"{self.usuario.username} - {self.data}"

    @property
    def total_pontos(self):
        # Normalizando tudo para base 100
        pts_academia = 100 if self.academia else 0
        pts_doce = 100 if not self.doce else 0  # Ganha ponto se NÃO comeu doce
        pts_agua = min(100, (self.agua / 3) * 100)

        # Corrida: 100km/mês = 3.33km/dia para ganhar 100 pontos diários
        # Logo, cada 1km vale 30 pontos.
        pts_corrida = self.corrida * 30

        return round(pts_academia + pts_doce + pts_agua + pts_corrida, 2)