from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile
from .forms import RegistrationForm, LoginForm
from booking_manager.models import BookingInquiry

def signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or getattr(request.user, 'profile', None) and request.user.profile.role == 'admin':
            return redirect('/admin-portal/dashboard/')
        return redirect('/accounts/user-panel/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            role = 'user'

            # Create User instance
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fullname
            )

            UserProfile.objects.create(
                user=user,
                phone_number=phone,
                role=role
            )

            # Auto-login after registration
            user_auth = authenticate(request, username=username, password=password)
            if user_auth:
                auth_login(request, user_auth)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                redirect_url = '/admin-portal/dashboard/' if (user.is_staff or role == 'admin') else '/accounts/user-panel/'
                return JsonResponse({
                    'status': 'success',
                    'message': 'Account created successfully! Welcome to Rentify.',
                    'redirect_url': redirect_url
                })

            messages.success(request, 'Registration successful! Welcome to Rentify.')
            if user.is_staff or role == 'admin':
                return redirect('/admin-portal/dashboard/')
            return redirect('/accounts/user-panel/')
        else:
            errors = [f"{field.capitalize()}: {err[0]}" for field, err in form.errors.items()]
            error_msg = " | ".join(errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            
            messages.error(request, error_msg)

    else:
        form = RegistrationForm()

    return render(request, 'user_accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin'):
            return redirect('/admin-portal/dashboard/')
        return redirect('/accounts/user-panel/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_user = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']

            # Resolve email to username if needed
            username = email_or_user
            user_obj = User.objects.filter(email__iexact=email_or_user).first()
            if user_obj:
                username = user_obj.username

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                auth_login(request, user)
                
                # Check user role
                is_admin = user.is_staff or user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')
                redirect_url = '/admin-portal/dashboard/' if is_admin else '/accounts/user-panel/'

                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful!',
                        'redirect_url': redirect_url
                    })

                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect(redirect_url)
            else:
                error_msg = 'Invalid credentials. Please check your email/username and password.'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)

                messages.error(request, error_msg)
        else:
            errors = [f"{err[0]}" for field, err in form.errors.items()]
            error_msg = " | ".join(errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)

            messages.error(request, error_msg)

    else:
        form = LoginForm()

    return render(request, 'user_accounts/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been signed out safely.')
    return redirect('/accounts/login/')


@login_required(login_url='/accounts/login/')
def user_panel_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        
        if action == 'submit_verification':
            if user_profile.verification_status == 'Verified':
                error_msg = "Your document is already verified & approved by admin. Verified documents are locked and cannot be modified."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                messages.error(request, error_msg)
                return redirect('/accounts/user-panel/')

            id_document_type = request.POST.get('id_document_type', 'Driving License').strip()
            id_number = request.POST.get('id_number', '').strip()
            document_file = request.POST.get('document_file', '').strip()

            if 'document_upload' in request.FILES:
                uploaded = request.FILES['document_upload']
                import os
                from django.conf import settings
                docs_dir = os.path.join(settings.BASE_DIR, 'media', 'user_documents')
                os.makedirs(docs_dir, exist_ok=True)
                file_path = os.path.join(docs_dir, f"user_{request.user.id}_{uploaded.name}")
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded.chunks():
                        destination.write(chunk)
                document_file = f"/media/user_documents/user_{request.user.id}_{uploaded.name}"

            if not id_number:
                error_msg = "Please enter a valid ID document number."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                messages.error(request, error_msg)
                return redirect('/accounts/user-panel/')

            user_profile.id_document_type = id_document_type
            user_profile.id_number = id_number
            if document_file:
                user_profile.document_file = document_file
            user_profile.verification_status = 'Pending'
            user_profile.rejection_reason = ''
            user_profile.save()

            success_msg = "Verification document submitted successfully! Admin will review and verify your account."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': success_msg,
                    'verification_status': user_profile.verification_status,
                    'id_document_type': user_profile.id_document_type,
                    'id_number': user_profile.id_number
                })
            messages.success(request, success_msg)
            return redirect('/accounts/user-panel/')

        else:
            fullname = request.POST.get('fullname', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip().lower()

            if fullname:
                request.user.first_name = fullname

            if email and email != request.user.email:
                if User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
                    error_msg = "This email is already registered to another account."
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                    messages.error(request, error_msg)
                    return redirect('/accounts/user-panel/')
                request.user.email = email

            request.user.save()

            if phone:
                user_profile.phone_number = phone
                user_profile.save()

            success_msg = "Profile details updated successfully!"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': success_msg,
                    'fullname': request.user.first_name or request.user.username,
                    'email': request.user.email,
                    'phone': user_profile.phone_number
                })
            messages.success(request, success_msg)
            return redirect('/accounts/user-panel/')

    # Real-time queries for logged-in user (Only Car and Bike vehicle bookings)
    user_inquiries = BookingInquiry.objects.filter(
        (Q(user=request.user) | Q(email__iexact=request.user.email)),
        category_type__in=['car', 'bike']
    ).distinct().order_by('-created_at')

    total_inquiries = user_inquiries.count()
    approved_inquiries = user_inquiries.filter(status='Approved').count()
    pending_inquiries = user_inquiries.filter(status='Pending').count()
    rejected_inquiries = user_inquiries.filter(Q(status='Rejected') | Q(status='Cancelled')).count()

    # Calculate Avatar Initials
    name_str = (request.user.first_name or request.user.username).strip()
    name_parts = name_str.split()
    if len(name_parts) >= 2:
        avatar_initials = f"{name_parts[0][0]}{name_parts[1][0]}".upper()
    else:
        avatar_initials = (name_str[:2] if len(name_str) >= 2 else "US").upper()

    context = {
        'user_profile': user_profile,
        'user_inquiries': user_inquiries,
        'total_inquiries': total_inquiries,
        'approved_inquiries': approved_inquiries,
        'pending_inquiries': pending_inquiries,
        'rejected_inquiries': rejected_inquiries,
        'avatar_initials': avatar_initials,
    }
    return render(request, 'user_accounts/user_panel.html', context)



def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not email:
            error_msg = "Please enter your registered email address."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'user_accounts/forgot_password.html')

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            error_msg = "No account found with this email address."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'user_accounts/forgot_password.html')

        # If user provides new password to reset directly
        if new_password:
            import re
            if len(new_password) < 6 or not re.search(r'[A-Za-z]', new_password) or not re.search(r'[0-9]', new_password):
                error_msg = "Password must be at least 6 characters and contain letters & numbers."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                messages.error(request, error_msg)
                return render(request, 'user_accounts/forgot_password.html')

            if new_password != confirm_password:
                error_msg = "Passwords do not match."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                messages.error(request, error_msg)
                return render(request, 'user_accounts/forgot_password.html')

            user.set_password(new_password)
            user.save()
            success_msg = "Password reset successfully! You can now login with your new password."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
                return JsonResponse({
                    'status': 'success',
                    'message': success_msg,
                    'redirect_url': '/accounts/login/'
                })
            messages.success(request, success_msg)
            return redirect('/accounts/login/')

        # If only email supplied, return reset instructions
        success_msg = f"Password reset link & temporary passcode sent to {user.email}."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'multipart/form-data':
            return JsonResponse({
                'status': 'success',
                'message': success_msg,
                'email': user.email
            })
        messages.success(request, success_msg)
        return render(request, 'user_accounts/forgot_password.html', {'email_sent': True, 'user_email': user.email})

    return render(request, 'user_accounts/forgot_password.html')

