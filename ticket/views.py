from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ticket.models import Ticket
from utils.pdf.ticket import TicketPDF


def print_pdf(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    pdf = TicketPDF(ticket)
    return pdf.render()

    # if ticket:
    #     return HttpResponse(ticket)

