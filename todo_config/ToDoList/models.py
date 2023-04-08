from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from django.db import models
import secrets



COLOR_LIST = [
        ('border-primary', 'Blue'),
        ('border-secondary', 'Gray'),
        ('border-success', 'Green'),
        ('border-danger', 'Red'),
        ('border-warning', 'Yellow'),
        ('border-info', 'Light Blue'),
        ('border-dark', 'Black'),
    ]



class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expiry_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['-expiry_date', ]

    def __str__(self):
        return self.user.username + ' - ' + self.token
        

    @staticmethod
    def token_generator():
        return secrets.token_hex(20)
        

    @classmethod
    def get_or_create_token(cls, user):
        token, created = cls.objects.get_or_create(user=user, defaults={
            'token': cls.token_generator(),
            'expiry_date': timezone.now() + timedelta(hours=1)
        })
        if not created and token.is_expired():
            token.delete()
            token = cls.objects.create(user=user, token=cls.token_generator(),
                                       expiry_date=timezone.now() + timedelta(hours=1)
                                       )
        return token

    def is_expired(self):
        return (self.expiry_date + timedelta(hours=1)) < timezone.now()




class Task(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True,
                             )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=15000,null=True,
                                   blank=True,
                                   )
    complete = models.BooleanField(default=False)
    color = models.CharField(max_length=20, choices=COLOR_LIST,
                              default='blue_bootstrp',
                             )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['updated_at']

    