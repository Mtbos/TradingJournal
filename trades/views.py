from django.shortcuts import render, redirect, get_object_or_404
from .forms import TradeForm
from .models import Trade
from .services import calculate_analytics
from django.contrib.auth.decorators import login_required



@login_required
def add_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            # Create the model instance without saving to DB yet
            trade = form.save(commit=False)
            # Assign the current logged-in user
            trade.user = request.user
            # Save to database
            trade.save()
            return redirect('trade_list')
    else:
        form = TradeForm()
    
    return render(request, "trades/add_trade.html", {"form": form})


@login_required
def trade_list(request):
    trades = Trade.objects.filter(user=request.user).order_by('id')

    # Adding the filtering method so that user can filter the trades
    symbol = request.GET.get('symbol', '').strip()
    side = request.GET.get('side', '').strip().lower()

    if symbol:
        trades = trades.filter(entry_symbol__icontains=symbol)

    if side:
        trades = trades.filter(entry_side__iexact=side)

    context = {
        'trades': trades,
        'symbol': symbol,
        'side': side,
    }

    return render(request, 'trades/trade_list.html', context)


@login_required
def update_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)

    if request.method == 'POST':
        form = TradeForm(request.POST, instance=trade)
        if form.is_valid():
            form.save()
            return redirect('trade_list')
    else:
        form = TradeForm(instance=trade)

    return render(request, "trades/update_trade.html", {"form": form, "trade": trade})


@login_required
def delete_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    
    if request.method == 'POST':
        trade.delete()
        return redirect('trade_list')
    
    return render(request, "trades/delete_trade_confirm.html", {"trade": trade})


@login_required
def analytics(request):
    # Filter trades specifically for the authenticated user
    trades = Trade.objects.filter(user=request.user)

    data = calculate_analytics(trades)

    return render(
        request,
        "trades/analytics.html",
        {"analytics": data}
    )