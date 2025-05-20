from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from api.models import Service
from api.dynamodb import get_status

class RegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="Username for the new user")
    images = serializers.ListField(
        child=serializers.CharField(help_text="Base64-encoded image string"),
        help_text="List of base64-encoded images of the user's face"
    )


class LoginRequestSerializer(serializers.Serializer):
    image = serializers.CharField(help_text="Base64-encoded image of the user's face")


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_admin = serializers.BooleanField()


class SignResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()


class ServiceTypeSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(help_text="ID of the service type")
    name = serializers.SerializerMethodField(help_text="Label of the service type")
    price = serializers.SerializerMethodField()
    can_book = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.value

    def get_name(self, obj):
        return obj.label

    def get_price(self, obj):
        return Service.PRICES.get(obj.value, 0)

    def get_can_book(self, obj):
        user = self.context.get('user')
        return Service.user_can_book(user, obj.value) if user else False


class ServiceSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()
    can_pay = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'schedule_time', 'type', 'state', 'paid', 'can_pay']

    def get_state(self, obj):
        status = get_status(obj.id)
        return int(status.get("sstate")) if status else None

    def get_paid(self, obj):
        status = get_status(obj.id)
        return status.get("paid") if status else False

    def get_can_pay(self, obj):
        user = self.context.get('user')
        return Service.user_can_pay(obj.id, user) if user else False

    def get_type(self, obj):
        return obj.get_type_display() if hasattr(obj, 'get_type_display') else str(obj.type)


class BookServiceRequestSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(help_text="UUID of the service to book")
    datetime = serializers.CharField(help_text="ISO 8601 formatted datetime string for the booking (e.g., '2023-10-01T12:00:00Z')")
