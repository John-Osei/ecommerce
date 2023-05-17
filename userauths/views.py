from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from userauths.forms import UserLoginForm, UserRegisterForm, ProfileForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from userauths.models import Profile
from .models import SubscribedUsers

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from userauths.tokens import account_activation_token
from django.db.models.query_utils import Q

from django.contrib.auth.decorators import login_required
from .decorators import user_is_superuser






# User = settings.AUTH_USER_MODEL
#Addded by me

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have an account!")
    return redirect("core:index")



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect("userauths:sign-in")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('core:index')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("userauths/activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b> {to_email} </b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')





def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(request.META.get("HTTP_REFERER", "core:index")) 

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        
    else:
        form = UserRegisterForm()


    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, f"Hello! You are already logged in")
        return redirect(request.META.get("HTTP_REFERER", "core:index"))  

    if request.method == "POST":
        
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect(request.META.get("HTTP_REFERER", "core:index")) 

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="userauths/sign-in.html",
        context={"form": form}
        )

        
@login_required
def logout_view(request):

    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")

@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed, Login to continue")
            return redirect("userauths:sign-in")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)


    form = SetPasswordForm(user)
    return render(request, 'userauths/password_reset_confirm.html', {'form': form})


def password_reset_request(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("userauths/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """"
                        <h2>Password reset sent</h2>
                        <p>
                            We've emailed you instructions for setting your password, If an account exist with the email you provided.
                            You should receive them shortly. <br> If you receive an email, please make sure you've entered the address
                            you registered with, and check your spam folder
                        </p>

                        """
                    )
                else:
                    messages.error(redirect, "Probelm sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect("core:index")

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue
    form = PasswordResetForm()     
    context = {
        'form': form,
    }

    return render(request=request, template_name='userauths/reset-password.html', context=context)

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in</b> now.")
                return redirect("userauths:sign-in")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'userauths/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("core:index")

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must type legit email to subscribe to a Newsletter")
            return redirect("core:index")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "core:index")) 

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "core:index"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("core:index")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "core:index"))  



# @user_is_superuser
# def newsletter(request):
#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data.get('subject')
#             receivers = form.cleaned_data.get('receivers').split(',')
#             email_message = form.cleaned_data.get('message')

#             mail = EmailMessage(subject, email_message, f"PyLessons <{request.user.email}>", bcc=receivers)
#             mail.content_subtype = 'html'

#             if mail.send():
#                 messages.success(request, "Email sent succesfully")
#             else:
#                 messages.error(request, "There was an error sending email")

#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)

#         return redirect('/')

#     form = NewsletterForm()
#     form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
#     return render(request=request, template_name='userauths/newsletter.html', context={'form': form})

