import os
from io import BytesIO
from celery import Celery
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

app = Celery('tasks', broker_url='redis://127.0.0.1:6379')


@app.task
def payment_completed(order_id):
    """
    task to send an e-mail notification when an order is
    successfully completed
    """
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'MY Shop - EE Invoice no, {order.id}'
    message = 'Please, find the attached invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])

    # generate PDF
    template_path = render_to_string('orders/order/pdf.html')
    context = {'order': order}
    out = BytesIO()
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, link_callback=link_callback)

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()


def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            f'media URI must start with {sUrl} or {mUrl}')
    return path