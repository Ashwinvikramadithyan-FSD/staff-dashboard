# hr/emails.py

from django.core.mail import send_mail
from django.conf import settings


def send_approval_email(borrow_request):
    subject = f"✅ Your Request for '{borrow_request.product.name}' has been Approved"
    message = f"""
Dear {borrow_request.first_name} {borrow_request.last_name},

Great news! Your borrow request has been APPROVED by HR.

━━━━━━━━━━━━━━━━━━━━━━━━━━
  REQUEST DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━
  Product     : {borrow_request.product.name}
  Code        : {borrow_request.product.code}
  Made In     : {borrow_request.product.made_in}
  Material    : {borrow_request.product.material}
  Take Time   : {borrow_request.take_time.strftime('%d %b %Y, %H:%M')}
  Return Time : {borrow_request.bring_time.strftime('%d %b %Y, %H:%M')}
  Status      : ✅ APPROVED
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please collect the product on time.

Regards,
Internal Asset Team
    """.strip()

    if borrow_request.staff_email:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@internalasset.com'),
            recipient_list=[borrow_request.staff_email],
            fail_silently=True,
        )


def send_rejection_email(borrow_request):
    subject = f"❌ Your Request for '{borrow_request.product.name}' has been Rejected"
    message = f"""
Dear {borrow_request.first_name} {borrow_request.last_name},

We regret to inform you that your borrow request has been REJECTED by HR.

━━━━━━━━━━━━━━━━━━━━━━━━━━
  REQUEST DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━
  Product     : {borrow_request.product.name}
  Code        : {borrow_request.product.code}
  Made In     : {borrow_request.product.made_in}
  Material    : {borrow_request.product.material}
  Take Time   : {borrow_request.take_time.strftime('%d %b %Y, %H:%M')}
  Return Time : {borrow_request.bring_time.strftime('%d %b %Y, %H:%M')}
  Status      : ❌ REJECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please contact HR if you have questions.

Regards,
Internal Asset Team
    """.strip()

    if borrow_request.staff_email:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@internalasset.com'),
            recipient_list=[borrow_request.staff_email],
            fail_silently=True,
        )