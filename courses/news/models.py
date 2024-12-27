from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=" Curs nomi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sanasi")

    def __str__(self):
        return self.name



class Lessons(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Mavzu")
    homework = models.TextField(verbose_name="Uyga vazifa")
    deadline = models.DateTimeField(verbose_name="Uyga vazifa muddati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sanasi")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sanasi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kursi")

    def __str__(self):
        return self.name

