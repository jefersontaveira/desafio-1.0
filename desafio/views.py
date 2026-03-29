from django.shortcuts import render, redirect
from .models import RegistroDiario
from datetime import date, timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

@login_required
def dashboard(request):
    periodo = request.GET.get('periodo', 'mes')
    hoje = timezone.localdate()

    # Configuração do Filtro de Data
    if periodo == 'dia':
        filtro = Q(data=hoje)
    elif periodo == 'ano':
        filtro = Q(data__year=hoje.year)
    else:  # mês
        filtro = Q(data__month=hoje.month, data__year=hoje.year)

    usuarios = User.objects.all()
    ranking_data = []

    for user in usuarios:
        registros = RegistroDiario.objects.filter(filtro, usuario=user)

        pontos = sum(reg.total_pontos for reg in registros)

        ranking_data.append({
            'nome': user.username,
            'pontos': round(pontos, 1)
        })

    ranking_data = sorted(ranking_data, key=lambda x: x['pontos'], reverse=True)

    historico = RegistroDiario.objects.filter(filtro).order_by('-data', 'usuario__username')

    return render(request, 'desafio/dashboard.html', {
        'ranking': ranking_data,
        'historico': historico,
        'periodo_atual': periodo
    })


@login_required
def registrar_progresso(request):
    hoje = timezone.localdate()  # Garante o fuso horário correto

    if request.method == "POST":
        # 1. Verifica se o usuário já tem um registro para o dia de hoje
        ja_registrou = RegistroDiario.objects.filter(usuario=request.user, data=hoje).exists()

        if ja_registrou:
            # Avisa na tela que não pode enviar duas vezes (precisaremos colocar o HTML disso depois)
            messages.error(request, 'Você já enviou o seu registro diário. Para alterar entre em contato com o desenvolvedor.')
            return redirect('dashboard')

        # 2. Se não registrou, nós criamos o registro do zero
        RegistroDiario.objects.create(
            usuario=request.user,
            data=hoje,
            academia=request.POST.get('academia') == 'on',
            doce=request.POST.get('doce') == 'on',
            agua=float(request.POST.get('agua', 0)),
            corrida=float(request.POST.get('corrida', 0)),
        )

        messages.success(request, 'Check-in realizado com sucesso!')
        return redirect('dashboard')

    return render(request, 'desafio/form.html')

def api_ranking(request):
    dados = [
        {"nome": "Jeferson", "pontos": 850},
        {"nome": "Thalles", "pontos": 720},
        {"nome": "Mariam", "pontos": 910},
    ]
    return JsonResponse(dados, safe=False)
