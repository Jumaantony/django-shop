from celery import Celery
from django.core.mail import send_mail
from .models import Order

# connect to redis

app = Celery('tasks', broker='amqp://pd3cfd77a31e74f3a8271be9add8fb55ee70ba9e229f9033f779c1980fc5dc71b:**@ec2-44-195'
                             '-137-100.compute-1.amazonaws.com\:7000//:')


# redis://:pd3cfd77a31e74f3a8271be9add8fb55ee70ba9e229f9033f779c1980fc5dc71b:**@ec2-44-195-137-100.compute-1.amazonaws
# .com\:7000//:


@app.task
def order_created(order_id):
    # task to send an email notification when an order is created
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message,
                          'odongoanton2@gmail.com',
                          [order.email])
    return mail_sent