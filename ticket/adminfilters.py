from django.contrib import admin
from django.db.models import Q


class TicketDeliveredFilter(admin.SimpleListFilter):
    # title of the filter
    title = 'Ticket Status'
    parameter_name = 'delivered'

    def lookups(self, request, model_admin):
        """
        list of the choices for the filter
        """
        return (
            ('true', 'Delivered'),
            ('false', 'Not delivered'),
        )

    def queryset(self, request, queryset):
        """
        filter the results based on the value
        """
        # filter based on the value of the filter
        if self.value() == 'true':
            # get the tickets that are delivered
            # return the queryset with the right parameters
            return queryset.filter(Q(delivered=True))
        elif self.value() == 'false':
            # get the tickets that are still inside the service.
            return queryset.filter(Q(delivered=False))
