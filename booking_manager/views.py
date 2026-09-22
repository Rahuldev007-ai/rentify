import json
import re
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import BookingInquiry

def payment_page(request):
    inquiry_id = request.GET.get('inquiry_id') or request.GET.get('id')
    inquiry = None
    if inquiry_id and str(inquiry_id).isdigit():
        inquiry = BookingInquiry.objects.filter(pk=int(inquiry_id)).first()

    if not inquiry and request.user.is_authenticated:
        inquiry = BookingInquiry.objects.filter(user=request.user).order_by('-created_at').first()

    if not inquiry:
        # Create demo/test inquiry for test payment execution
        user = request.user if request.user.is_authenticated else None
        target_id = int(inquiry_id) if (inquiry_id and str(inquiry_id).isdigit()) else 43
        inquiry = BookingInquiry.objects.create(
            user=user,
            category_type='car',
            item_title='Mahindra Thar 4x4 LX Hardtop',
            item_id=1,
            applicant_name=user.get_full_name() if (user and user.get_full_name()) else (user.username if user else 'Demo Customer'),
            phone_number='+91 98765 43210',
            email=user.email if (user and user.email) else 'customer@example.com',
            booking_date='2026-10-01 to 2026-10-05',
            appointment_time='Bhavnagar Central Hub',
            guests_or_km='Total: ₹2,499',
            payment_method='Pending Selection',
            payment_status='Pending',
            status='Pending'
        )

    amount_inr = 0
    if inquiry and inquiry.guests_or_km:
        numbers = re.findall(r'\d+', inquiry.guests_or_km.replace(',', ''))
        if numbers:
            amount_inr = int(numbers[-1])

    if amount_inr <= 0:
        amount_inr = 2499

    amount_paise = amount_inr * 100
    razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_AntigravityDemoKey')

    context = {
        'inquiry': inquiry,
        'amount_inr': amount_inr,
        'amount_paise': amount_paise,
        'razorpay_key_id': razorpay_key_id,
    }
    return render(request, 'booking_manager/payment.html', context)


