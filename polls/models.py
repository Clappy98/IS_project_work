from django.db import models

# Create your models here.
class User(models.Model):
    pass    # Django creates ad autoincrementing ID field as pk

class Question(models.Model):
    text = models.TextField(primary_key=True)
    is_negative = models.BooleanField()

class Attribute(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class Performance(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    year = models.IntegerField()
    duration = models.IntegerField()

class Background(models.Model):
    type = models.CharField(max_length=20)

class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class QuestionCategory(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)

    value = models.IntegerField()

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)

class PerformanceCharacteristic(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    value = models.IntegerField()