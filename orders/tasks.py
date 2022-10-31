from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task()
def order_created(order_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""
    order = Order.objects.get(id=order_id)
    subject = f'Order №{order.id}'
    message = f'Dear {order.first_name}, thanks for your order \U0001F609' \
              f'\n\nYou have successfully placed an order in our store!. ' \
              f'You order id is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@My_shop.com', [order.email])

    return mail_sent

