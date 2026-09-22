import datetime
import json
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car, Bike, VehicleCategory
from booking_manager.models import BookingInquiry

def get_booked_dates_for_car(car_id=None, car_name=None):
    """
    Returns a set of 'YYYY-MM-DD' date strings on which a car is booked by active inquiries.
    """
    query = BookingInquiry.objects.filter(category_type='car').exclude(status='Cancelled')
    if car_id:
        query = query.filter(Q(item_id=car_id) | Q(item_title__icontains=car_name if car_name else ''))
    elif car_name:
        query = query.filter(item_title__icontains=car_name)

    booked_dates = set()
    for inquiry in query:
        s_date_str = inquiry.start_date
        e_date_str = inquiry.end_date

        if not s_date_str or not e_date_str:
            b_str = inquiry.booking_date or ''
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', b_str)
            if len(dates) >= 2:
                s_date_str, e_date_str = dates[0], dates[1]
            elif len(dates) == 1:
                s_date_str = e_date_str = dates[0]

        if s_date_str and e_date_str:
            try:
                start_dt = datetime.datetime.strptime(s_date_str, '%Y-%m-%d').date()
                end_dt = datetime.datetime.strptime(e_date_str, '%Y-%m-%d').date()
                curr = start_dt
                while curr <= end_dt:
                    booked_dates.add(curr.strftime('%Y-%m-%d'))
                    curr += datetime.timedelta(days=1)
            except Exception:
                pass
    return booked_dates

def carrent_page(request):
    category = request.GET.get('category', 'all').strip().lower()
    search_q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    page_number = request.GET.get('page', 1)

    cars_queryset = Car.objects.all()

    if category and category != 'all':
        cars_queryset = cars_queryset.filter(category__icontains=category)

    if search_q:
        cars_queryset = cars_queryset.filter(Q(name__icontains=search_q) | Q(category__icontains=search_q))

    if location:
        cars_queryset = cars_queryset.filter(Q(location_name__icontains=location) | Q(description__icontains=location))

    # Parse requested travel date range if provided
    requested_dates = set()
    if start_date and end_date:
        try:
            s_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            e_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            curr = s_dt
            while curr <= e_dt:
                requested_dates.add(curr.strftime('%Y-%m-%d'))
                curr += datetime.timedelta(days=1)
        except Exception:
            pass

    cars = list(cars_queryset)
    booked_cars_info = []

    for car in cars:
        car_booked = get_booked_dates_for_car(car.id, car.name)
        overlap = requested_dates.intersection(car_booked) if requested_dates else set()
        if overlap:
            car.is_booked_by_other = True
            car.booked_overlap_dates = sorted(list(overlap))
            booked_cars_info.append({
                'id': car.id,
                'name': car.name,
                'dates': sorted(list(overlap))
            })
        else:
            car.is_booked_by_other = False
            car.booked_overlap_dates = []

    # Display all cars matching filters so users can view full fleet, with booked cars marked read-only
    paginator = Paginator(cars, 10)
    cars_page = paginator.get_page(page_number)

    # Fetch categories dynamically from database for currently available items only
    db_categories = list(Car.objects.filter(status='Available').exclude(category='').values_list('category', flat=True).distinct())
    categories = sorted(list(set([c.strip() for c in db_categories if c and c.strip()])))

    # Fetch locations dynamically from Car database
    db_locations = list(Car.objects.exclude(location_name='').values_list('location_name', flat=True).distinct())
    locations = sorted(list(set([l.strip() for l in db_locations if l and l.strip()])))
    if not locations:
        locations = ['Bhavnagar Central Hub', 'Mumbai Central Hub', 'Delhi Airport Terminal 3', 'Bhavnagar Station Road', 'Bangalore Indiranagar Hub', 'Ahmedabad SG Highway']

    context = {
        'cars': cars_page,
        'cars_count': len(cars),
        'booked_count': len(booked_cars_info),
        'categories': categories,
        'locations': locations,
        'selected_category': category,
        'selected_location': location,
        'search_q': search_q,
        'start_date': start_date,
        'end_date': end_date,
        'booked_cars_info': booked_cars_info,
        'has_booked_cars': len(booked_cars_info) > 0 and len(requested_dates) > 0,
    }
    return render(request, 'vehicle_rentals/carrent.html', context)


