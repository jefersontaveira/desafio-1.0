from django.contrib import admin
from .models import RegistroDiario


@admin.register(RegistroDiario)
class RegistroDiarioAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na listagem
    list_display = ('usuario', 'data', 'academia', 'doce', 'agua', 'corrida', 'get_pontos')

    # Filtros laterais para facilitar a busca
    list_filter = ('data', 'usuario', 'academia', 'doce')

    # Campo de busca por nome de usuário
    search_fields = ('usuario__username',)

    # Ordenação padrão (mais recente primeiro)
    ordering = ('-data',)

    # Função para exibir os pontos calculados no Admin
    def get_pontos(self, obj):
        # Aqui chamamos a propriedade que calcula os pontos no seu Model
        return f"{obj.total_pontos} pts"

    get_pontos.short_description = 'Pontuação Total'