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
        PESO_BASE = 10
        PTS_KM_NORMAL = 3  # 3.33km/dia = ~10 pontos
        PTS_KM_EXTRA = 1  # Bônus reduzido após bater 100km no mês

        pts_total = 0
        pts_total += min(PESO_BASE, (self.agua / 3.0) * PESO_BASE)
        if not self.doce:
            pts_total += PESO_BASE
        if not self.pk:
            return round(pts_total + (self.corrida * PTS_KM_NORMAL) + (PESO_BASE if self.academia else 0), 2)
        if self.academia:
            semana_atual = self.data.isocalendar()[1]
            treinos_antes = RegistroDiario.objects.filter(
                usuario=self.usuario,
                data__year=self.data.year,
                data__week=semana_atual,
                data__lt=self.data,
                academia=True
            ).count()

            if treinos_antes < 6:
                pts_total += PESO_BASE
        if self.corrida > 0:
            km_acumulado_antes = RegistroDiario.objects.filter(
                usuario=self.usuario,
                data__year=self.data.year,
                data__month=self.data.month,
                data__lt=self.data
            ).aggregate(models.Sum('corrida'))['corrida__sum'] or 0.0

            km_hoje = self.corrida
            km_total_com_hoje = km_acumulado_antes + km_hoje

            # Verifica se está no limite normal ou se já é extra
            if km_acumulado_antes >= 100:
                pts_total += (km_hoje * PTS_KM_EXTRA)
            elif km_total_com_hoje > 100:
                km_normal = 100 - km_acumulado_antes
                km_extra = km_total_com_hoje - 100
                pts_total += (km_normal * PTS_KM_NORMAL) + (km_extra * PTS_KM_EXTRA)
            else:
                pts_total += (km_hoje * PTS_KM_NORMAL)

        return round(pts_total, 2)