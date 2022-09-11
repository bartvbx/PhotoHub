# Import django first to prevent error 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.'
import django
django.setup()

from datetime import date, datetime, timedelta, timezone
from smtplib import SMTPException

from celery import shared_task
from django.core.mail import EmailMessage

from photos.models import Photo
from users.models import Profile


def send_summary_email(user) -> str:
    """
    Send an email with photos added by followed users within the last day.
    """
    followed_by_user = Profile.objects.filter(follows=user)
    last_mail = datetime.now(timezone.utc) - timedelta(days=1)
    new_photos = Photo.objects.filter(author__profile__in=followed_by_user, created__gte=last_mail)

    if len(new_photos) > 0:
        email_content = (
            "Hello,\n"
            f"There are {len(new_photos)} new photo(s) added by users you are following.\n"
            "Check the list below and visit PhotoHub to see details, give a like, and comment!\n"
            "Photos added within the last 24 hours:\n"
        )
        for photo in new_photos:
            email_content += f'- "{photo.title}" [{photo.category}] by {photo.author.username} \n'
        email_content += (
            "Have a great day,\n"
            "PhotoHub team"
        )
    else:
        email_content = (
            "Hello,\n"
            "Unfortunately, none of the users you follow have added new photos lately.\n"
            "Maybe it's a good opportunity to surprise them by uploading your own?\n"
            "Don't hesitate and visit PhotoHub!\n"
            "Have a great day,\n"
            "PhotoHub team"
        )

    email = EmailMessage(
        f"PhotoHub - {date.today()} followed users activity summary",
        email_content,
        "photohub@photohub.com",
        [user.user.email]
    )

    try:
        email.send(fail_silently=False)
        return "Email have been sent successfully"
    except SMTPException as e:
        return f"Email hasn't been sent: {e}"


@shared_task
def send_daily_email():
    """
    Send daily summary emails to users that confirmed they want to receive them.
    """
    users_accepting_emails = Profile.objects.filter(summary_email=True).all()

    for user in users_accepting_emails:
        send_summary_email(user)

    if len(users_accepting_emails) < 1:
        return "Emails haven't been sent, none of the users accepts summary emails"

    return "Emails have been sent"
