import string
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def async_send_mail(
        message, subject, from_email,
        recipient, fail_silently=True
):
    send_mail(
        message='',
        html_message=message,
        subject=subject, 
        from_email=from_email, 
        recipient_list=[recipient],
        fail_silently=fail_silently,
    )


class AsyncEmailMessage:
    from_email = 'test@test.test'
    
    def __init__(self, body, subject, to):
        self.body = body
        self.to = to
        self.subject = subject
    
    def send(self, fail_silently=True):
        if isinstance(self.to, (tuple, list)):
            for recipient in self.to:
                async_send_mail.delay(
                    message=self.body, 
                    subject=self.subject, 
                    from_email=self.from_email,
                    recipient=recipient,
                    fail_silently=fail_silently,
                )
        elif isinstance(self.to, (string,)):
            async_send_mail.delay(
                message=self.body,
                subject=self.subject,
                from_email=self.from_email,
                recipient=self.to,
                fail_silently=fail_silently,
            )
        else:
            raise TypeError('sending message failed unrecognized recipent address format '
                            'should be list, tuple or string')