def car_details_page(request):
    car_id = request.GET.get('id', '1')
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    location = request.GET.get('location', '').strip()

    car = None
    if str(car_id).isdigit():
        car = Car.objects.filter(pk=int(car_id)).first()

    if not car:
        car = Car.objects.first()

    # Parse features into individual items list
    features_list = []
    if car and car.features:
        raw_feats = car.features.replace('\n', ',').split(',')
        features_list = [f.strip() for f in raw_feats if f and f.strip()]

    # Extract all booked dates for this car
    booked_dates_set = get_booked_dates_for_car(car.id if car else None, car.name if car else None)
    booked_dates_list = sorted(list(booked_dates_set))
    booked_dates_json = json.dumps(booked_dates_list)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            next_url = f"/vehicles/car-details/?id={car.id if car else 1}"
            if start_date:
                next_url += f"&start_date={start_date}"
            if end_date:
                next_url += f"&end_date={end_date}"
            if location:
                next_url += f"&location={location}"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'require_login': True,
                    'login_url': f"/accounts/login/?next={next_url}",
                    'message': 'Please login to book a car!'
                }, status=401)
            messages.warning(request, 'Please log in to your account before placing a car booking.')
            return redirect(f"/accounts/login/?next={next_url}")

        # Check date availability on server side before saving
        pickup_date = request.POST.get('pickup_date', start_date)
        return_date = request.POST.get('return_date', end_date)
        
        req_dates = set()
        if pickup_date and return_date:
            try:
                s_dt = datetime.datetime.strptime(pickup_date, '%Y-%m-%d').date()
                e_dt = datetime.datetime.strptime(return_date, '%Y-%m-%d').date()
                curr = s_dt
                while curr <= e_dt:
                    req_dates.add(curr.strftime('%Y-%m-%d'))
                    curr += datetime.timedelta(days=1)
            except Exception:
                pass

        if req_dates.intersection(booked_dates_set):
            conflict_dates = ", ".join(sorted(list(req_dates.intersection(booked_dates_set))))
            err_msg = f"Sorry! This car is already booked by another customer on: {conflict_dates}. Please select available dates."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': err_msg}, status=400)
            messages.error(request, err_msg)
            return redirect(f"/vehicles/car-details/?id={car.id if car else 1}&start_date={start_date}&end_date={end_date}&location={location}")

        # Enforce user details from request.user for logged-in users
        full_name = request.user.get_full_name() or request.user.username
        email = request.user.email
        user_profile = getattr(request.user, 'profile', None)
        phone = (getattr(user_profile, 'phone_number', '') if user_profile else '') or request.POST.get('phone', '').strip()

        pickup_location = request.POST.get('pickup_location', location or 'Bhavnagar Central Hub')
        total_amount = request.POST.get('total_amount', '0')
        vehicle_name = request.POST.get('vehicle_name', car.name if car else 'Car Rental')

        inquiry = BookingInquiry.objects.create(
            user=request.user,
            category_type='car',
            item_title=vehicle_name,
            item_id=car.id if car else 1,
            applicant_name=full_name,
            phone_number=phone,
            email=email,
            start_date=pickup_date,
            end_date=return_date,
            booking_date=f"{pickup_date} to {return_date}" if (pickup_date and return_date) else "Flexible Date",
            appointment_time=pickup_location,
            guests_or_km=f"Total: ₹{total_amount}",
            payment_method='Pending Selection',
            payment_status='Pending',
            status='Pending'
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Booking details saved! Proceeding to payment...',
                'redirect_url': f'/bookings/payment/?inquiry_id={inquiry.id}'
            })

    # Fetch reviews & ratings submitted by customers for this car
    reviews_qs = BookingInquiry.objects.filter(category_type='feedback').filter(
        Q(item_id=car.id) | Q(item_title__icontains=car.name)
    ).order_by('-created_at')

    reviews = []
    ratings_sum = 0
    for r in reviews_qs:
        try:
            r_val = float(re.findall(r'\d+\.?\d*', r.guests_or_km or r.hours_needed or '5.0')[0])
        except Exception:
            r_val = 5.0
        ratings_sum += r_val
        reviews.append({
            'user_name': r.applicant_name or (r.user.get_full_name() if r.user else 'Verified Customer'),
            'rating': r_val,
            'stars': int(round(r_val)),
            'comment': r.special_requirements or 'Great vehicle condition and smooth rental experience!',
            'date': r.created_at.strftime('%b %d, %Y') if r.created_at else 'Recent'
        })

    avg_rating = round(ratings_sum / len(reviews), 1) if reviews else float(car.rating)
    if reviews:
        car.rating = avg_rating
        car.save()

    context = {
        'car': car,
        'features_list': features_list,
        'start_date': start_date,
        'end_date': end_date,
        'location': location,
        'booked_dates': booked_dates_list,
        'booked_dates_json': booked_dates_json,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'reviews_count': len(reviews),
    }
    return render(request, 'vehicle_rentals/car_details.html', context)