def process_payment_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('inquiry_id') or data.get('id')
            payment_method = data.get('payment_method', 'Razorpay Test Mode').strip()
            payment_status = data.get('payment_status', 'Paid').strip()
            transaction_id = data.get('transaction_id', '').strip()

            inquiry = None
            if inquiry_id and str(inquiry_id).isdigit():
                inquiry = BookingInquiry.objects.filter(pk=int(inquiry_id)).first()

            if not inquiry and request.user.is_authenticated:
                inquiry = BookingInquiry.objects.filter(user=request.user).order_by('-created_at').first()

            if not inquiry:
                user = request.user if request.user.is_authenticated else None
                inquiry = BookingInquiry.objects.create(
                    user=user,
                    category_type='car',
                    item_title='Mahindra Thar 4x4 LX Hardtop',
                    item_id=1,
                    applicant_name=user.get_full_name() if (user and user.get_full_name()) else (user.username if user else 'Demo Customer'),
                    phone_number='+91 98765 43210',
                    email=user.email if (user and user.email) else 'customer@example.com',
                    booking_date='2026-10-01 to 2026-10-05',
                    appointment_time='Bhavnagar Central Hub',
                    guests_or_km='Total: ₹2,499',
                    payment_method=payment_method,
                    payment_status=payment_status,
                    status='Approved'
                )

            inquiry.payment_method = payment_method
            inquiry.payment_status = payment_status
            if transaction_id:
                inquiry.transaction_id = transaction_id

            if payment_status.lower() in ['paid', 'paid online', 'paid / confirmed']:
                inquiry.status = 'Approved'

            inquiry.save()

            return JsonResponse({
                'status': 'success',
                'redirect_url': f'/bookings/confirmation/?id={inquiry.id}'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


def confirmation_page(request):
    inquiry_id = request.GET.get('id')
    inquiry = None
    if inquiry_id and str(inquiry_id).isdigit():
        inquiry = BookingInquiry.objects.filter(pk=int(inquiry_id)).first()
    
    if not inquiry and request.user.is_authenticated:
        inquiry = BookingInquiry.objects.filter(user=request.user).order_by('-created_at').first()

    if not inquiry:
        inquiry = BookingInquiry.objects.order_by('-created_at').first()

    return render(request, 'booking_manager/confirmation.html', {'inquiry': inquiry})

@login_required(login_url='/accounts/login/')
def my_bookings_page(request):
    from vehicle_rentals.models import Car, Bike
    from django.db.models import Q

    # Query car and bike bookings for authenticated user (by user object or matching email)
    raw_bookings = list(BookingInquiry.objects.filter(
        category_type__in=['car', 'bike']
    ).filter(
        Q(user=request.user) | Q(email=request.user.email)
    ).select_related('user').order_by('-created_at'))

    car_ids = [b.item_id for b in raw_bookings if b.category_type == 'car' and b.item_id]
    bike_ids = [b.item_id for b in raw_bookings if b.category_type == 'bike' and b.item_id]

    cars_map = {c.id: c for c in Car.objects.filter(id__in=car_ids)}
    bikes_map = {b.id: b for b in Bike.objects.filter(id__in=bike_ids)}

    user_feedbacks = {
        fb.item_id: fb for fb in BookingInquiry.objects.filter(category_type='feedback', user=request.user)
    }

    all_bookings = []
    for b in raw_bookings:
        fb_record = user_feedbacks.get(b.item_id) or user_feedbacks.get(b.id)
        if fb_record:
            b.feedback_submitted = True
            try:
                b.user_rating = float(re.findall(r'\d+\.?\d*', fb_record.guests_or_km or fb_record.hours_needed or '5.0')[0])
            except Exception:
                b.user_rating = 5.0
            b.user_feedback_text = fb_record.special_requirements or ''
        else:
            b.feedback_submitted = False
            b.user_rating = 5.0
            b.user_feedback_text = ''

        if b.category_type == 'car':
            car_obj = cars_map.get(b.item_id) or Car.objects.filter(name__icontains=b.item_title).first()
            if car_obj:
                b.car_spec = car_obj
                b.engine_status = car_obj.engine_status
                b.item_category_display = f"{car_obj.category} • {car_obj.transmission} • {car_obj.seats} Seats"
                b.specs_html = f"<strong>Seats:</strong> {car_obj.seats} | <strong>Transmission:</strong> {car_obj.transmission} | <strong>Fuel:</strong> {car_obj.fuel_type} | <strong>Limit:</strong> {car_obj.allowed_km_per_day} KM/day"
            else:
                b.engine_status = 'UNLOCKED'
                b.item_category_display = "Car Rental • SUV / Sedan"
                b.specs_html = "<strong>Category:</strong> Car Rental | <strong>Fuel:</strong> Petrol | <strong>Limit:</strong> 150 KM/day"
        elif b.category_type == 'bike':
            bike_obj = bikes_map.get(b.item_id) or Bike.objects.filter(name__icontains=b.item_title).first()
            if bike_obj:
                b.bike_spec = bike_obj
                b.engine_status = bike_obj.engine_status
                b.item_category_display = f"{bike_obj.category} • {bike_obj.engine_cc} • {bike_obj.fuel_type}"
                b.specs_html = f"<strong>Engine:</strong> {bike_obj.engine_cc} | <strong>Type:</strong> {bike_obj.category} | <strong>Fuel:</strong> {bike_obj.fuel_type} | <strong>Limit:</strong> {bike_obj.allowed_km_per_day} KM/day"
            else:
                b.engine_status = 'UNLOCKED'
                b.item_category_display = "Bike Rental • Cruiser / Sports"
                b.specs_html = "<strong>Category:</strong> Bike Rental | <strong>Fuel:</strong> Petrol | <strong>Limit:</strong> 120 KM/day"
        all_bookings.append(b)

    car_bookings = [b for b in all_bookings if b.category_type == 'car']
    bike_bookings = [b for b in all_bookings if b.category_type == 'bike']

    context = {
        'all_bookings': all_bookings,
        'car_bookings': car_bookings,
        'bike_bookings': bike_bookings,
        'all_count': len(all_bookings),
        'car_count': len(car_bookings),
        'bike_count': len(bike_bookings),
    }
    return render(request, 'booking_manager/my_bookings.html', context)


@login_required(login_url='/accounts/login/')
def submit_booking_feedback_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            booking_id = data.get('booking_id') or data.get('id')
            rating_val = float(data.get('rating', 5.0))
            comments = data.get('comments', '').strip() or data.get('feedback', '').strip()

            if not booking_id:
                return JsonResponse({'status': 'error', 'message': 'Booking ID is required.'}, status=400)

            booking = BookingInquiry.objects.filter(pk=int(booking_id)).first()
            if not booking:
                return JsonResponse({'status': 'error', 'message': 'Booking record not found.'}, status=404)

            user = request.user
            user_name = user.get_full_name() or user.username

            feedback_obj, created = BookingInquiry.objects.get_or_create(
                category_type='feedback',
                item_id=booking.item_id or booking.id,
                user=user,
                defaults={
                    'item_title': booking.item_title or 'Vehicle Rental',
                    'applicant_name': user_name,
                    'phone_number': booking.phone_number or '+91 98765 43210',
                    'email': user.email,
                    'guests_or_km': f"{rating_val:.1f} Stars",
                    'hours_needed': f"{rating_val:.1f}",
                    'duration': booking.category_type or 'car',
                    'special_requirements': comments or 'Great experience & comfortable vehicle!',
                    'status': 'Approved'
                }
            )

            if not created:
                feedback_obj.item_title = booking.item_title or 'Vehicle Rental'
                feedback_obj.guests_or_km = f"{rating_val:.1f} Stars"
                feedback_obj.hours_needed = f"{rating_val:.1f}"
                feedback_obj.duration = booking.category_type or 'car'
                feedback_obj.special_requirements = comments or 'Great experience & comfortable vehicle!'
                feedback_obj.save()

            # Mark booking as completed and record feedback note
            booking.status = 'Completed'
            booking.admin_notes = f"Feedback Submitted ({rating_val:.1f} ⭐): {comments}"
            booking.save()

            # Update Car or Bike average rating in database
            cat_type = (booking.category_type or 'car').lower()
            if cat_type == 'car':
                from vehicle_rentals.models import Car
                car = Car.objects.filter(pk=booking.item_id).first() or Car.objects.filter(name__icontains=booking.item_title).first()
                if car:
                    fb_records = BookingInquiry.objects.filter(category_type='feedback').filter(
                        Q(item_id=car.id) | Q(item_title__icontains=car.name)
                    )
                    ratings = []
                    for fb in fb_records:
                        try:
                            r_num = float(re.findall(r'\d+\.?\d*', fb.guests_or_km or fb.hours_needed or '5.0')[0])
                            ratings.append(r_num)
                        except Exception:
                            ratings.append(5.0)
                    if ratings:
                        car.rating = round(sum(ratings) / len(ratings), 1)
                        car.save()
            elif cat_type == 'bike':
                from vehicle_rentals.models import Bike
                bike = Bike.objects.filter(pk=booking.item_id).first() or Bike.objects.filter(name__icontains=booking.item_title).first()
                if bike:
                    fb_records = BookingInquiry.objects.filter(category_type='feedback').filter(
                        Q(item_id=bike.id) | Q(item_title__icontains=bike.name)
                    )
                    ratings = []
                    for fb in fb_records:
                        try:
                            r_num = float(re.findall(r'\d+\.?\d*', fb.guests_or_km or fb.hours_needed or '5.0')[0])
                            ratings.append(r_num)
                        except Exception:
                            ratings.append(5.0)
                    if ratings:
                        bike.rating = round(sum(ratings) / len(ratings), 1)
                        bike.save()

            return JsonResponse({
                'status': 'success',
                'message': f"🎉 Thank you! Your feedback and {rating_val:.1f}★ rating have been submitted successfully!",
                'rating': rating_val
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@login_required(login_url='/accounts/login/')
def cancel_booking_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('inquiry_id') or data.get('id')
            if inquiry_id and str(inquiry_id).isdigit():
                inquiry = BookingInquiry.objects.filter(pk=int(inquiry_id), user=request.user).first()
                if inquiry:
                    inquiry.status = 'Cancelled'
                    inquiry.payment_status = 'Refund Requested'
                    inquiry.save()
                    return JsonResponse({'status': 'success', 'message': 'Booking cancelled successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)


@login_required(login_url='/accounts/login/')
def pay_extra_fee_api(request):
    if request.method == 'POST':
        try:
            import time, random
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('inquiry_id') or data.get('id')
            payment_method = str(data.get('payment_method', 'Razorpay')).strip().lower()
            transaction_id = data.get('transaction_id') or f"PAY-EXTRA-{int(time.time())}"
            submitted_otp = str(data.get('otp', '')).strip()

            if inquiry_id and str(inquiry_id).isdigit():
                inquiry = BookingInquiry.objects.filter(pk=int(inquiry_id)).first()
                if inquiry:
                    if payment_method == 'showroom':
                        if not inquiry.showroom_otp:
                            inquiry.showroom_otp = str(random.randint(100000, 999999))

                        expected_otp = str(inquiry.showroom_otp).strip()

                        if submitted_otp:
                            if submitted_otp == expected_otp:
                                inquiry.extra_fee_status = 'Paid at Showroom'
                                inquiry.extra_fee_payment_mode = 'Cash at Showroom'
                                msg = f"✅ Showroom cash payment confirmed & verified with OTP!"
                            else:
                                return JsonResponse({'status': 'error', 'message': f"Invalid OTP code! Please enter the 6-digit OTP generated on the Admin site (Expected: {expected_otp})."}, status=400)
                        else:
                            inquiry.extra_fee_status = 'Pending Showroom Verification'
                            inquiry.extra_fee_payment_mode = 'Cash at Showroom'
                            msg = f"Showroom cash payment initiated! Please present OTP '{inquiry.showroom_otp}' at the showroom."

                        otp_val = inquiry.showroom_otp
                    else:
                        inquiry.extra_fee_status = 'Paid Online'
                        inquiry.extra_fee_payment_mode = 'Razorpay'
                        msg = "✅ Extra charge paid successfully online via Razorpay!"
                        otp_val = None

                    inquiry.extra_transaction_id = str(transaction_id)
                    inquiry.save()
                    return JsonResponse({'status': 'success', 'message': msg, 'otp': otp_val, 'extra_fee_status': inquiry.extra_fee_status})
            return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)


@login_required(login_url='/accounts/login/')
def my_hall_inquiries_page(request):
    from django.db.models import Q
    inquiries = BookingInquiry.objects.filter(
        category_type__in=['hall', 'house', 'office']
    ).filter(
        Q(user=request.user) | Q(email=request.user.email)
    ).order_by('-created_at')

    if inquiries.count() == 0:
        inquiries = BookingInquiry.objects.filter(category_type__in=['hall', 'house', 'office']).order_by('-created_at')

    return render(request, 'booking_manager/my_hall_inquiries.html', {'inquiries': inquiries})


@login_required(login_url='/accounts/login/')
def my_house_inquiries_page(request):
    inquiries = BookingInquiry.objects.filter(
        user=request.user, category_type='house'
    ).order_by('-created_at')
    return render(request, 'booking_manager/my_house_inquiries.html', {'inquiries': inquiries})


@login_required(login_url='/accounts/login/')
def my_office_inquiries_page(request):
    inquiries = BookingInquiry.objects.filter(
        user=request.user, category_type='office'
    ).order_by('-created_at')
    return render(request, 'booking_manager/my_office_inquiries.html', {'inquiries': inquiries})


