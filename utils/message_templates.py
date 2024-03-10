from django.template.loader import render_to_string
from django.utils.html import strip_tags


class message:
    html_message = None
    subject = None
    plain_message = None

    def signup_message(self, user):
        self.html_message = render_to_string('email/signup.html', {'user': user})
        self.subject = "Account Approved at Lootlo"
        self.plain_message = strip_tags(render_to_string('email/signup.html', {'user': user}))


    def reset_password(self, user,token):
        self.html_message = render_to_string('email/reset_password.html', {'user': user,'token':token})
        self.subject = "Reset password email"
        self.plain_message = strip_tags(render_to_string('email/reset_password.html', {'user': user}))

    def reset_password_confirmation(self, user):
        self.html_message = render_to_string('email/reset_password_confirmation.html', {'user': user})
        self.subject = "Reset password confirmation email"
        self.plain_message = strip_tags(render_to_string('email/reset_password_confirmation.txt', {'user': user}))