def get_booked_dates_for_bike(bike_id=None, bike_name=None):
    """
    Returns a set of 'YYYY-MM-DD' date strings on which a bike is booked by active inquiries.
    """
    query = BookingInquiry.objects.filter(category_type='bike').exclude(status='Cancelled')
    if bike_id:
        query = query.filter(Q(item_id=bike_id) | Q(item_title__icontains=bike_name if bike_name else ''))
    elif bike_name:
        query = query.filter(item_title__icontains=bike_name)

    booked_dates = set()
    for inquiry in query:
        s_date_str = inquiry.start_date
        e_date_str = inquiry.end_date

        if not s_date_str or not e_date_str:
            b_str = inquiry.booking_date or ''
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', b_str)
            if len(dates) >= 2:
                s_date_str, e_date_str = dates[0], dates[1]
            elif len(dates) == 1:
                s_date_str = e_date_str = dates[0]

        if s_date_str and e_date_str:
            try:
                start_dt = datetime.datetime.strptime(s_date_str, '%Y-%m-%d').date()
                end_dt = datetime.datetime.strptime(e_date_str, '%Y-%m-%d').date()
                curr = start_dt
                while curr <= end_dt:
                    booked_dates.add(curr.strftime('%Y-%m-%d'))
                    curr += datetime.timedelta(days=1)
            except Exception:
                pass
    return booked_dates


def bikerent_page(request):
    category = request.GET.get('category', 'all').strip().lower()
    search_q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    page_number = request.GET.get('page', 1)

    bikes_queryset = Bike.objects.all()

    if category and category != 'all':
        bikes_queryset = bikes_queryset.filter(category__icontains=category)

    if search_q:
        bikes_queryset = bikes_queryset.filter(Q(name__icontains=search_q) | Q(category__icontains=search_q))

    if location:
        bikes_queryset = bikes_queryset.filter(Q(location_name__icontains=location) | Q(description__icontains=location))

    # Parse requested travel date range if provided
    requested_dates = set()
    if start_date and end_date:
        try:
            s_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            e_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            curr = s_dt
            while curr <= e_dt:
                requested_dates.add(curr.strftime('%Y-%m-%d'))
                curr += datetime.timedelta(days=1)
        except Exception:
            pass

    bikes = list(bikes_queryset)
    booked_bikes_info = []

    for bike in bikes:
        bike_booked = get_booked_dates_for_bike(bike.id, bike.name)
        overlap = requested_dates.intersection(bike_booked) if requested_dates else set()
        if overlap:
            bike.is_booked_by_other = True
            bike.booked_overlap_dates = sorted(list(overlap))
            booked_bikes_info.append({
                'id': bike.id,
                'name': bike.name,
                'dates': sorted(list(overlap))
            })
        else:
            bike.is_booked_by_other = False
            bike.booked_overlap_dates = []

    # Display all bikes in fleet with booked status marked
    paginator = Paginator(bikes, 10)
    bikes_page = paginator.get_page(page_number)

    # Fetch categories dynamically from database (both bike items and VehicleCategory model)
    db_categories = list(Bike.objects.values_list('category', flat=True).distinct())
    custom_categories = list(VehicleCategory.objects.filter(vehicle_type='bike').values_list('name', flat=True))
    categories = sorted(list(set([c.strip() for c in (db_categories + custom_categories) if c and c.strip()])))

    # Fetch locations dynamically from Bike database
    db_locations = list(Bike.objects.exclude(location_name='').values_list('location_name', flat=True).distinct())
    locations = sorted(list(set([l.strip() for l in db_locations if l and l.strip()])))
    if not locations:
        locations = ['Bhavnagar Station Road', 'Mumbai Central Hub', 'Ahmedabad SG Highway', 'Bangalore Indiranagar Hub']

    context = {
        'bikes': bikes_page,
        'bikes_count': len(bikes),
        'booked_count': len(booked_bikes_info),
        'categories': categories,
        'locations': locations,
        'selected_category': category,
        'selected_location': location,
        'search_q': search_q,
        'start_date': start_date,
        'end_date': end_date,
        'booked_bikes_info': booked_bikes_info,
        'has_booked_bikes': len(booked_bikes_info) > 0 and len(requested_dates) > 0,
    }
    return render(request, 'vehicle_rentals/bikerent.html', context)


