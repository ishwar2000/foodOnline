from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

def send_verification_link(request, user):
    currentSite = get_current_site(request)
    mailSubject = "Please Activate your Account"
    message = render_to_string("accounts/emailVerification.html",
                               {"user":user, "domain":currentSite, 
                                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                                "token":default_token_generator.make_token(user)})
    toMail = user.email
    # print(message, toMail)
    mail = EmailMessage(mailSubject, message, to=[toMail], from_email="Food Online")
    mail.content_subtype = "html"
    mail.send()

def sendResetToken(request, user):
    currentSite = get_current_site(request)
    mailSubject = "Please Reset your Password"
    message = render_to_string("accounts/resetToken.html",
                               {"user":user, "domain":currentSite, 
                                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                                "token":default_token_generator.make_token(user)})
    toMail = user.email
    # print(message)
    mail = EmailMessage(mailSubject, message, to=[toMail], from_email="Food Online")
    mail.content_subtype = "html"
    mail.send()

def vendorApproveStatus(mailSubject, isApproved, user):
    message = render_to_string("accounts/vendorApproveStatus.html",
                               {"user":user,  
                                "isApproved":isApproved 
                                })
    toMail = user.email
    # print(message)
    mail = EmailMessage(mailSubject, message, to=[toMail], from_email="Food Online")
    mail.content_subtype = "html"
    # mail.send()