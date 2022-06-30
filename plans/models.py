from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.core.exceptions import ValidationError

User = get_user_model()
class Plan(models.Model):

    class PlanStatus(models.TextChoices):
        PENDING = 'pending', _('pending')
        DOING = 'doing', _('doing')
        RETURNED = 'returned', _('returned')
        DONE = 'done', _('done')


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plan')
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=PlanStatus.choices, default=PlanStatus.PENDING)

    def mark_as_done(self):
        self.status = self.PlanStatus.DONE
        self.save()

    def mark_as_pending(self):
        self.status = self.PlanStatus.PENDING
        self.save()

    def mark_as_doing(self):
        self.status = self.PlanStatus.DOING
        self.save()

    def mark_as_returned(self):
        self.status = self.PlanStatus.RETURNED
        self.save()

WEEK_DAYS = [
        ('SA', 'saturday'),
        ('MO', 'monday'),
        ('TU', 'tuesday'),
        ('WE', 'wednesday'),
        ('TH', 'thursday'),
        ('FR', 'friday'),
        ('SU', 'sunday')
]

X_DAY_WEEK = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6')
] 


PART_CHOICES = [
    ('anytime', 'anytime'),
    ('morning', 'morning'),
    ('afternoon', 'afternoon'),
    ('evening', 'evening'),
]
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit')
    name = models.CharField(max_length=30)
    repeat_day = MultiSelectField(choices=WEEK_DAYS, blank=True, null=True)
    repeat_week = models.IntegerField(choices=X_DAY_WEEK, blank=True, null=True)
    repeat_month = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], blank=True, null=True)
    part_day = models.CharField(max_length=9, choices=PART_CHOICES)
    finished = models.BooleanField(default=False)

    def clean(self) -> None:

        if self.repeat_day:
            if  self.repeat_month or self.repeat_week:
                raise ValidationError(
                {'repeat_day': "Xatolik!, repeat_day, repeat_week va repeat_month lardan faqat biri tanlansin"})

        if self.repeat_month:
            if  self.repeat_day or self.repeat_week:
                raise ValidationError(
                {'repeat_month': "Xatolik!, repeat_day, repeat_week va repeat_month lardan faqat biri tanlansin"})

        if self.repeat_week:
            if  self.repeat_month or self.repeat_day:
                raise ValidationError(
                {'repeat_week': "Xatolik!, repeat_day, repeat_week va repeat_month lardan faqat biri tanlansin"})

        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    ''' 
    Even though the admin site invokes the method. The clean method is not invoked 
    on save() or create() by default. So the best practice is to override the save method of 
    the model and invoke the full_clean() method that under the hood calls clean and other validation hooks.
    '''

    def mark_as_finished(self):
        self.finished = True
        self.save()

    def mark_as_unfinished(self):
        self.finished = False
        self.save()




