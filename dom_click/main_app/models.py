from django.db import models

from auth_app.models import Client


class Application(models.Model):
    """Модель Заявок"""

    class Meta:
        ordering = ['-created']

    TITLE_CHOICES = (
        ('ремонт', 'ремонт'),
        ('обслуживание', 'обслуживание'),
        ('консультация', 'консультация'),
    )

    STATUS_CHOICES = (
        ('открыта', 'открыта'),
        ('в работе', 'в работе'),
        ('закрыта', 'закрыта'),
    )

    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE,
        db_index=True, verbose_name='клиент', related_name='user')
    worker = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, blank=True, db_index=True,
        null=True, verbose_name='сотрудник', related_name='user_w')
    title = models.CharField(
        max_length=16, choices=TITLE_CHOICES, verbose_name='тип заявки')
    content = models.CharField(max_length=256, verbose_name='описание заявки')
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, verbose_name='статус заявки')
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='активна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создана')
    edited = models.DateTimeField(auto_now=True, verbose_name='изменена')

    def __str__(self):
        return str(self.title)
