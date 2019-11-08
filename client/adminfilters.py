from django.contrib import admin
from datetime import datetime, timedelta
from django.db.models import Q
from client.models import SubscriptionType


class SubscriptionExpirationFilter(admin.SimpleListFilter):
    # title of the filter
    title = 'Expires'
    parameter_name = 'payments'

    def lookups(self, request, model_admin):
        """
        list of the choices for the filter
        """
        return (
            ('week', 'This week'),
            ('month', 'This month'),
            ('year', 'This year'),
            ('expired', 'Expired')
        )

    def queryset(self, request, queryset):
        """
        filter the results based on the value
        """
        # date of today
        date = datetime.date(datetime.now())
        # filter based on the value of the filter
        if self.value() == 'week':
            week_day = date.weekday()
            # get the from and to days
            # the week is from monday to sunday
            from_date = date - timedelta(days=week_day)
            to_date = date + timedelta(days=6 - week_day)
            # return the queryset with the right parameters
            return queryset.filter(Q(payments__paid_until__gte=date) & Q(payments__paid_until__lte=to_date))
        elif self.value() == 'month':
            # first day of the month
            from_date = date - timedelta(days=date.day - 1)
            # get the last day of the month
            if date.month == 12:
                to_date = date.replace(day=31)
            else:
                to_date = date.replace(month=date.month + 1, day=1) - timedelta(days=1)
            # return the queryset with the right parameters
            return queryset.filter(Q(payments__paid_until__gte=date) & Q(payments__paid_until__lte=to_date))
        elif self.value() == 'year':
            # get the first and last day of the year
            from_date = date.replace(month=1, day=1)
            to_date = date.replace(month=12, day=31)
            # return the queryset with the right parameters
            return queryset.filter(Q(payments__paid_until__gte=date) & Q(payments__paid_until__lte=to_date))
        elif self.value() == 'expired':
            # return the queryset with the right parameters
            return queryset.filter(payments__paid_until__lte=date)


class SubscriptionTypeFilter(admin.SimpleListFilter):
    # title of the filter
    title = 'Type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        """
        list of the choices for the filter
        """
        return ((sub.id, sub.description) for sub in SubscriptionType.objects.all())

    def queryset(self, request, queryset):
        """
        filter the results based on the value
        """
        if self.value():
            return queryset.filter(type=self.value())