from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task
def send_notification_email(subject, message, from_email, recipient_list):
    print('send_notification_email called')
    logger.info(f'Sending email with subject: {subject}, from: {from_email}, to: {recipient_list}')
    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info('Email sent successfully')
    except Exception as e:
        logger.error(f'Error sending email: {e}')