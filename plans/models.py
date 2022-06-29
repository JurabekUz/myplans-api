from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

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



class Habit(models.Model):
    REPEAT_CHOICES = [
    ('week_days', (
            ('SA', 'saturday'),
            ('MO', 'monday'),
            ('TU', 'tuesday'),
            ('WE', 'wednesday'),
            ('TH', 'thursday'),
            ('FR', 'friday'),
            ('SU', 'sunday')
        )
    ),
    ('x_day_week', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6')
     )
    ),
    ('x_day_month', (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    )),
    ]

    PART_CHOICES = [
        ('anytime', 'anytime'),
        ('morning', 'morning'),
        ('afternoon', 'afternoon'),
        ('evening', 'evening'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit')
    name = models.CharField(max_length=30)
    repeat = MultiSelectField(choices=REPEAT_CHOICES)
    part_day = models.CharField(max_length=9, choices=PART_CHOICES)
    finished = models.BooleanField(default=False)

    def mark_as_finished(self):
        self.finished = True
        self.save()

    def mark_as_unfinished(self):
        self.finished = False
        self.save()




