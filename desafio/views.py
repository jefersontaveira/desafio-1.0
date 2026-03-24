from django.shortcuts import render, redirect
from .models import RegistroDiario
from datetime import date, timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    periodo = request.GET.get('periodo', 'mes')
    hoje = date.today()

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

        stats = registros.aggregate(
            total_km=Sum('corrida'),
            total_agua=Sum('agua'),
            total_acad=Count('id', filter=Q(academia=True)),
            dias_sem_doce=Count('id', filter=Q(doce=False))
        )

        km = stats['total_km'] or 0
        agua = stats['total_agua'] or 0
        acad = stats['total_acad'] or 0
        doces_meta = stats['dias_sem_doce'] or 0

        pontos = (acad * 100) + (doces_meta * 100) + (agua * 33.33) + (km * 30)

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
    if request.method == "POST":
        RegistroDiario.objects.update_or_create(
            usuario=request.user,
            data=date.today(),
            defaults={
                'academia': request.POST.get('academia') == 'on',
                'doce': request.POST.get('doce') == 'on',
                'agua': float(request.POST.get('agua', 0)),
                'corrida': float(request.POST.get('corrida', 0)),
            }
        )
        return redirect('dashboard')
    return render(request, 'desafio/form.html')

def api_ranking(request):
    dados = [
        {"nome": "Jeferson", "pontos": 850},
        {"nome": "Thalles", "pontos": 720},
        {"nome": "Mariam", "pontos": 910},
    ]
    return JsonResponse(dados, safe=False)