def bike_details_page(request):
    bike_id = request.GET.get('id', '1')
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    location = request.GET.get('location', '').strip()

    bike = None
    if str(bike_id).isdigit():
        bike = Bike.objects.filter(pk=int(bike_id)).first()

    if not bike:
        bike = Bike.objects.first()

    # Parse features into individual items list
    features_list = []
    if bike and bike.features:
        raw_feats = bike.features.replace('\n', ',').split(',')
        features_list = [f.strip() for f in raw_feats if f and f.strip()]

    # Extract all booked dates for this bike
    booked_dates_set = get_booked_dates_for_bike(bike.id if bike else None, bike.name if bike else None)
    booked_dates_list = sorted(list(booked_dates_set))
    booked_dates_json = json.dumps(booked_dates_list)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            next_url = f"/vehicles/bike-details/?id={bike.id if bike else 1}"
            if start_date:
                next_url += f"&start_date={start_date}"
            if end_date:
                next_url += f"&end_date={end_date}"
            if location:
                next_url += f"&location={location}"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'require_login': True,
                    'login_url': f"/accounts/login/?next={next_url}",
                    'message': 'Please login to book a bike!'
                }, status=401)
            messages.warning(request, 'Please log in to your account before placing a bike booking.')
            return redirect(f"/accounts/login/?next={next_url}")

        # Check date availability on server side before saving
        pickup_date = request.POST.get('pickup_date', start_date)
        return_date = request.POST.get('return_date', end_date)
        
        req_dates = set()
        if pickup_date and return_date:
            try:
                s_dt = datetime.datetime.strptime(pickup_date, '%Y-%m-%d').date()
                e_dt = datetime.datetime.strptime(return_date, '%Y-%m-%d').date()
                curr = s_dt
                while curr <= e_dt:
                    req_dates.add(curr.strftime('%Y-%m-%d'))
                    curr += datetime.timedelta(days=1)
            except Exception:
                pass

        if req_dates.intersection(booked_dates_set):
            conflict_dates = ", ".join(sorted(list(req_dates.intersection(booked_dates_set))))
            err_msg = f"Sorry! This bike is already booked by another customer on: {conflict_dates}. Please select available dates."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': err_msg}, status=400)
            messages.error(request, err_msg)
            return redirect(f"/vehicles/bike-details/?id={bike.id if bike else 1}&start_date={start_date}&end_date={end_date}&location={location}")

        # Enforce user details from request.user for logged-in users
        full_name = request.user.get_full_name() or request.user.username
        email = request.user.email
        user_profile = getattr(request.user, 'profile', None)
        phone = (getattr(user_profile, 'phone_number', '') if user_profile else '') or request.POST.get('phone', '').strip()

        pickup_location = request.POST.get('pickup_location', location or 'Bhavnagar Station Road')
        total_amount = request.POST.get('total_amount', '0')
        bike_name = request.POST.get('bike_name', bike.name if bike else 'Bike Rental')

        inquiry = BookingInquiry.objects.create(
            user=request.user,
            category_type='bike',
            item_title=bike_name,
            item_id=bike.id if bike else 1,
            applicant_name=full_name,
            phone_number=phone,
            email=email,
            start_date=pickup_date,
            end_date=return_date,
            booking_date=f"{pickup_date} to {return_date}" if (pickup_date and return_date) else "Flexible Date",
            appointment_time=pickup_location,
            guests_or_km=f"Total: ₹{total_amount}",
            payment_method='Pending Selection',
            payment_status='Pending',
            status='Pending'
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Bike rental inquiry submitted! Proceeding to payment...',
                'redirect_url': f'/bookings/payment/?inquiry_id={inquiry.id}'
            })

    # Fetch reviews & ratings submitted by customers for this bike
    reviews_qs = BookingInquiry.objects.filter(category_type='feedback').filter(
        Q(item_id=bike.id) | Q(item_title__icontains=bike.name)
    ).order_by('-created_at')

    reviews = []
    ratings_sum = 0
    for r in reviews_qs:
        try:
            r_val = float(re.findall(r'\d+\.?\d*', r.guests_or_km or r.hours_needed or '5.0')[0])
        except Exception:
            r_val = 5.0
        ratings_sum += r_val
        reviews.append({
            'user_name': r.applicant_name or (r.user.get_full_name() if r.user else 'Verified Rider'),
            'rating': r_val,
            'stars': int(round(r_val)),
            'comment': r.special_requirements or 'Great bike performance and smooth ride!',
            'date': r.created_at.strftime('%b %d, %Y') if r.created_at else 'Recent'
        })

    avg_rating = round(ratings_sum / len(reviews), 1) if reviews else float(bike.rating)
    if reviews:
        bike.rating = avg_rating
        bike.save()

    context = {
        'bike': bike,
        'features_list': features_list,
        'start_date': start_date,
        'end_date': end_date,
        'location': location,
        'booked_dates': booked_dates_list,
        'booked_dates_json': booked_dates_json,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'reviews_count': len(reviews),
    }
    return render(request, 'vehicle_rentals/bike_details.html', context)


