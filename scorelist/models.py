from django.db import models


# Create your models here.

class ScoreList(models.Model):
    player = models.CharField(max_length=50, verbose_name="玩家名称")
    score = models.IntegerField(default=0, verbose_name='分数')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        db_table = 'scorelist'

    def __str__(self):
        return '%s %s %s' % (self.id, self.player, self.score)
