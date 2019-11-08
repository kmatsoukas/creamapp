from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from datetime import datetime
from utils.notifications.mail import send_mail


class Client(models.Model):
    """
    Client model for the clients tickets
    """
    # TODO: Add an adrress field
    # TODO: Separate the phone fields into different models
    # TODO: Add ticket number field and auto generate it on save.
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=14, blank=True, default="")
    mobile = models.CharField(max_length=14, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    comment = models.TextField(max_length=300, blank=True, default="")
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ('last_name',)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return " ".join([self.last_name, self.first_name])

    def phone_number(self):
        if self.phone:
            home = "Σταθερο: {}".format(self.phone)
        else:
            home = "Σταθερο: N/A"
        if self.mobile:
            mobile = "Κινητο: {}".format(self.mobile)
        else:
            mobile = "Κινητο: N/A"
        return " - ".join([home, mobile])

    def landline(self):
        """
        returns the landline of the client and N/A if not available
        :return: string
        """
        if not self.phone:
            return 'N/A'
        else:
            return self.phone

    def mobile_phone(self):
        """
        returns the mobile phone of the client and N/A if not available
        :return: string
        """
        if not self.mobile:
            return 'N/A'
        else:
            return self.mobile


class DeviceType(models.Model):
    """
    Model that's assosiated with the device class. It keeps the device type for each device.
    """
    type = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return self.type


class DeviceModel(models.Model):
    """
    Model for the devices names....
    """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Model for the devices of the tickets that's assosiated to the client
    """
    client = models.ForeignKey(Client, related_name='devices')
    model = models.ForeignKey(DeviceModel, related_name='devices', blank=True, null=True)
    serial_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    comment = models.TextField(max_length=200, null=True, blank=True)
    type = models.ForeignKey(DeviceType, related_name='devices')

    class Meta:
        ordering = ('model',)

    def __str__(self):
        return " ".join([self.client.full_name(), self.serial_number, '-', self.model.name])


class SubscriptionType(models.Model):
    """
    Model for the types of subscriptions for the clients
    """
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Subscription(models.Model):
    """
    Model for client subscriptions
    """

    client = models.ForeignKey(Client, related_name='subscriptions')
    type = models.ForeignKey(SubscriptionType, related_name='subscriptions')
    description = models.CharField(max_length=50)
    create_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return " - ".join([str(self.id), self.description])

    def notify_expiration(self, days):
        subject = '{0} subscription - {1} ending in {2} days'.format(self.client.full_name(), self.description, days)
        context = {
            'client': self.client,
            'subscription': " - ".join([self.type.description, self.description]),
            'expiration_date': self.active_payment().paid_until.strftime("%d-%m-%Y"),
            'price': "".join([str(self.active_payment().amount), '€']),
            'days': days
        }
        send_mail('support@d-h.gr', subject, context)

    def paid_for(self, sub_months=None, start_now=False):
        # check if the the start date is counting from the expiration day of today
        if not sub_months:
            months = self.duration
        else:
            months = sub_months
        if start_now:
            self.start_date = datetime.date(datetime.now())
            self.duration = months
        else:
            self.start_date = self.expiration_date
            self.duration = months
        # save the model to update the subscription dates
        self.save()

    def last_payment(self):
        """
        Get the last payment transaction of the subscription
        """
        return self.payments.last()

    def active_payment(self):
        """
        Get the active payment of the subscription
        """
        date = datetime.date(datetime.now())
        return self.payments.filter(paid_until__gte=date).first()

    # static methods
    @staticmethod
    def expire_in_days(days):
        """
        returns the subscriptions that expire in n days.
        :param days: integer
        :return:
        """
        return Subscription.objects.filter(payments__paid_until=datetime.now() + relativedelta(days=days))

    def save(self, *args, **kwargs):
        """
        Override the default save method of the model
        """
        if self.create_date is None:
            self.create_date = datetime.now()
        super(Subscription, self).save(*args, **kwargs)


class Payment(models.Model):
    """
    Track payments for the client subscriptions
    """

    # durations of the subscriptions
    DURATIONS = (
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '12 Months'),
        (24, '24 Months'),
    )

    client = models.ForeignKey(Client, related_name='payments')
    subscription = models.ForeignKey(Subscription, related_name='payments')
    duration = models.IntegerField(choices=DURATIONS, default=12)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid_on = models.DateField()
    paid_until = models.DateField(blank=True)

    def __str__(self):
        return " ".join([self.client.full_name(), self.subscription.description])

    def save(self, *args, **kwargs):
        self.paid_until = self.paid_on + relativedelta(months=self.duration)
        self.client = self.subscription.client
        # run the super
        super(Payment, self).save(*args, **kwargs)