def jawa_page(request):
    return bike_details_page(request)


def manage_categories_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        vehicle_type = request.POST.get('vehicle_type', 'car').strip().lower()
        description = request.POST.get('description', '').strip()

        if name:
            obj, created = VehicleCategory.objects.get_or_create(
                name=name,
                vehicle_type=vehicle_type,
                defaults={'description': description}
            )
            if created:
                messages.success(request, f"New category '{name}' for {vehicle_type.upper()} added successfully!")
            else:
                messages.info(request, f"Category '{name}' already exists.")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f"Category '{name}' added successfully!"})

            return redirect('/vehicles/manage-categories/')

    car_categories = VehicleCategory.objects.filter(vehicle_type='car').order_by('-created_at')
    bike_categories = VehicleCategory.objects.filter(vehicle_type='bike').order_by('-created_at')

    # Also extract distinct categories from existing vehicles
    existing_car_cats = set(Car.objects.values_list('category', flat=True).distinct())
    existing_bike_cats = set(Bike.objects.values_list('category', flat=True).distinct())

    context = {
        'car_categories': car_categories,
        'bike_categories': bike_categories,
        'existing_car_cats': sorted(list(existing_car_cats)),
        'existing_bike_cats': sorted(list(existing_bike_cats)),
    }
    return render(request, 'vehicle_rentals/manage_categories.html', context)


def delete_category_api(request):
    if request.method == 'POST':
        cat_id = request.POST.get('id')
        if cat_id and str(cat_id).isdigit():
            VehicleCategory.objects.filter(pk=int(cat_id)).delete()
            return JsonResponse({'status': 'success', 'message': 'Category deleted successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid category deletion request.'}, status=400)

