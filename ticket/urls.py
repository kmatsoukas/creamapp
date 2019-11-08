from django.conf.urls import url, include
from ticket.views import print_pdf


urlpatterns = [
    url(r'(?P<pk>\d+)/print', print_pdf)
]