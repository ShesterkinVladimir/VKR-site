from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class UploadedFile(models.Model):
    file = models.FileField("Файл", upload_to='csv/')
    uploaded_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} {self.uploaded_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Загруженный файл"
        verbose_name_plural = "Загруженные файлы"


@receiver(pre_delete, sender=UploadedFile)
def uploaded_file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete()
