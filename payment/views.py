import braintree
import weasyprint
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def payment_process(request):
    """Обработчик процесса оплаты онлайн"""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Получение токена для создания транзакции.
        nonce = request.POST.get('payment_method_nonce', None)
        # Создание и сохранение транзакции
        result = braintree.Transaction.sale(
            {
                'amount': '{:.2f}'.format(order.get_total_const()),
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True
                }
            })
        if result.is_success:
            # Отметка заказа как оплаченного
            order.paid = True
            # Сохранение ID транзакции в заказе
            order.braintree_id = result.transaction.id
            order.save()
            # Создание электронного сообщения.
            subject = _(f'My Shop - Invoice №{order.id}')
            message = _('Please, find attached the invoice for your recent purchase.')
            email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
            # Формирование PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '\\css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            # Прикрепляем PDF к электронному сообщению.
            email.attach(f'order_{order.id}', out.getvalue(), 'application/pdf')
            # Отправка сообщения.
            email.send()
            mark_safe(messages.success(request, _(f'Order paid, thank you. \
                                                   Click <a class="text-secondary" \
                                                   href={reverse_lazy("shop:product_list")}>here</a> \
                                                   to continue shopping. \
                                                   The file with the paid order was sent to the {order.email}')))
            return redirect('payment:done')
        else:
            mark_safe(messages.error(request, _(f'Something went wrong, \
                                                click <a class="text-secondary" \
                                                href="{reverse_lazy("shop:product_list")}">here</a> \
                                                to return to purchase back. \
                                                Thanks for understanding.')))
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JavaScript SDK
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')





