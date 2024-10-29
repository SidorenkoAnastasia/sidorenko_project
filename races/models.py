from django.db import models
from django.contrib.auth.models import User

class Race(models.Model):
    # Модель гонки, которая определяет основные поля для гонок, инфу о названии, дате и т.д.
    name = models.CharField(max_length=100)
    date = models.DateField()
    path = models.TextField()
    organizer = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.name

class Participant(models.Model):
    # Модель участника гонки, представляющая участников,
    # которые зарегистрированы в конкретной гонке.
    name = models.CharField(max_length=100)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

class CommentRace(models.Model):
    # Позволяет пользователям оставлять текстовые комментарии к гонкам.
    race = models.ForeignKey('Race', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.text[:20]}...'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    # Связываем комментарий с пользователем ^^^
    content = models.TextField() 
    # Содержимое комментария ^^^
    created_at = models.DateTimeField(auto_now_add=True)  
    # Дата и время создания комментария ^^^

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"

class RaceRegistration(models.Model):
    # Содержит информацию о том, какой пользователь зарегистрировался на какую гонку.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Ссылка на модель User, представляющая участника, который зарегистрировался на гонку.
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    # Ссылка на модель Race, представляющая гонку, на которую зарегистрировался пользователь.
    def __str__(self):
        return f"{self.user.username} registered for {self.race.name}"