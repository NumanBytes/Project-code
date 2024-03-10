from django.conf import settings
from django.core.mail import send_mail
from .message_templates import message


class EmailClient:
    sender = str(settings.EMAIL_HOST_USER)
    fail_silently = not settings.DEBUG
    msg = message()

    def send_signup_email(self, user):
        self.msg.signup_message(user)
        sent = send_mail(
            subject=self.msg.subject,
            html_message=self.msg.html_message,
            message=self.msg.plain_message,
            recipient_list=[user.email],
            fail_silently=self.fail_silently,
            from_email=self.sender
        )
        return sent

    def reset_password_email(self,user,token):
        self.msg.reset_password(user,token)
        sent=send_mail(
            subject=self.msg.subject,
            html_message=self.msg.html_message,
            message=self.msg.plain_message,
            recipient_list=[user.email],
            fail_silently=self.fail_silently,
            from_email=self.sender)
        return sent

    def reset_password_confirmation(self,user):
        self.msg.reset_password_confirmation(user)
        sent = send_mail(
            subject=self.msg.subject,
            html_message=self.msg.html_message,
            message=self.msg.plain_message,
            recipient_list=[user.email],
            fail_silently=self.fail_silently,
            from_email=self.sender)
        return sent
