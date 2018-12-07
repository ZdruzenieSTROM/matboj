from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

class Participant(models.Model):
    name = models.CharField(max_length=200)

    competition = models.ForeignKey('competition.Competition', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

class Match(models.Model):
    class Meta:
        verbose_name_plural = 'matches'

    competition = models.ForeignKey('competition.Competition', on_delete=models.CASCADE)

    winner = models.ForeignKey(
        'competition.Participant',
        on_delete=models.CASCADE,
        related_name='winner'
    )

    loser = models.ForeignKey(
        'competition.Participant',
        on_delete=models.CASCADE,
        related_name='loser'
    )

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Víťaz: {}, Porazený: {} @ {}".format(self.winner, self.loser, self.time)
