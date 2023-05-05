from datetime import datetime, time, date
from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Activity(TimeStampedUUIDModel):
    class Priority(models.TextChoices):
        LOW = "low", _("low")
        MEDIUM = "medium", _("medium")
        HIGH = "high", _("high")

    tanggal = models.DateField(verbose_name=_("tanggal"), default=date.today())
    waktu = models.TimeField(
        verbose_name=_("waktu"), default=datetime.now().strftime("%H:%M:%S")
    )
    judul = models.CharField(verbose_name=_("judul"), max_length=225)
    deskripsi = models.TextField(verbose_name=_("deskripsi"))
    prioritas = models.CharField(
        verbose_name=_("priority"),
        choices=Priority.choices,
        default=Priority.MEDIUM,
        max_length=15,
    )
    # creator = models.ForeignKey(
    #     "accounts.User",
    #     verbose_name=_("creator"),
    #     related_name="creator_activity",
    #     on_delete=models.CASCADE,
    # )

    class labels(models.TextChoices):
        PERSONAL = "personal", _("personal")
        GROUP = "group", _("group")

    label = models.CharField(
        verbose_name=_("label"),
        choices=labels.choices,
        default=labels.PERSONAL,
        max_length=15,
    )

    asign = models.TextField(
        verbose_name=_("asign"), max_length=225, default=None, blank=True, null=True
    )

    class Meta:
        verbose_name = "activity"
        verbose_name_plural = "activities"
        db_table = "activities_activity"

    def __str__(self):
        return self.judul
