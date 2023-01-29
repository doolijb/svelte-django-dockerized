from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# from templated_email import send_templated_mail


# def send_confirmation_email(request, email_address):
#     confirmation = EmailConfirmation.create(email_address)
#     domain = request.get_host()
#     send_templated_mail(
#         template_name="email_confirmation",
#         subject="Email Confirmation",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[email_address],
#         context={
#             "website": f"https://{domain}",
#             "confirmation_url": f"https://{domain}{reverse('account_confirm_email', kwargs={'key':confirmation.key})}",
#         },
#     )
#     confirmation.sent = timezone.now()
#     confirmation.save()


# def send_password_reset_email(request, email_address, token):
#     domain = request.get_host()
#     send_templated_mail(
#         template_name="password_reset_token",
#         subject="Password Reset",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[email_address],
#         context={
#             "website": f"https://{domain}",
#             "reset_url": f"https://{domain}/account/password/reset/{token}",
#         },
#     )
