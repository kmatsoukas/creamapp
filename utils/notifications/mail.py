import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
from django.template import loader


def send_mail(send_to, subject, context, send_from='hosting@d-h.gr', server="smtp.office365.com", port=587,
                          tls=True, html=True,
                          username='kostas@d-h.gr', password='7419km!*'):
    """
    Send an email with office365 or any other provider.
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to if isinstance(send_to, str) else COMMASPACE.join(send_to)
    msg['Subject'] = subject

    content = loader.render_to_string('notification.html', context, using=None)

    msg.attach(MIMEText(content, 'html' if html else 'plain'))
    smtp = smtplib.SMTP(server, int(port))

    if tls:
        smtp.starttls()

    if username is not None:
        smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
