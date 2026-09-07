'''
def calculate_analytics(trades):
    total_trades = trades.count()

    if total_trades == 0:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "break_even_trades": 0,
            "total_pnl": 0,
            "win_rate": 0,
        }

    winning_trades = 0
    losing_trades = 0
    break_even_trades = 0
    total_pnl = 0

    for trade in trades:
        pnl = trade.pnl
        total_pnl += pnl

        if pnl > 0:
            winning_trades += 1
        elif pnl < 0:
            losing_trades += 1
        else:
            break_even_trades += 1

    win_rate = (winning_trades / total_trades) * 100

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "break_even_trades": break_even_trades,
        "total_pnl": total_pnl,
        "win_rate": win_rate,
    }
'''


import json
from django.shortcuts import render
from .models import Trade

def calculate_analytics(trades):
    total_trades = trades.count()

    if total_trades == 0:
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "break_even_trades": 0,
            "total_pnl": 0.0,
            "win_rate": 0.0,
            "average_win_trade": 0.0,
            "average_loss_trade": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
        }

    winning_trades = 0
    losing_trades = 0
    break_even_trades = 0
    
    total_pnl = 0.0
    total_gross_profit = 0.0
    total_gross_loss = 0.0

    for trade in trades:
        # Convert Decimal or int to float to ensure safe arithmetic across all operations
        pnl = float(trade.pnl) if trade.pnl is not None else 0.0
        total_pnl += pnl

        if pnl > 0:
            winning_trades += 1
            total_gross_profit += pnl
        elif pnl < 0:
            losing_trades += 1
            total_gross_loss += abs(pnl)
        else:
            break_even_trades += 1

    # Win Rate & Loss Rate
    win_rate = round((winning_trades / total_trades) * 100, 1)
    win_probability = winning_trades / total_trades
    loss_probability = losing_trades / total_trades

    # Average Win and Average Loss
    average_win_trade = round(total_gross_profit / winning_trades, 2) if winning_trades > 0 else 0.0
    average_loss_trade = round(total_gross_loss / losing_trades, 2) if losing_trades > 0 else 0.0

    # Profit Factor: Gross Profit / Gross Loss
    if total_gross_loss > 0:
        profit_factor = round(total_gross_profit / total_gross_loss, 2)
    elif total_gross_profit > 0:
        profit_factor = round(total_gross_profit, 2)  # Infinity/undefined loss scenario
    else:
        profit_factor = 0.0

    # Expectancy: (Win Prob * Avg Win) - (Loss Prob * Avg Loss)
    expectancy = round((win_probability * average_win_trade) - (loss_probability * average_loss_trade), 2)

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "break_even_trades": break_even_trades,
        "total_pnl": round(total_pnl, 2),
        "win_rate": win_rate,
        "average_win_trade": average_win_trade,
        "average_loss_trade": average_loss_trade,
        "profit_factor": profit_factor,
        "expectancy": expectancy,
    }


def analytics_view(request):
    trades = Trade.objects.all().order_by('id')

    analytics = calculate_analytics(trades)

    dates_or_ids = []
    cumulative_pnl = []
    running_total = 0

    for trade in trades:
        running_total += float(trade.pnl)
        dates_or_ids.append(f"Trade #{trade.id}")
        cumulative_pnl.append(running_total)

    context = {
        'analytics': analytics,
        'chart_labels': json.dumps(dates_or_ids),
        'chart_data': json.dumps(cumulative_pnl),
    }

    return render(request, 'analytics.html', context)