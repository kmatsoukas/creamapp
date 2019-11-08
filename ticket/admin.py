from django.contrib import admin
from ticket.models import Ticket, TicketStatus, Charges
from ticket.adminfilters import TicketDeliveredFilter


class ChargesInline(admin.TabularInline):
    model = Ticket.parts.through


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin class for the Ticket class.
    """
    list_display = [
        'id',
        'client_name',
        'client_phone',
        'ticket_status',
        'date_admitted',
        'device_model',
        'device_serial_number',
        'total_cost',
        'delivered',
        'ticket_pdf'
    ]

    inlines = [
        ChargesInline
    ]

    list_filter = (
        TicketDeliveredFilter,
    )

    search_fields = [
        'client__first_name',
        'client__last_name',
        'device__serial_number'
    ]

    def client_name(self, obj):
        """
        returns the full name of the client associated with the ticket
        """
        return obj.client.full_name()
    # set the description of the field
    client_name.short_description = 'Client'

    def client_phone(self, obj):
        """
        returns the phone of the client associated with the ticket
        """
        return obj.client.phone_number()
    # set the description of the field
    client_phone.short_description = 'Phones'

    def device_model(self, obj):
        """
        returns the model of the device associated with the ticket
        """
        return obj.device.model.name
    # set the description of the field
    device_model.short_description = "Model"

    def device_serial_number(self, obj):
        """
        returns the serial number of the device associated with the ticket
        """
        return obj.device.serial_number
    # set the description of the field
    device_serial_number.short_description = "Serial #"

    def ticket_status(self, obj):
        """
        returns status of the ticket
        """
        return obj.status.status
    # set the description of the field
    ticket_status.short_description = "Status"

    def ticket_pdf(self, obj):
        """
        returns the link to the pdf print
        """
        return '<a href="/tickets/{0}/print" target="_blank">Print PDF</a>'.format(obj.id)
    ticket_pdf.allow_tags = True
    ticket_pdf.short_description = 'PDF Report'

    def date_admitted(self, obj):
        """
        Returs the date admitted to the service.
        """
        return obj.admission_date.strftime("%d-%m-%Y")
    date_admitted.short_description = 'Date Admitted'

    def total_cost(self, obj):
        """
        returns the total cost of the ticket including the parts used.
        """
        return "{0} €".format(obj.total_cost())

    total_cost.short_description = "Total Cost"


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    pass

