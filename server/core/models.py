from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=120)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=180)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.CharField(max_length=120)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, default='neutral')

    def __str__(self):
        return f'Review by {self.reviewer} for {self.dealer.name}'
