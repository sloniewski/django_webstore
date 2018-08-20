from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from webstore.core.utils import random_string, unique_id_generator
from webstore.payment.models import Payment

from . models import Order


@receiver(pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.uuid:
        instance.uuid = unique_id_generator(instance, random_string)


@receiver(post_save, sender=Payment)
def send_confirmation_mail(sender, instance, **kwargs):
    if kwargs['created']:
        # TODO hit database only once to get order and user details
        order = instance.order
        send_mail(
            subject='Order: {}, created'.format(order.uuid),
            message='Your order {}, is awating payment. Due amount is: {},'\
                    'please transfer money to {}. Order details can be'\
                    'viewed here {}'.format(
                        order.uuid, instance.value,
                        '123', order.get_absolute_url(),
                    ),
            from_email='test@test.com',
            recipient_list=[order.user.email],
        )
        return True
    return False
