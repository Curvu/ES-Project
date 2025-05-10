from django.db import models
from django.db.models import Q
from django.utils import timezone
import uuid

class Users(models.Model):
    username = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Token(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.token} - {self.is_valid}"

class Service(models.Model):
    class States(models.IntegerChoices):
        SCHEDULED = 1, "Scheduled"
        REPAIRING = 2, "Repairing"
        WAITING_FOR_PICKUP = 3, "Waiting for Pickup"
        FINISHED = 4, "Finished"
        CANCELLED = -1, "Cancelled"

    class Types(models.IntegerChoices):
        SCREEN_REPLACEMENT = 1, "Screen Replacement"
        BATTERY_REPLACEMENT = 2, "Battery Replacement"
        SOFTWARE_TROUBLESHOOTING = 3, "Software Troubleshooting"
        DATA_RECOVERY = 4, "Data Recovery"
        VIRUS_REMOVAL = 5, "Virus Removal"

    PRICES = {
        Types.SCREEN_REPLACEMENT: 100,
        Types.BATTERY_REPLACEMENT: 50,
        Types.SOFTWARE_TROUBLESHOOTING: 30,
        Types.DATA_RECOVERY: 80,
        Types.VIRUS_REMOVAL: 40,
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    schedule_time = models.DateTimeField()
    service_type = models.IntegerField(choices=Types.choices)

    @classmethod
    def user_can_book(cls, user, service_type=None):
        # if user doesn't have a booking for the same service type that is not finished
        return not cls.objects.filter(
            user=user,
            service_state__lt=cls.States.FINISHED,
            service_type=service_type,
        ).exists()

    @classmethod
    def get_all_service_prices(cls, user=None):
        return [
            {
                "id": t.value,
                "name": t.label,
                "price": cls.PRICES.get(t.value),
                "can_book": cls.user_can_book(user, t),
            }
            for t in cls.Types
        ]

    @classmethod
    def is_time_slot_booked(cls, datetime):
        end_time = datetime + timezone.timedelta(hours=1)
        return cls.objects.filter(
            Q(schedule_time__lt=end_time) & Q(schedule_time__gte=datetime)
        ).exists()

    @classmethod
    def book_service(cls, user, service_type, datetime):
        if cls.is_time_slot_booked(datetime):
            return 0
        if not cls.user_can_book(user, service_type):
            return -1
        if datetime < timezone.now():
            return -2

        service = cls(
            user=user,
            service_type=service_type,
            schedule_time=datetime,
            service_state=cls.States.SCHEDULED,
        )

        service.save()
        return service

    def to_dict(self):
        return {
            "id": self.id,
            "schedule_time": self.schedule_time,
            "service_type": self.Types(self.service_type).label,
            "service_state": self.service_state,
            "paid": self.paid,
            "delivered": self.delivered,
        }

    #! Mudar isto para o DynamoDB !#

    service_state = models.IntegerField(
        choices=States.choices,
        default=States.SCHEDULED,
    )

    paid = models.BooleanField(default=False) # Can pay if State >= 2
    delivered = models.BooleanField(default=False)
