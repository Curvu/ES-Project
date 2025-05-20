from django.db import models
from django.db.models import Q
from django.utils import timezone
import uuid
from .user import User
from ..dynamodb import get_status, update_status

class Service(models.Model):
    class States(models.IntegerChoices):
        SCHEDULE = 1, "Schedule"
        PAYMENT = 2, "Payment"
        REPAIRING = 3, "Repairing"
        DELIVERY = 4, "Delivery"
        FINISHED = 5, "Finished"
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_time = models.DateTimeField()
    type = models.IntegerField(choices=Types.choices)

    @classmethod
    def user_can_book(cls, user, type=None):
        services = cls.objects.filter(user=user, type=type)
        for service in services:
            status = get_status(service.id)
            if not status:
                return False
            status = int(status.get("sstate", 0))
            if status <= cls.States.PAYMENT and status != cls.States.CANCELLED:
                return False
        return True

    @classmethod
    def user_can_pay(cls, service_id, user):
        status = get_status(service_id)
        if not status:
            return False
        state = int(status.get("sstate", 0))
        paid = status.get("paid", False)

        if paid:
            return False

        return (
            state == cls.States.PAYMENT
            and not status.get("paid", False)
            and cls.objects.filter(user=user).exists()
        )

    @classmethod
    def is_time_slot_booked(cls, datetime):
        end_time = datetime + timezone.timedelta(hours=1)
        return cls.objects.filter(
            schedule_time__lt=end_time,
            schedule_time__gt=datetime - timezone.timedelta(hours=1)
        ).exists()

    @classmethod
    def book_service(cls, user, type, datetime):
        if (cls.is_time_slot_booked(datetime) or
            not cls.user_can_book(user, type) or
            datetime < timezone.now()):
            return 0
        service = cls(user=user, type=type, schedule_time=datetime)
        service.save()
        return service

    @classmethod
    def pay_service(cls, service_id, user):
        if not cls.user_can_pay(service_id, user):
            return False

        update_status(service_id, "paid", True)
        return True
