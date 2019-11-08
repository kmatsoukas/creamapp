from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, BaseDocTemplate, PageTemplate, FrameBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import Color
from django.http import HttpResponse
import os

PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]


class TicketPDF:
    """
    Generate pdf of a Ticket.
    """
    # generate the paths for the files used.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(base_dir, 'assets', 'Verdana.ttf')
    font_file_bold = os.path.join(base_dir, 'assets', 'VerdanaBold.ttf')
    background_image = os.path.join(base_dir, 'assets', 'prosfora.jpg')
    dh_logo = os.path.join(base_dir, 'assets', 'dhlogo.jpg')
    # default font
    font = 'Verdana'
    base_color = Color(0, 0.6, 0.8, 1)
    # paragraph styles
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    styleH2 = styles['Heading3']
    styleB = styles['BodyText']
    # change the font of the styles
    styleH.fontName = font
    styleH2.fontName = font
    styleN.fontName = font
    styleB.fontName = font
    # change the heading1 style
    styleH.borderWidth = 1
    styleH.borderColor = Color(0, 0.6, 0.8, 1)
    styleH.fontSize = 14
    styleH.alignment = 1
    # story lists for the frames
    story = []
    # create the frames
    htwelve = PAGE_HEIGHT / 12
    info_frame_left = Frame(0, htwelve * 9, PAGE_WIDTH/2, (PAGE_HEIGHT / 12) * 1.4, leftPadding=30)
    info_frame_right = Frame(PAGE_WIDTH / 2, htwelve * 9, PAGE_WIDTH / 2, htwelve * 1.4, leftPadding=30)
    left_frame = Frame(0, htwelve * 6, PAGE_WIDTH / 2, htwelve * 3, leftPadding=30)
    right_frame = Frame(PAGE_WIDTH / 2, htwelve * 6, PAGE_WIDTH / 2, htwelve * 3, leftPadding=30)
    actions_frame = Frame(0, htwelve * 4, PAGE_WIDTH, htwelve * 2, leftPadding=30)
    parts_frame = Frame(0, 0, PAGE_WIDTH, htwelve * 4, leftPadding=30)

    def __init__(self, ticket):
        # Generate the response object and set the contant type
        self.response = HttpResponse(content_type='application/pdf')
        # Change the disposition of the pdf file
        self.response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
        # register the font to the pdf class
        pdfmetrics.registerFont(TTFont('Verdana', self.font_file))
        pdfmetrics.registerFont(TTFont('VerdanaBold', self.font_file_bold))
        # get the ticket passed to the class.
        self.ticket = ticket

    def print_client_info(self):
        """
        Prints the client info to the pdf
        """
        self.story.append(
            Paragraph('Πληροφορίες Πελάτη', self.styleH)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Πελάτης: </font>{0}'.format(self.ticket.client.full_name()), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Σταθερό: </font>{0}'.format(self.ticket.client.landline()), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Κινητό: </font>{0}'.format(self.ticket.client.mobile_phone()), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Service ID: </font>{0}'.format(self.ticket.id), self.styleN)
        )
        self.story.append(FrameBreak())

    def print_device_info(self):
        """
        Prints the device info to the pdf
        """
        self.story.append(
            Paragraph('Πληροφορίες Συσκευής', self.styleH)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Ημερομηνία Εισαγωγής: </font>{0}'.format(self.ticket.admission_date.strftime("%d-%m-%Y")), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Ημερομηνία Εξαγωγής: </font>{0}'.format(self.ticket.discharge_full_date()), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>Συσκευή: </font>{0}'.format(self.ticket.device.model), self.styleN)
        )
        self.story.append(
            Paragraph('<font color=(0,0.6,0.8)>S/N: </font>{0}'.format(self.ticket.device.serial_number), self.styleN)
        )
        self.story.append(FrameBreak())

    def print_problem(self):
        """
        Print the problem of the ticket
        """
        self.story.append(
            Paragraph('Περιγραφή Προβήματος', self.styleH)
        )
        self.story.append(
            Paragraph(self.ticket.problem, self.styleB)
        )
        self.story.append(FrameBreak())

    def print_diagnosis(self):
        """
        Print the diagnosis of the ticket
        """
        self.story.append(
            Paragraph('Διάγνωση Προβλήματος', self.styleH)
        )
        self.story.append(
            Paragraph(self.ticket.diagnosis, self.styleB)
        )
        self.story.append(FrameBreak())

    def print_actions(self):
        """
        Print the actions of the ticket
        """
        self.story.append(
            Paragraph('Ενέργειες Τεχνικού', self.styleH)
        )
        self.story.append(
            Paragraph(self.ticket.actions, self.styleB)
        )
        self.story.append(FrameBreak())

    def print_parts(self):
        """
        Prints the table of the used parts.
        """
        self.story.append(
            Paragraph('Ανταλλακτικά', self.styleH)
        )
        heading = [['Ανταλλακτικό', 'Serial Number', 'Τιμή']]
        parts = [[x.part.part, x.serial_number, "{0} €".format(x.charge)] for x in self.ticket.charges.all()]
        prices = [
            ['', 'Σύνολο Ανταλλακτικών', "{0} €".format(self.ticket.parts_cost())],
            ['', 'Σύνολο Εργασίας', "{0} €".format(self.ticket.work_charge)],
            ['', 'Τελικό Σύνολο', "{0} €".format(self.ticket.total_cost())]
        ]
        data = heading + parts + prices
        # set the table style
        tstyle = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONT', (0, 0), (-1, -1), self.font),
            ('TEXTCOLOR', (0, 0), (2, 0), self.base_color),
            ('FONT', (0, 0), (2, 0), 'VerdanaBold'),
            ('FONTSIZE', (0, 0), (2, 0), 12),
            ('LINEABOVE', (0, 1), (2, 1), 1, self.base_color),
            ('TEXTCOLOR', (-2, -3), (-2, -2), self.base_color),
            ('TEXTCOLOR', (-2, -1), (-1, -1), self.base_color),
            ('FONT', (-2, -1), (-1, -1), 'VerdanaBold'),
            ('FONTSIZE', (-2, -3), (-1, -2), 12),
            ('FONTSIZE', (-2, -1), (-1, -1), 14),
        ])
        table = Table(data, colWidths=[((PAGE_WIDTH / 12) * 10) / 3] * 3)
        table.setStyle(tstyle)
        self.story.append(table)

    @staticmethod
    def build_page(canvas, doc):
        canvas.saveState()
        canvas.drawImage(TicketPDF.background_image, 0, 0)
        canvas.drawImage(TicketPDF.dh_logo, 50, 750, 200, 80, True, 'c')
        canvas.setFont(TicketPDF.font, 18)
        canvas.drawString(350, 780, "Παραστατικό Service")
        # print the dividing line
        # TicketPDF.draw_line(730)
        canvas.setFont(TicketPDF.font, 16)
        canvas.restoreState()

    def render(self):
        """
        Render the file and return the HttpResponse with the file.
        :return: HttpResponse
        """
        doc = BaseDocTemplate(
            self.response,
            title="{0} - ServiceID {1}".format(self.ticket.client.full_name(), self.ticket.id),
            author='Digital Horizon'
        )
        doc.addPageTemplates([
            PageTemplate(
                frames=[
                    self.info_frame_left,
                    self.info_frame_right,
                    self.left_frame,
                    self.right_frame,
                    self.actions_frame,
                    self.parts_frame
                ], onPage=TicketPDF.build_page
            )
        ])
        self.print_client_info()
        self.print_device_info()
        self.print_problem()
        self.print_diagnosis()
        self.print_actions()
        self.print_parts()
        doc.build(self.story)
        return self.response
