from django.db import models
from django.contrib.auth.models import User

class Trade(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='trades'
)

    BUY = 'buy'
    SELL = 'sell'
    SIDE_CHOICES = [(BUY , 'buy'), (SELL , 'sell')]


    entry_symbol = models.CharField(max_length=20)
    entry = models.DecimalField(max_digits=15, decimal_places=2)
    exit = models.DecimalField(max_digits=15, decimal_places=2)
    entry_side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    pnl = models.DecimalField(max_digits=15, decimal_places=2)

    # method to calculate the pnl
    def calculate_pnl(self):
        side = self.entry_side.lower() if self.entry_side else ''
        if side == self.BUY:
            return (self.exit - self.entry) * self.quantity
        elif side == self.SELL:
            return (self.entry - self.exit) * self.quantity
        return 0
    
    def save(self, *args, **kwargs):
        self.pnl = self.calculate_pnl()
        super().save(*args, **kwargs)