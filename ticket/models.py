from django.db import models
from client.models import Client, Device
from storage.models import Part


class TicketStatus(models.Model):
    """
    Model for the status of the ticket
    """
    status = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=30, blank=True, default="")

    def __str__(self):
        return self.status


class Ticket(models.Model):
    """
    Model for the tickets opened for the clients.
    """
    client = models.ForeignKey(Client, related_name='tickets')
    device = models.ForeignKey(Device, related_name='tickets')
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(TicketStatus, related_name='tickets')
    delivered = models.BooleanField(default=False)
    problem = models.TextField(max_length=400)
    diagnosis = models.TextField(max_length=600, blank=True, default="")
    actions = models.TextField(max_length=600, blank=True, default="")
    work_charge = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    parts = models.ManyToManyField(Part, through='Charges', through_fields=('ticket', 'part'), related_name='tickets')

    def __str__(self):
        return "{} - {}".format(self.client, self.device)

    def parts_cost(self):
        """
        calculate the total cost of the parts used in the ticket
        """
        return sum([x.charge for x in self.charges.all()])

    def total_cost(self):
        """
        return the total cost of the ticket
        :return: decimal
        """
        return sum([self.parts_cost(), self.work_charge])

    def discharge_full_date(self):
        if self.discharge_date:
            return self.discharge_date.strftime("%d-%m-%Y")
        return 'N/A'


class Charges(models.Model):
    """
    Class for the Charges of the ticket parts
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='charges')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='charges')
    charge = models.DecimalField(max_digits=6, decimal_places=2)
    serial_number = models.CharField(max_length=30, blank=True, default="")
