from django.contrib.auth.models import AbstractUser
from django.db.models import CharField,DecimalField, PositiveIntegerField, IntegerField, BooleanField, Model, TextChoices, PROTECT, ForeignKey, TextField, EmailField
from django_resized import ResizedImageField
from apps.utils.token import bot_activation_token

from apps.models.payments import PaymentHistory


class User(AbstractUser):
    phone = CharField(max_length=255, unique=True)
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='users')
    address = CharField(max_length=555, blank=True, null=True)
    telegram_id = CharField(max_length=55, null=True, blank=True)
    bot_is_activate = BooleanField(default=False)
    bot_active_token = CharField(max_length=255, unique=True)
    balance = DecimalField(max_digits=30, decimal_places=2, default=0)  # main balance
    bonus = PositiveIntegerField(default=0)  # bonus balance
    deposit = DecimalField(max_digits=30, decimal_places=2, default=0)  # deposit balance
    coin = PositiveIntegerField(default=0)

    @property
    def payout(self):
        amounts = self.paymenthistory_set.filter(
            status=PaymentHistory.StatusChoices.ACCEPTED
        ).values_list('amount', flat=True)
        return sum(amounts)


class Contact(Model):
    phone = CharField(max_length=255)
    email = EmailField(max_length=255)
    telegram = CharField(max_length=255)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


class Tickets(Model):
    class SenderTextChoice(TextChoices):
        XARIDOR = 'customer', 'xaridor'
        KURYER = 'kuryer', 'kuryer'
        ADMIN = 'admin', 'admin'
        SOTUVCHI = 'salesman', 'sotuvchi'
        BOSHQA = 'other', 'boshqa'

    class PurposeTextChoice(TextChoices):
        MUAMMO = 'issue', 'muammo'
        TAKLIF = 'suggestion', 'taklif'

    author = ForeignKey(User, PROTECT)
    sender = CharField(max_length=55, choices=SenderTextChoice.choices)
    sender_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    ticket_purpose = CharField(max_length=55, choices=PurposeTextChoice.choices)
    message = TextField()
