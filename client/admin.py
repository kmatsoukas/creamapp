from django.contrib import admin
from client.models import Client, DeviceType, Device, Subscription, SubscriptionType, Payment, DeviceModel
from datetime import datetime
from client.adminfilters import SubscriptionExpirationFilter, SubscriptionTypeFilter


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceModel)
class DiviceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    pass


class SubscriptionsInline(admin.TabularInline):
    model = Payment
    extra = 1

    exclude = [
        'paid_until',
        'client'
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [
        SubscriptionsInline,
    ]
    # list of fields to display
    list_display = [
        'client',
        'description',
        'type',
        'subscription_status',
        'create_date',
        'last_payment',
        'expires_in'
    ]

    list_filter = (
        SubscriptionExpirationFilter,
        SubscriptionTypeFilter
    )

    def expires_in(self, obj: Subscription):
        """
        returns the expiration date of the last payment
        """
        last_payment = obj.active_payment()
        if last_payment:
            return last_payment.paid_until
        else:
            return 'Never Paid'

    def last_payment(self, obj: Subscription):
        """
        return the last payment date
        """
        last_payment = obj.active_payment()
        if last_payment:
            return last_payment.paid_on
        else:
            return 'Never Paid'

    def subscription_status(self, obj: Subscription):
        """
        returns the status of the subscription
        """
        last_payment = obj.active_payment()
        if last_payment:
            if last_payment.paid_until < datetime.date(datetime.now()):
                return 'Expired'
            else:
                return 'Active'
        else:
            return 'Never Paid'

    def client(self, obj: Subscription):
        """
        return the full name of the client
        """
        return obj.client.full_name()


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # exclude fields from the admin form
    exclude = ('paid_until',)
    # list of fields to display on the table
    list_display = [
        'subscription',
        'subscription_client',
        'duration',
        'amount',
        'paid_on',
        'paid_until'
    ]

    def subscription_client(self, obj: Payment):
        """
        return the client's name
        """
        return obj.client.full_name()
