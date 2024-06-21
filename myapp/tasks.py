from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_email_task(subject, from_email, recipient_list, template_name, context):
  html_content = render_to_string(template_name, context)
  text_content = 'This is an important message.'

  msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
  msg.attach_alternative(html_content, "text/html")
  msg.send()

@shared_task
def notify_invitation(recipient_list, context):
  html_content = render_to_string('invitation.html', context)
  text_content = 'Invitation to team.'

  msg = EmailMultiAlternatives('Team invitation', text_content, 'klaus.trabalhando@gmail.com', recipient_list)
  msg.attach_alternative(html_content, "text/html")
  msg.send()