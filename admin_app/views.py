import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from vehicle_rentals.models import Car, Bike, VehicleCategory, VehicleFeature

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'))

def admin_login_page(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('/admin-portal/dashboard/')
    return redirect('/accounts/login/')

def get_dashboard_analytics_payload():
    from vehicle_rentals.models import Car, Bike
    from property_rentals.models import EventHall, CommercialOffice, House
    from booking_manager.models import BookingInquiry
    from django.utils import timezone
    import datetime, re

    total_cars = Car.objects.count()
    total_bikes = Bike.objects.count()
    total_halls = EventHall.objects.count()
    total_offices = CommercialOffice.objects.count()
    total_houses = House.objects.count()

    total_inventory = total_cars + total_bikes + total_halls + total_offices + total_houses

    inquiries = BookingInquiry.objects.all().order_by('-id')
    total_bookings = inquiries.count()
    pending_bookings = inquiries.filter(status='Pending').count()
    approved_bookings = inquiries.filter(status__in=['Approved', 'Confirmed']).count()
    rejected_bookings = inquiries.filter(status__in=['Rejected', 'Cancelled']).count()

    cat_car = inquiries.filter(category_type='car').count()
    cat_bike = inquiries.filter(category_type='bike').count()
    cat_hall = inquiries.filter(category_type='hall').count()
    cat_office = inquiries.filter(category_type='office').count()
    cat_house = inquiries.filter(category_type='house').count()

    def extract_inquiry_price(inq):
        if inq.quoted_price and inq.quoted_price > 0:
            return float(inq.quoted_price)
        if inq.guests_or_km and 'Total: ₹' in inq.guests_or_km:
            match = re.search(r'Total:\s*₹\s*([0-9,]+)', inq.guests_or_km)
            if match:
                return float(match.group(1).replace(',', ''))
        defaults = {'car': 2500, 'bike': 500, 'hall': 45000, 'office': 75000, 'house': 35000}
        return float(defaults.get(inq.category_type, 2000))

    total_gross_revenue = sum(extract_inquiry_price(i) for i in inquiries)

    rev_car = sum(extract_inquiry_price(i) for i in inquiries if i.category_type == 'car')
    rev_bike = sum(extract_inquiry_price(i) for i in inquiries if i.category_type == 'bike')
    rev_hall = sum(extract_inquiry_price(i) for i in inquiries if i.category_type == 'hall')
    rev_office = sum(extract_inquiry_price(i) for i in inquiries if i.category_type == 'office')
    rev_house = sum(extract_inquiry_price(i) for i in inquiries if i.category_type == 'house')

    now = timezone.now()

    # 1 Day (Past 24 Hours split into 6 4-hour intervals)
    day_labels = ['00:00-04:00', '04:00-08:00', '08:00-12:00', '12:00-16:00', '16:00-20:00', '20:00-24:00']
    day_data = [0.0] * 6
    day_start = now - datetime.timedelta(hours=24)
    day_inquiries = inquiries.filter(created_at__gte=day_start)
    for inq in day_inquiries:
        if inq.created_at:
            hr = inq.created_at.hour
            slot = min(hr // 4, 5)
            day_data[slot] += extract_inquiry_price(inq)

    # 1 Week (Past 7 Days daily breakdown)
    week_labels = []
    week_data = []
    for d in range(6, -1, -1):
        target_day = (now - datetime.timedelta(days=d)).date()
        week_labels.append(target_day.strftime('%a (%b %d)'))
        sum_rev = sum(extract_inquiry_price(i) for i in inquiries if i.created_at and i.created_at.date() == target_day)
        week_data.append(sum_rev)

    # 1 Month (Past 30 Days split into 4 weeks)
    month_labels = ['Week 1 (Past 7d)', 'Week 2 (8-14d)', 'Week 3 (15-21d)', 'Week 4 (22-30d)']
    month_data = [0.0, 0.0, 0.0, 0.0]
    for inq in inquiries:
        if inq.created_at:
            delta_days = (now - inq.created_at).days
            if 0 <= delta_days <= 7:
                month_data[0] += extract_inquiry_price(inq)
            elif 8 <= delta_days <= 14:
                month_data[1] += extract_inquiry_price(inq)
            elif 15 <= delta_days <= 21:
                month_data[2] += extract_inquiry_price(inq)
            elif 22 <= delta_days <= 30:
                month_data[3] += extract_inquiry_price(inq)

    recent_activity = []
    for i in inquiries[:8]:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        amount = extract_inquiry_price(i)
        recent_activity.append({
            'id': i.id,
            'title': i.item_title or 'Booking Request',
            'category': i.category_type.capitalize() if i.category_type else 'Car',
            'user': user_name,
            'phone': i.phone_number or 'N/A',
            'status': i.status or 'Pending',
            'payment_status': i.payment_status or 'Pending',
            'payment_method': i.payment_method or 'Razorpay / Cash',
            'amount': amount,
            'date': str(i.booking_date) if i.booking_date else i.created_at.strftime('%b %d, %Y')
        })

    return {
        'total_inventory': total_inventory,
        'total_cars': total_cars,
        'total_bikes': total_bikes,
        'total_halls': total_halls,
        'total_offices': total_offices,
        'total_houses': total_houses,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'rejected_bookings': rejected_bookings,
        'gross_revenue': total_gross_revenue,
        'status_breakdown': {
            'confirmed': approved_bookings,
            'pending': pending_bookings,
            'cancelled': rejected_bookings,
            'total': total_bookings
        },
        'category_ratio': [cat_car, cat_bike, cat_hall, cat_office, cat_house],
        'revenue_values': [rev_car, rev_bike, rev_hall, rev_office, rev_house],
        'timeframe_revenue': {
            '1_day': {
                'labels': day_labels,
                'data': day_data,
                'total': sum(day_data)
            },
            '1_week': {
                'labels': week_labels,
                'data': week_data,
                'total': sum(week_data)
            },
            '1_month': {
                'labels': month_labels,
                'data': month_data,
                'total': sum(month_data)
            }
        },
        'recent_activity': recent_activity
    }

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_dashboard_page(request):
    dashboard_data = get_dashboard_analytics_payload()
    return render(request, 'admin_app/dashboard.html', {
        'dashboard_json': json.dumps(dashboard_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_dashboard_api(request):
    try:
        dashboard_data = get_dashboard_analytics_payload()
        return JsonResponse({'status': 'success', 'data': dashboard_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_vehicles_page(request):
    return render(request, 'admin_app/manage_vehicles.html')

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_cars_page(request):
    cars = Car.objects.all().order_by('-id')
    cars_data = []
    for c in cars:
        cars_data.append({
            'id': c.id,
            'name': c.name,
            'category': c.category,
            'price': float(c.price_per_day),
            'seats': c.seats,
            'transmission': c.transmission,
            'fuelType': c.fuel_type,
            'startKm': c.start_km,
            'endKm': c.end_km,
            'allowedKmPerDay': c.allowed_km_per_day,
            'extraKmRate': float(c.extra_km_rate),
            'inspectionStatus': c.inspection_status,
            'status': c.status,
            'description': c.description,
            'features': c.features,
            'rating': float(c.rating),
            'image': c.image,
            'returnImage': c.return_image,
            'gpsLat': c.gps_lat,
            'gpsLng': c.gps_lng,
            'locationName': c.location_name,
            'engineStatus': c.engine_status,
            'ignitionStatus': c.ignition_status,
        })

    # Fetch unique categories dynamically from database
    db_categories = list(Car.objects.exclude(category='').values_list('category', flat=True).distinct())
    custom_categories = list(VehicleCategory.objects.filter(vehicle_type='car').values_list('name', flat=True))
    categories = sorted(list(set([c.strip() for c in (db_categories + custom_categories) if c and c.strip()])))
    if not categories:
        categories = ['SUV', 'Thar / Off-Road', 'Sedan', 'Hatchback', 'Luxury', 'Convertible']

    # Fetch Car Categories DB records for Tab 2 management
    car_categories_objs = VehicleCategory.objects.filter(vehicle_type='car').order_by('-id')
    car_categories_list = []
    for cat in car_categories_objs:
        car_categories_list.append({
            'id': cat.id,
            'name': cat.name,
            'description': cat.description,
            'count': Car.objects.filter(category__icontains=cat.name).count()
        })

    # Fetch Car Features DB records for Tab 3 management
    car_features_objs = VehicleFeature.objects.filter(vehicle_type='car').order_by('-id')
    car_features_list = []
    for feat in car_features_objs:
        car_features_list.append({
            'id': feat.id,
            'name': feat.name,
            'description': feat.description
        })

    return render(request, 'admin_app/manage_cars.html', {
        'cars': cars,
        'categories': categories,
        'car_categories_list': car_categories_list,
        'car_features_list': car_features_list,
        'cars_json': json.dumps(cars_data)
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_car_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            category = data.get('category', 'SUV').strip()
            price = float(data.get('price', 0))
            seats = int(data.get('seats', 5))
            transmission = data.get('transmission', 'Automatic').strip()
            fuel_type = data.get('fuelType', 'Petrol').strip()
            start_km = int(data.get('startKm', 10000))
            end_km = int(data.get('endKm', start_km + 120))
            allowed_km_per_day = int(data.get('allowedKmPerDay', 150))
            extra_km_rate = float(data.get('extraKmRate', 15.00))
            inspection_status = data.get('inspectionStatus', 'Verified').strip()
            status = data.get('status', 'Available').strip()
            description = data.get('description', 'Feature-loaded car perfect for road trips and city driving.').strip()
            features = data.get('features', '4x4 Drive, Automatic Transmission, Touchscreen Infotainment, Dual Airbags, ABS with EBD').strip()
            rating = float(data.get('rating', 4.9))
            image = data.get('image', '/static/images/image/carimgs/thar1.jpg').strip()

            if not name or price <= 0:
                return JsonResponse({'status': 'error', 'message': 'Invalid name or price.'}, status=400)

            car = Car.objects.create(
                name=name,
                category=category,
                price_per_day=price,
                seats=seats,
                transmission=transmission,
                fuel_type=fuel_type,
                start_km=start_km,
                end_km=end_km,
                allowed_km_per_day=allowed_km_per_day,
                extra_km_rate=extra_km_rate,
                inspection_status=inspection_status,
                status=status,
                description=description,
                features=features,
                rating=rating,
                image=image,
                return_image=image
            )
            return JsonResponse({
                'status': 'success',
                'car': {
                    'id': car.id,
                    'name': car.name,
                    'category': car.category,
                    'price': float(car.price_per_day),
                    'seats': car.seats,
                    'transmission': car.transmission,
                    'fuelType': car.fuel_type,
                    'startKm': car.start_km,
                    'endKm': car.end_km,
                    'allowedKmPerDay': car.allowed_km_per_day,
                    'extraKmRate': float(car.extra_km_rate),
                    'inspectionStatus': car.inspection_status,
                    'status': car.status,
                    'description': car.description,
                    'features': car.features,
                    'rating': float(car.rating),
                    'image': car.image,
                    'returnImage': car.return_image,
                    'gpsLat': car.gps_lat,
                    'gpsLng': car.gps_lng,
                    'locationName': car.location_name,
                    'engineStatus': car.engine_status,
                    'ignitionStatus': car.ignition_status,
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_car_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            car_id = data.get('id')
            car = Car.objects.filter(pk=car_id).first()
            if not car:
                return JsonResponse({'status': 'error', 'message': 'Car not found.'}, status=404)

            if 'name' in data and data['name']: car.name = str(data['name']).strip()
            if 'category' in data and data['category']: car.category = str(data['category']).strip()
            if 'price' in data and data['price'] is not None: car.price_per_day = float(data['price'])
            if 'seats' in data and data['seats'] is not None: car.seats = int(data['seats'])
            if 'transmission' in data and data['transmission']: car.transmission = str(data['transmission']).strip()
            if 'fuelType' in data and data['fuelType']: car.fuel_type = str(data['fuelType']).strip()
            if 'startKm' in data and data['startKm'] is not None: car.start_km = int(data['startKm'])
            if 'endKm' in data and data['endKm'] is not None: car.end_km = int(data['endKm'])
            if 'allowedKmPerDay' in data and data['allowedKmPerDay'] is not None: car.allowed_km_per_day = int(data['allowedKmPerDay'])
            if 'extraKmRate' in data and data['extraKmRate'] is not None: car.extra_km_rate = float(data['extraKmRate'])
            if 'inspectionStatus' in data and data['inspectionStatus']: car.inspection_status = str(data['inspectionStatus']).strip()
            if 'status' in data and data['status']: car.status = str(data['status']).strip()
            if 'description' in data: car.description = str(data['description']).strip()
            if 'features' in data: car.features = str(data['features']).strip()
            if 'rating' in data and data['rating'] is not None: car.rating = float(data['rating'])
            if 'image' in data and data['image']: car.image = str(data['image']).strip()
            if 'returnImage' in data and data['returnImage']: car.return_image = str(data['returnImage']).strip()
            if 'engineStatus' in data and data['engineStatus']: car.engine_status = str(data['engineStatus']).strip()

            car.save()
            return JsonResponse({
                'status': 'success',
                'car': {
                    'id': car.id,
                    'name': car.name,
                    'category': car.category,
                    'price': float(car.price_per_day),
                    'seats': car.seats,
                    'transmission': car.transmission,
                    'fuelType': car.fuel_type,
                    'startKm': car.start_km,
                    'endKm': car.end_km,
                    'allowedKmPerDay': car.allowed_km_per_day,
                    'extraKmRate': float(car.extra_km_rate),
                    'inspectionStatus': car.inspection_status,
                    'status': car.status,
                    'description': car.description,
                    'features': car.features,
                    'rating': float(car.rating),
                    'image': car.image,
                    'returnImage': car.return_image,
                    'gpsLat': car.gps_lat,
                    'gpsLng': car.gps_lng,
                    'locationName': car.location_name,
                    'engineStatus': car.engine_status,
                    'ignitionStatus': car.ignition_status,
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_car_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            car_id = data.get('id')
            car = Car.objects.filter(pk=car_id).first()
            if car:
                car.delete()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Car not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)

from vehicle_rentals.models import Car, Bike

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_bikes_page(request):
    bikes = Bike.objects.all().order_by('-id')
    bikes_data = []
    for b in bikes:
        bikes_data.append({
            'id': b.id,
            'name': b.name,
            'category': b.category,
            'price': float(b.price_per_day),
            'engineCc': b.engine_cc,
            'powerHp': b.power_hp,
            'averageMileage': b.average_mileage,
            'fuelType': b.fuel_type,
            'startKm': b.start_km,
            'endKm': b.end_km,
            'allowedKmPerDay': b.allowed_km_per_day,
            'extraKmRate': float(b.extra_km_rate),
            'inspectionStatus': b.inspection_status,
            'status': b.status,
            'description': b.description,
            'features': b.features,
            'rating': float(b.rating),
            'image': b.image,
            'returnImage': b.return_image,
            'gpsLat': b.gps_lat,
            'gpsLng': b.gps_lng,
            'locationName': b.location_name,
            'engineStatus': b.engine_status,
            'ignitionStatus': b.ignition_status,
        })
    db_categories = list(Bike.objects.exclude(category='').values_list('category', flat=True).distinct())
    custom_categories = list(VehicleCategory.objects.filter(vehicle_type='bike').values_list('name', flat=True))
    categories = sorted(list(set([c.strip() for c in (db_categories + custom_categories) if c and c.strip()])))
    if not categories:
        categories = ['Cruiser', 'Sports', 'Commuter', 'Scooter', 'Touring', 'Superbike']

    bike_categories_objs = VehicleCategory.objects.filter(vehicle_type='bike').order_by('-id')
    bike_categories_list = []
    for cat in bike_categories_objs:
        bike_categories_list.append({
            'id': cat.id,
            'name': cat.name,
            'description': cat.description,
            'count': Bike.objects.filter(category__icontains=cat.name).count()
        })

    bike_features_objs = VehicleFeature.objects.filter(vehicle_type='bike').order_by('-id')
    bike_features_list = []
    for feat in bike_features_objs:
        bike_features_list.append({
            'id': feat.id,
            'name': feat.name,
            'description': feat.description
        })

    return render(request, 'admin_app/manage_bikes.html', {
        'bikes': bikes,
        'categories': categories,
        'bike_categories_list': bike_categories_list,
        'bike_features_list': bike_features_list,
        'bikes_json': json.dumps(bikes_data)
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_bike_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            category = data.get('category', 'Cruiser').strip()
            price = float(data.get('price', 0))
            engine_cc = data.get('engineCc', '350cc').strip()
            power_hp = data.get('powerHp', '20.2 BHP').strip()
            average_mileage = data.get('averageMileage', '35 km/l').strip()
            fuel_type = data.get('fuelType', 'Petrol').strip()
            start_km = int(data.get('startKm', 5000))
            end_km = int(data.get('endKm', start_km + 80))
            allowed_km_per_day = int(data.get('allowedKmPerDay', 120))
            extra_km_rate = float(data.get('extraKmRate', 5.00))
            inspection_status = data.get('inspectionStatus', 'Verified').strip()
            status = data.get('status', 'Available').strip()
            description = data.get('description', 'High performance two-wheeler built for long rides.').strip()
            features = data.get('features', 'Dual Channel ABS, Electric Start, Digital Console').strip()
            rating = float(data.get('rating', 4.8))
            image = data.get('image', '/static/images/image/bikeimg/bullet.jpg').strip()

            if not name or price <= 0:
                return JsonResponse({'status': 'error', 'message': 'Invalid name or price.'}, status=400)

            bike = Bike.objects.create(
                name=name,
                category=category,
                price_per_day=price,
                engine_cc=engine_cc,
                power_hp=power_hp,
                average_mileage=average_mileage,
                fuel_type=fuel_type,
                start_km=start_km,
                end_km=end_km,
                allowed_km_per_day=allowed_km_per_day,
                extra_km_rate=extra_km_rate,
                inspection_status=inspection_status,
                status=status,
                description=description,
                features=features,
                rating=rating,
                image=image,
                return_image=image
            )
            return JsonResponse({
                'status': 'success',
                'bike': {
                    'id': bike.id,
                    'name': bike.name,
                    'category': bike.category,
                    'price': float(bike.price_per_day),
                    'engineCc': bike.engine_cc,
                    'powerHp': bike.power_hp,
                    'averageMileage': bike.average_mileage,
                    'fuelType': bike.fuel_type,
                    'startKm': bike.start_km,
                    'endKm': bike.end_km,
                    'allowedKmPerDay': bike.allowed_km_per_day,
                    'extraKmRate': float(bike.extra_km_rate),
                    'inspectionStatus': bike.inspection_status,
                    'status': bike.status,
                    'description': bike.description,
                    'features': bike.features,
                    'rating': float(bike.rating),
                    'image': bike.image,
                    'returnImage': bike.return_image,
                    'gpsLat': bike.gps_lat,
                    'gpsLng': bike.gps_lng,
                    'locationName': bike.location_name,
                    'engineStatus': bike.engine_status,
                    'ignitionStatus': bike.ignition_status,
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_bike_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            bike_id = data.get('id')
            bike = Bike.objects.filter(pk=bike_id).first()
            if not bike:
                return JsonResponse({'status': 'error', 'message': 'Bike not found.'}, status=404)

            if 'name' in data and data['name']: bike.name = str(data['name']).strip()
            if 'category' in data and data['category']: bike.category = str(data['category']).strip()
            if 'price' in data and data['price'] is not None: bike.price_per_day = float(data['price'])
            if 'engineCc' in data and data['engineCc']: bike.engine_cc = str(data['engineCc']).strip()
            if 'powerHp' in data and data['powerHp']: bike.power_hp = str(data['powerHp']).strip()
            if 'averageMileage' in data and data['averageMileage']: bike.average_mileage = str(data['averageMileage']).strip()
            if 'fuelType' in data and data['fuelType']: bike.fuel_type = str(data['fuelType']).strip()
            if 'startKm' in data and data['startKm'] is not None: bike.start_km = int(data['startKm'])
            if 'endKm' in data and data['endKm'] is not None: bike.end_km = int(data['endKm'])
            if 'allowedKmPerDay' in data and data['allowedKmPerDay'] is not None: bike.allowed_km_per_day = int(data['allowedKmPerDay'])
            if 'extraKmRate' in data and data['extraKmRate'] is not None: bike.extra_km_rate = float(data['extraKmRate'])
            if 'inspectionStatus' in data and data['inspectionStatus']: bike.inspection_status = str(data['inspectionStatus']).strip()
            if 'status' in data and data['status']: bike.status = str(data['status']).strip()
            if 'description' in data: bike.description = str(data['description']).strip()
            if 'features' in data: bike.features = str(data['features']).strip()
            if 'rating' in data and data['rating'] is not None: bike.rating = float(data['rating'])
            if 'image' in data and data['image']: bike.image = str(data['image']).strip()
            if 'returnImage' in data and data['returnImage']: bike.return_image = str(data['returnImage']).strip()
            if 'engineStatus' in data and data['engineStatus']: bike.engine_status = str(data['engineStatus']).strip()

            bike.save()
            return JsonResponse({
                'status': 'success',
                'bike': {
                    'id': bike.id,
                    'name': bike.name,
                    'category': bike.category,
                    'price': float(bike.price_per_day),
                    'engineCc': bike.engine_cc,
                    'powerHp': bike.power_hp,
                    'averageMileage': bike.average_mileage,
                    'fuelType': bike.fuel_type,
                    'startKm': bike.start_km,
                    'endKm': bike.end_km,
                    'allowedKmPerDay': bike.allowed_km_per_day,
                    'extraKmRate': float(bike.extra_km_rate),
                    'inspectionStatus': bike.inspection_status,
                    'status': bike.status,
                    'description': bike.description,
                    'features': bike.features,
                    'rating': float(bike.rating),
                    'image': bike.image,
                    'returnImage': bike.return_image,
                    'gpsLat': bike.gps_lat,
                    'gpsLng': bike.gps_lng,
                    'locationName': bike.location_name,
                    'engineStatus': bike.engine_status,
                    'ignitionStatus': bike.ignition_status,
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_bike_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            bike_id = data.get('id')
            bike = Bike.objects.filter(pk=bike_id).first()
            if bike:
                bike.delete()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Bike not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_categories_page(request):
    if request.method == 'POST':
        v_type = request.POST.get('vehicle_type', 'car').strip().lower()
        cat_name = request.POST.get('name', '').strip()
        desc = request.POST.get('description', '').strip()
        if cat_name:
            VehicleCategory.objects.create(name=cat_name, vehicle_type=v_type, description=desc)
            messages.success(request, f"Category '{cat_name}' added successfully!")
        return redirect('/admin-portal/manage-categories/')

    car_categories = VehicleCategory.objects.filter(vehicle_type='car').order_by('-id')
    bike_categories = VehicleCategory.objects.filter(vehicle_type='bike').order_by('-id')
    car_features = VehicleFeature.objects.filter(vehicle_type='car').order_by('-id')
    bike_features = VehicleFeature.objects.filter(vehicle_type='bike').order_by('-id')

    active_car_cats = list(Car.objects.exclude(category='').values_list('category', flat=True).distinct())
    active_bike_cats = list(Bike.objects.exclude(category='').values_list('category', flat=True).distinct())

    return render(request, 'admin_app/manage_categories.html', {
        'car_categories': car_categories,
        'bike_categories': bike_categories,
        'car_features': car_features,
        'bike_features': bike_features,
        'active_car_cats': active_car_cats,
        'active_bike_cats': active_bike_cats,
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_category_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            v_type = data.get('vehicle_type', 'car').strip().lower()
            description = data.get('description', '').strip()

            if not name:
                return JsonResponse({'status': 'error', 'message': 'Category name is required.'}, status=400)

            category, created = VehicleCategory.objects.get_or_create(
                name=name,
                vehicle_type=v_type,
                defaults={'description': description}
            )
            if not created and description:
                category.description = description
                category.save()

            return JsonResponse({
                'status': 'success',
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'vehicle_type': category.vehicle_type,
                    'description': category.description
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_category_api(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
            cat_id = data.get('id')
            cat_name = data.get('name')

            cat = None
            if cat_id and str(cat_id).isdigit() and int(cat_id) > 0:
                cat = VehicleCategory.objects.filter(pk=int(cat_id)).first()
            if not cat and cat_name:
                cat = VehicleCategory.objects.filter(name__iexact=str(cat_name).strip()).first()

            if cat:
                cat.delete()
                return JsonResponse({'status': 'success', 'message': 'Category deleted successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Category not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_feature_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            v_type = data.get('vehicle_type', 'car').strip().lower()
            description = data.get('description', '').strip()

            if not name:
                return JsonResponse({'status': 'error', 'message': 'Feature name is required.'}, status=400)

            feature, created = VehicleFeature.objects.get_or_create(
                name=name,
                vehicle_type=v_type,
                defaults={'description': description}
            )
            if not created and description:
                feature.description = description
                feature.save()

            return JsonResponse({
                'status': 'success',
                'feature': {
                    'id': feature.id,
                    'name': feature.name,
                    'vehicle_type': feature.vehicle_type,
                    'description': feature.description
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_feature_api(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
            feat_id = data.get('id')
            feat_name = data.get('name')

            feat = None
            if feat_id and str(feat_id).isdigit() and int(feat_id) > 0:
                feat = VehicleFeature.objects.filter(pk=int(feat_id)).first()
            if not feat and feat_name:
                feat = VehicleFeature.objects.filter(name__iexact=str(feat_name).strip()).first()

            if feat:
                feat.delete()
                return JsonResponse({'status': 'success', 'message': 'Feature deleted successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Feature not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)




@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_toggle_engine_lock_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            vehicle_type = str(data.get('type', 'car')).lower()
            vehicle_id = data.get('id')
            vehicle_title = data.get('title', '')
            
            vehicle = None
            if vehicle_type == 'bike':
                if vehicle_id and str(vehicle_id).isdigit() and int(vehicle_id) > 0:
                    vehicle = Bike.objects.filter(pk=int(vehicle_id)).first()
                if not vehicle and vehicle_title:
                    vehicle = Bike.objects.filter(name__icontains=vehicle_title).first()
                if not vehicle:
                    vehicle = Bike.objects.first()
            else:
                if vehicle_id and str(vehicle_id).isdigit() and int(vehicle_id) > 0:
                    vehicle = Car.objects.filter(pk=int(vehicle_id)).first()
                if not vehicle and vehicle_title:
                    vehicle = Car.objects.filter(name__icontains=vehicle_title).first()
                if not vehicle:
                    vehicle = Car.objects.first()
                
            if not vehicle:
                return JsonResponse({'status': 'error', 'message': 'Vehicle not found.'}, status=404)
                
            vehicle.engine_status = 'LOCKED' if vehicle.engine_status != 'LOCKED' else 'UNLOCKED'
            vehicle.save()
            return JsonResponse({'status': 'success', 'engineStatus': vehicle.engine_status, 'vehicle_name': getattr(vehicle, 'name', '')})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_update_booking_status_api(request):
    if request.method == 'POST':
        try:
            from booking_manager.models import BookingInquiry
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('id')
            new_status = data.get('status', 'Approved').strip()
            
            inquiry = BookingInquiry.objects.filter(pk=inquiry_id).first()
            if not inquiry:
                return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)
                
            if new_status in ['Approved', 'Confirmed']:
                inquiry.status = 'Approved'
                inquiry.payment_status = 'Paid / Confirmed'
            elif new_status == 'Completed':
                inquiry.status = 'Completed'
                inquiry.payment_status = 'Completed'
            elif new_status == 'Rejected':
                inquiry.status = 'Rejected'
                inquiry.payment_status = 'Rejected'
            elif new_status == 'Cancelled':
                inquiry.status = 'Cancelled'
                inquiry.payment_status = 'Cancelled'
            elif new_status == 'Pending':
                inquiry.status = 'Pending'
                inquiry.payment_status = 'Pending'
            else:
                inquiry.status = new_status

            if 'quoted_price' in data and str(data.get('quoted_price')).strip() != '':
                try:
                    inquiry.quoted_price = float(data.get('quoted_price'))
                except (ValueError, TypeError):
                    pass

            if 'representative_name' in data:
                inquiry.representative_name = str(data.get('representative_name')).strip()

            if 'representative_phone' in data:
                inquiry.representative_phone = str(data.get('representative_phone')).strip()

            if 'meeting_location' in data:
                inquiry.meeting_location = str(data.get('meeting_location')).strip()

            if 'admin_notes' in data:
                inquiry.admin_notes = str(data.get('admin_notes')).strip()

            inquiry.save()
            return JsonResponse({'status': 'success', 'inquiry_id': inquiry.id, 'new_status': inquiry.status})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_extra_charge_api(request):
    if request.method == 'POST':
        try:
            from booking_manager.models import BookingInquiry
            from vehicle_rentals.models import Car, Bike
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('id')
            extra_fee = float(data.get('extra_fee', 0))
            extra_km = int(data.get('extra_km', 0))
            
            inquiry = BookingInquiry.objects.filter(pk=inquiry_id).first()
            if not inquiry:
                return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)
                
            inquiry.extra_km_fee = extra_fee
            inquiry.extra_km_driven = extra_km
            if extra_fee > 0:
                if inquiry.extra_fee_status in ['No Extra Fee', '']:
                    inquiry.extra_fee_status = 'Pending Payment'
            else:
                inquiry.extra_fee_status = 'No Extra Fee'
            inquiry.save()

            # Update vehicle odometer start_km / end_km & return_image if passed
            if 'start_km' in data or 'end_km' in data or 'return_image' in data:
                try:
                    v = None
                    if inquiry.category_type == 'car':
                        v = Car.objects.filter(pk=inquiry.item_id).first() or Car.objects.filter(name__icontains=inquiry.item_title).first()
                    elif inquiry.category_type == 'bike':
                        v = Bike.objects.filter(pk=inquiry.item_id).first() or Bike.objects.filter(name__icontains=inquiry.item_title).first()
                    if v:
                        if 'start_km' in data and data['start_km'] != '':
                            v.start_km = int(data['start_km'])
                        if 'end_km' in data and data['end_km'] != '':
                            v.end_km = int(data['end_km'])
                        if 'return_image' in data and data['return_image']:
                            v.return_image = str(data['return_image']).strip()
                        v.save()
                except Exception as ex_v:
                    pass

            return JsonResponse({
                'status': 'success',
                'inquiry_id': inquiry.id,
                'extra_fee': float(inquiry.extra_km_fee),
                'extra_km': inquiry.extra_km_driven,
                'extra_fee_status': inquiry.extra_fee_status
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_confirm_extra_fee_api(request):
    if request.method == 'POST':
        try:
            from booking_manager.models import BookingInquiry
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('id')
            
            inquiry = BookingInquiry.objects.filter(pk=inquiry_id).first()
            if not inquiry:
                return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)
                
            inquiry.extra_fee_status = 'Settlement Confirmed'
            inquiry.save()
            return JsonResponse({'status': 'success', 'inquiry_id': inquiry.id, 'extra_fee_status': inquiry.extra_fee_status})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


def helper_build_booking_dict(i):
    from vehicle_rentals.models import Car, Bike
    from datetime import datetime
    import re

    user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
    user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
    user_phone = i.phone_number or '+91 98765 43210'
    
    user_verification_status = 'Unverified'
    if i.user and hasattr(i.user, 'profile'):
        user_verification_status = i.user.profile.verification_status

    cat_type = str(i.category_type or 'car').lower()

    v = None
    if cat_type == 'car':
        v = Car.objects.filter(pk=i.item_id).first() or Car.objects.filter(name__icontains=i.item_title).first()
    elif cat_type == 'bike':
        v = Bike.objects.filter(pk=i.item_id).first() or Bike.objects.filter(name__icontains=i.item_title).first()

    start_km = v.start_km if v else 10000
    end_km = v.end_km if v else 10200
    allowed_km = v.allowed_km_per_day if v else 150
    extra_rate = float(v.extra_km_rate) if v else 15.0
    gps_lat = v.gps_lat if v else '21.7645'
    gps_lng = v.gps_lng if v else '72.1519'
    engine_status = v.engine_status if v else 'UNLOCKED'
    ignition_status = v.ignition_status if v else 'OFF'

    start_d_str = str(i.start_date or '').strip()
    end_d_str = str(i.end_date or '').strip()

    if not start_d_str or not end_d_str or start_d_str == 'None' or end_d_str == 'None':
        dates_found = re.findall(r'\d{4}-\d{2}-\d{2}', str(i.booking_date or ''))
        if len(dates_found) >= 2:
            start_d_str = dates_found[0]
            end_d_str = dates_found[1]
        elif len(dates_found) == 1:
            start_d_str = end_d_str = dates_found[0]

    if not start_d_str or start_d_str == 'None':
        start_d_str = '2026-09-22'
    if not end_d_str or end_d_str == 'None':
        end_d_str = start_d_str

    days = 1
    try:
        s_dt = datetime.strptime(start_d_str[:10], "%Y-%m-%d")
        e_dt = datetime.strptime(end_d_str[:10], "%Y-%m-%d")
        diff_days = (e_dt - s_dt).days
        if diff_days > 0:
            days = diff_days
    except Exception:
        if hasattr(i, 'num_days') and i.num_days and i.num_days > 0:
            days = i.num_days

    location_name = i.appointment_time if (i.appointment_time and not re.match(r'^\d{4}-\d{2}-\d{2}', str(i.appointment_time))) else (i.location_preference or (v.location_name if v else 'Bhavnagar Central Hub'))

    total_allowed = allowed_km * days
    driven_km = max(0, end_km - start_km)
    calc_extra_km = max(0, driven_km - total_allowed)

    extra_km_driven = i.extra_km_driven if (i.extra_km_driven and i.extra_km_driven > 0) else calc_extra_km
    extra_km_fee = float(i.extra_km_fee) if (i.extra_km_fee and i.extra_km_fee > 0) else float(extra_km_driven * extra_rate)

    total_val = 2499.0
    if i.guests_or_km:
        nums = re.findall(r'\d+', str(i.guests_or_km).replace(',', ''))
        if nums:
            total_val = float(nums[-1])

    price_per_day = float(v.price_per_day) if (v and hasattr(v, 'price_per_day') and v.price_per_day) else 1500.0

    return_img = v.return_image if (v and hasattr(v, 'return_image') and v.return_image) else (i.image_url or '/static/images/image/carimgs/thar1.jpg')
    prev_img = i.image_url or (v.image if (v and hasattr(v, 'image')) else '/static/images/image/carimgs/thar1.jpg')

    raw_feats = getattr(v, 'features', 'Air Condition, Touchscreen, ABS') if v else 'Air Condition, Touchscreen, ABS'
    clean_feats = str(raw_feats).replace('\r\n', ', ').replace('\n', ', ').replace('\r', ', ')

    specs = {
        'seats': getattr(v, 'seats', 5) if v else 5,
        'transmission': getattr(v, 'transmission', 'Automatic') if v else 'Automatic',
        'fuel_type': getattr(v, 'fuel_type', 'Petrol') if v else 'Petrol',
        'category': getattr(v, 'category', 'Standard') if v else 'Standard',
        'engine_cc': getattr(v, 'engine_cc', '350cc') if v else '350cc',
        'features': clean_feats
    }

    return {
        'id': f"VG-{i.id}",
        'db_id': i.id,
        'user_id': i.user.id if i.user else None,
        'vehicle_id': i.item_id,
        'user': user_name,
        'email': user_email,
        'phone': user_phone,
        'verificationStatus': user_verification_status,
        'vehicle': i.item_title or 'Vehicle',
        'type': cat_type.capitalize(),
        'startDate': start_d_str,
        'endDate': end_d_str,
        'days': days,
        'dailyPrice': price_per_day,
        'startKm': start_km,
        'endKm': end_km,
        'allowedKmPerDay': allowed_km,
        'extraKmRate': extra_rate,
        'extraKmDriven': extra_km_driven,
        'extraKmFee': extra_km_fee,
        'extraFeeStatus': i.extra_fee_status or 'Pending',
        'extraFeePaymentMode': getattr(i, 'extra_fee_payment_mode', 'Razorpay') or 'Razorpay',
        'showroomOtp': getattr(i, 'showroom_otp', '') or (f"{100000 + (i.id * 73) % 899999}"),
        'total': total_val,
        'status': i.status or 'Pending',
        'prevImg': prev_img,
        'returnImg': return_img,
        'gpsLat': gps_lat,
        'gpsLng': gps_lng,
        'locationName': location_name,
        'engineStatus': engine_status,
        'ignitionStatus': ignition_status,
        'specs': specs,
    }


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_bookings_api(request):
    try:
        from booking_manager.models import BookingInquiry
        inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike', 'Car', 'Bike']).order_by('-id')
        bookings_data = [helper_build_booking_dict(i) for i in inquiries]
        return JsonResponse({'status': 'success', 'bookings': bookings_data, 'count': len(bookings_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_bookings_page(request):
    from booking_manager.models import BookingInquiry
    inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike', 'Car', 'Bike']).order_by('-id')
    bookings_data = [helper_build_booking_dict(i) for i in inquiries]

    return render(request, 'admin_app/manage_bookings.html', {
        'inquiries': inquiries,
        'bookings_json': json.dumps(bookings_data)
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_halls_page(request):
    from property_rentals.models import EventHall
    from vehicle_rentals.models import VehicleCategory, VehicleFeature
    from property_rentals.views import seed_default_halls_if_needed
    seed_default_halls_if_needed()

    # Seed default hall categories if empty
    default_hall_categories = ["Marriage Banquet", "Corporate Ballroom", "Party & Celebration", "Open Air Garden Lawn", "Luxury Convention Centre"]
    for cat_name in default_hall_categories:
        VehicleCategory.objects.get_or_create(name=cat_name, vehicle_type='hall')

    # Seed default hall features if empty
    default_hall_features = ["Central AC", "In-House Catering", "LED Stage & DJ", "24/7 Power Backup", "Bridal Luxury Suite", "Valet Parking", "Sound System", "CCTV & Security"]
    for feat_name in default_hall_features:
        VehicleFeature.objects.get_or_create(name=feat_name, vehicle_type='hall')

    halls = EventHall.objects.all().order_by('-id')
    halls_data = []
    for h in halls:
        halls_data.append({
            'id': h.id,
            'name': h.name,
            'category': h.category,
            'price': float(h.price_per_day),
            'capacity': h.capacity,
            'acType': h.ac_type,
            'parking': h.parking,
            'catering': h.catering_policy,
            'stageDj': h.stage_dj_setup,
            'location': h.location,
            'amenities': h.amenities,
            'status': h.status,
            'image': h.image or '/static/images/image/c1.jpg'
        })

    hall_categories_qs = VehicleCategory.objects.filter(vehicle_type='hall').order_by('name')
    categories = [c.name for c in hall_categories_qs]
    hall_categories_list = []
    for c in hall_categories_qs:
        count = EventHall.objects.filter(category__iexact=c.name).count()
        hall_categories_list.append({'id': c.id, 'name': c.name, 'description': c.description, 'count': count})

    hall_features_qs = VehicleFeature.objects.filter(vehicle_type='hall').order_by('name')
    hall_features_list = [{'id': f.id, 'name': f.name, 'description': f.description} for f in hall_features_qs]

    return render(request, 'admin_app/manage_halls.html', {
        'halls': halls,
        'halls_json': json.dumps(halls_data),
        'categories': categories,
        'categories_json': json.dumps(categories),
        'hall_categories_list': hall_categories_list,
        'hall_features_list': hall_features_list,
        'features_json': json.dumps(hall_features_list),
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_halls_api(request):
    try:
        from property_rentals.models import EventHall
        halls = EventHall.objects.all().order_by('-id')
        halls_data = []
        for h in halls:
            halls_data.append({
                'id': h.id,
                'name': h.name,
                'category': h.category,
                'price': float(h.price_per_day),
                'capacity': h.capacity,
                'acType': h.ac_type,
                'parking': h.parking,
                'catering': h.catering_policy,
                'stageDj': h.stage_dj_setup,
                'location': h.location,
                'amenities': h.amenities,
                'status': h.status,
                'image': h.image or '/static/images/image/c1.jpg'
            })
        return JsonResponse({'status': 'success', 'halls': halls_data, 'count': len(halls_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_hall_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import EventHall
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            category = data.get('category', 'Marriage Banquet').strip()
            price = float(data.get('price', 0))
            capacity = int(data.get('capacity', 0))
            ac_type = data.get('acType', 'Central AC').strip()
            parking = data.get('parking', '').strip()
            catering = data.get('catering', '').strip()
            stage_dj = data.get('stageDj', '').strip()
            location = data.get('location', '').strip()
            amenities = data.get('amenities', '').strip()
            status = data.get('status', 'Available').strip()
            image = data.get('image', '/static/images/image/c1.jpg').strip()

            if not name or len(name) < 3:
                return JsonResponse({'status': 'error', 'message': 'Hall title must be at least 3 characters long.'}, status=400)
            if price <= 0:
                return JsonResponse({'status': 'error', 'message': 'Daily rent rate must be greater than ₹0.'}, status=400)
            if capacity <= 0:
                return JsonResponse({'status': 'error', 'message': 'Guest capacity must be greater than 0.'}, status=400)
            if not location or len(location) < 3:
                return JsonResponse({'status': 'error', 'message': 'Location address is required (min 3 chars).'}, status=400)

            hall = EventHall.objects.create(
                name=name,
                category=category,
                price_per_day=price,
                capacity=capacity,
                ac_type=ac_type,
                parking=parking or '100 Vehicles',
                catering_policy=catering or 'In-House Pure Veg',
                stage_dj_setup=stage_dj or 'Stage + DJ Console',
                location=location,
                amenities=amenities or '24/7 Power Backup, Dressing Rooms',
                status=status,
                image=image
            )
            return JsonResponse({'status': 'success', 'hall_id': hall.id, 'message': f"Hall '{hall.name}' created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_hall_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import EventHall
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            hall_id = data.get('id')
            hall = EventHall.objects.filter(pk=hall_id).first()
            if not hall:
                return JsonResponse({'status': 'error', 'message': 'Event hall not found.'}, status=404)

            if 'name' in data and data['name']: hall.name = str(data['name']).strip()
            if 'category' in data and data['category']: hall.category = str(data['category']).strip()
            if 'price' in data and data['price'] is not None: hall.price_per_day = float(data['price'])
            if 'capacity' in data and data['capacity'] is not None: hall.capacity = int(data['capacity'])
            if 'acType' in data and data['acType']: hall.ac_type = str(data['acType']).strip()
            if 'parking' in data and data['parking']: hall.parking = str(data['parking']).strip()
            if 'catering' in data and data['catering']: hall.catering_policy = str(data['catering']).strip()
            if 'stageDj' in data and data['stageDj']: hall.stage_dj_setup = str(data['stageDj']).strip()
            if 'location' in data and data['location']: hall.location = str(data['location']).strip()
            if 'status' in data and data['status']: hall.status = str(data['status']).strip()
            if 'amenities' in data: hall.amenities = str(data['amenities']).strip()
            if 'image' in data and data['image']: hall.image = str(data['image']).strip()

            hall.save()
            return JsonResponse({'status': 'success', 'hall_id': hall.id, 'message': f"Hall '{hall.name}' specifications updated successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_hall_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import EventHall
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            hall_id = data.get('id')
            hall = EventHall.objects.filter(pk=hall_id).first()
            if hall:
                hall.delete()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Event hall not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_houses_page(request):
    from property_rentals.models import House
    from vehicle_rentals.models import VehicleCategory, VehicleFeature

    # Seed default house categories if empty
    default_house_categories = ["Luxury Villa", "Row House / Townhouse", "Apartment Flat", "Duplex Bungalow", "Penthouse Suite"]
    for cat_name in default_house_categories:
        VehicleCategory.objects.get_or_create(name=cat_name, vehicle_type='house')

    # Seed default house features if empty
    default_house_features = ["Private Swimming Pool", "Solar Power System", "24/7 Gated Security", "Covered Car Garage", "Private Garden", "Modular Kitchen", "Balcony View"]
    for feat_name in default_house_features:
        VehicleFeature.objects.get_or_create(name=feat_name, vehicle_type='house')

    houses = House.objects.all().order_by('-id')
    houses_data = []
    for h in houses:
        houses_data.append({
            'id': h.id,
            'name': h.name,
            'category': h.category,
            'price': float(h.monthly_rent),
            'bedrooms': h.bedrooms,
            'bathrooms': h.bathrooms,
            'areaSqft': h.area_sqft,
            'furnishing': h.furnishing,
            'parking': h.parking,
            'location': h.location,
            'amenities': h.amenities,
            'status': h.status,
            'image': h.image or '/static/images/image/houseimg/i1.jpg'
        })

    house_categories_qs = VehicleCategory.objects.filter(vehicle_type='house').order_by('name')
    categories = [c.name for c in house_categories_qs]
    house_categories_list = []
    for c in house_categories_qs:
        count = House.objects.filter(category__iexact=c.name).count()
        house_categories_list.append({'id': c.id, 'name': c.name, 'description': c.description, 'count': count})

    house_features_qs = VehicleFeature.objects.filter(vehicle_type='house').order_by('name')
    house_features_list = [{'id': f.id, 'name': f.name, 'description': f.description} for f in house_features_qs]

    return render(request, 'admin_app/manage_houses.html', {
        'houses': houses,
        'houses_json': json.dumps(houses_data),
        'categories': categories,
        'categories_json': json.dumps(categories),
        'house_categories_list': house_categories_list,
        'house_features_list': house_features_list,
        'features_json': json.dumps(house_features_list),
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_houses_api(request):
    try:
        from property_rentals.models import House
        houses = House.objects.all().order_by('-id')
        houses_data = []
        for h in houses:
            houses_data.append({
                'id': h.id,
                'name': h.name,
                'category': h.category,
                'price': float(h.monthly_rent),
                'bedrooms': h.bedrooms,
                'bathrooms': h.bathrooms,
                'areaSqft': h.area_sqft,
                'furnishing': h.furnishing,
                'parking': h.parking,
                'location': h.location,
                'amenities': h.amenities,
                'status': h.status,
                'image': h.image or '/static/images/image/houseimg/i1.jpg'
            })
        return JsonResponse({'status': 'success', 'houses': houses_data, 'count': len(houses_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_house_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import House
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            category = data.get('category', 'Luxury Villa').strip()
            price = float(data.get('price', 0))
            bedrooms = int(data.get('bedrooms', 3))
            bathrooms = int(data.get('bathrooms', 3))
            area_sqft = data.get('areaSqft', '2400 sq.ft').strip()
            furnishing = data.get('furnishing', 'Fully Furnished').strip()
            parking = data.get('parking', '2 Car Covered Garage').strip()
            location = data.get('location', '').strip()
            amenities = data.get('amenities', '').strip()
            status = data.get('status', 'Available').strip()
            image = data.get('image', '/static/images/image/houseimg/i1.jpg').strip()

            if not name or len(name) < 3:
                return JsonResponse({'status': 'error', 'message': 'House title must be at least 3 characters.'}, status=400)
            if price <= 0:
                return JsonResponse({'status': 'error', 'message': 'Monthly rent must be greater than ₹0.'}, status=400)
            if not location or len(location) < 3:
                return JsonResponse({'status': 'error', 'message': 'Location address is required (min 3 chars).'}, status=400)

            house = House.objects.create(
                name=name,
                category=category,
                monthly_rent=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area_sqft=area_sqft,
                furnishing=furnishing,
                parking=parking,
                location=location,
                amenities=amenities or '24/7 Gated Security, Private Garden',
                status=status,
                image=image
            )
            return JsonResponse({'status': 'success', 'house_id': house.id, 'message': f"House '{house.name}' created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_house_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import House
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            house_id = data.get('id')
            house = House.objects.filter(pk=house_id).first()
            if not house:
                return JsonResponse({'status': 'error', 'message': 'House listing not found.'}, status=404)

            if 'name' in data and data['name']: house.name = str(data['name']).strip()
            if 'category' in data and data['category']: house.category = str(data['category']).strip()
            if 'price' in data and data['price'] is not None: house.monthly_rent = float(data['price'])
            if 'bedrooms' in data and data['bedrooms'] is not None: house.bedrooms = int(data['bedrooms'])
            if 'bathrooms' in data and data['bathrooms'] is not None: house.bathrooms = int(data['bathrooms'])
            if 'areaSqft' in data and data['areaSqft']: house.area_sqft = str(data['areaSqft']).strip()
            if 'furnishing' in data and data['furnishing']: house.furnishing = str(data['furnishing']).strip()
            if 'parking' in data and data['parking']: house.parking = str(data['parking']).strip()
            if 'location' in data and data['location']: house.location = str(data['location']).strip()
            if 'status' in data and data['status']: house.status = str(data['status']).strip()
            if 'amenities' in data: house.amenities = str(data['amenities']).strip()
            if 'image' in data and data['image']: house.image = str(data['image']).strip()

            house.save()
            return JsonResponse({'status': 'success', 'house_id': house.id, 'message': f"House '{house.name}' updated successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_house_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import House
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            house_id = data.get('id')
            house = House.objects.filter(pk=house_id).first()
            if house:
                house.delete()
                return JsonResponse({'status': 'success', 'message': 'House deleted successfully.'})
            return JsonResponse({'status': 'error', 'message': 'House listing not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_offices_page(request):
    from property_rentals.models import CommercialOffice
    from vehicle_rentals.models import VehicleCategory, VehicleFeature

    # Seed default office categories if empty
    default_office_categories = ["IT Tech Suite", "Co-Working Hub", "Corporate Executive Suite", "Commercial Retail Space", "Startup Incubator Hub"]
    for cat_name in default_office_categories:
        VehicleCategory.objects.get_or_create(name=cat_name, vehicle_type='office')

    # Seed default office features if empty
    default_office_features = ["High-Speed Fiber Internet", "VRV Central AC", "Dedicated Server Room", "Executive Conference Room", "Pantry & Cafeteria", "24/7 Biometric Access", "Underground Parking"]
    for feat_name in default_office_features:
        VehicleFeature.objects.get_or_create(name=feat_name, vehicle_type='office')

    offices = CommercialOffice.objects.all().order_by('-id')
    offices_data = []
    for o in offices:
        offices_data.append({
            'id': o.id,
            'name': o.name,
            'category': o.category,
            'price': float(o.monthly_rent),
            'workstations': o.workstations,
            'conferenceRooms': o.conference_rooms,
            'areaSqft': o.area_sqft,
            'acType': o.ac_type,
            'parking': o.parking,
            'location': o.location,
            'amenities': o.amenities,
            'status': o.status,
            'image': o.image or '/static/images/image/officeimg/o1.jpg'
        })

    office_categories_qs = VehicleCategory.objects.filter(vehicle_type='office').order_by('name')
    categories = [c.name for c in office_categories_qs]
    office_categories_list = []
    for c in office_categories_qs:
        count = CommercialOffice.objects.filter(category__iexact=c.name).count()
        office_categories_list.append({'id': c.id, 'name': c.name, 'description': c.description, 'count': count})

    office_features_qs = VehicleFeature.objects.filter(vehicle_type='office').order_by('name')
    office_features_list = [{'id': f.id, 'name': f.name, 'description': f.description} for f in office_features_qs]

    return render(request, 'admin_app/manage_offices.html', {
        'offices': offices,
        'offices_json': json.dumps(offices_data),
        'categories': categories,
        'categories_json': json.dumps(categories),
        'office_categories_list': office_categories_list,
        'office_features_list': office_features_list,
        'features_json': json.dumps(office_features_list),
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_offices_api(request):
    try:
        from property_rentals.models import CommercialOffice
        offices = CommercialOffice.objects.all().order_by('-id')
        offices_data = []
        for o in offices:
            offices_data.append({
                'id': o.id,
                'name': o.name,
                'category': o.category,
                'price': float(o.monthly_rent),
                'workstations': o.workstations,
                'conferenceRooms': o.conference_rooms,
                'areaSqft': o.area_sqft,
                'acType': o.ac_type,
                'parking': o.parking,
                'location': o.location,
                'amenities': o.amenities,
                'status': o.status,
                'image': o.image or '/static/images/image/officeimg/o1.jpg'
            })
        return JsonResponse({'status': 'success', 'offices': offices_data, 'count': len(offices_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_add_office_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import CommercialOffice
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name', '').strip()
            category = data.get('category', 'IT Tech Suite').strip()
            price = float(data.get('price', 0))
            workstations = int(data.get('workstations', 25))
            conference_rooms = int(data.get('conferenceRooms', 2))
            area_sqft = data.get('areaSqft', '1800 sq.ft').strip()
            ac_type = data.get('acType', 'VRV Central AC').strip()
            parking = data.get('parking', '4 Underground Slots').strip()
            location = data.get('location', '').strip()
            amenities = data.get('amenities', '').strip()
            status = data.get('status', 'Available').strip()
            image = data.get('image', '/static/images/image/officeimg/o1.jpg').strip()

            if not name or len(name) < 3:
                return JsonResponse({'status': 'error', 'message': 'Office title must be at least 3 characters.'}, status=400)
            if price <= 0:
                return JsonResponse({'status': 'error', 'message': 'Monthly rent must be greater than ₹0.'}, status=400)
            if not location or len(location) < 3:
                return JsonResponse({'status': 'error', 'message': 'Location address is required (min 3 chars).'}, status=400)

            office = CommercialOffice.objects.create(
                name=name,
                category=category,
                monthly_rent=price,
                workstations=workstations,
                conference_rooms=conference_rooms,
                area_sqft=area_sqft,
                ac_type=ac_type,
                parking=parking,
                location=location,
                amenities=amenities or 'High-Speed Fiber Internet, Pantry, 24/7 Access',
                status=status,
                image=image
            )
            return JsonResponse({'status': 'success', 'office_id': office.id, 'message': f"Office '{office.name}' created successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_office_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import CommercialOffice
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            office_id = data.get('id')
            office = CommercialOffice.objects.filter(pk=office_id).first()
            if not office:
                return JsonResponse({'status': 'error', 'message': 'Office listing not found.'}, status=404)

            if 'name' in data and data['name']: office.name = str(data['name']).strip()
            if 'category' in data and data['category']: office.category = str(data['category']).strip()
            if 'price' in data and data['price'] is not None: office.monthly_rent = float(data['price'])
            if 'workstations' in data and data['workstations'] is not None: office.workstations = int(data['workstations'])
            if 'conferenceRooms' in data and data['conferenceRooms'] is not None: office.conference_rooms = int(data['conferenceRooms'])
            if 'areaSqft' in data and data['areaSqft']: office.area_sqft = str(data['areaSqft']).strip()
            if 'acType' in data and data['acType']: office.ac_type = str(data['acType']).strip()
            if 'parking' in data and data['parking']: office.parking = str(data['parking']).strip()
            if 'location' in data and data['location']: office.location = str(data['location']).strip()
            if 'status' in data and data['status']: office.status = str(data['status']).strip()
            if 'amenities' in data: office.amenities = str(data['amenities']).strip()
            if 'image' in data and data['image']: office.image = str(data['image']).strip()

            office.save()
            return JsonResponse({'status': 'success', 'office_id': office.id, 'message': f"Office '{office.name}' updated successfully!"})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_delete_office_api(request):
    if request.method == 'POST':
        try:
            from property_rentals.models import CommercialOffice
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            office_id = data.get('id')
            office = CommercialOffice.objects.filter(pk=office_id).first()
            if office:
                office.delete()
                return JsonResponse({'status': 'success', 'message': 'Office listing deleted successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Office listing not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_bookings_page(request):
    from booking_manager.models import BookingInquiry
    from vehicle_rentals.models import Car, Bike
    import re

    inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike']).order_by('-id')
    bookings_data = []
    for i in inquiries:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
        user_phone = i.phone_number or '+91 98765 43210'
        
        user_verification_status = 'Unverified'
        if i.user and hasattr(i.user, 'profile'):
            user_verification_status = i.user.profile.verification_status

        v = None
        if i.category_type == 'car':
            v = Car.objects.filter(pk=i.item_id).first() or Car.objects.filter(name__icontains=i.item_title).first()
        elif i.category_type == 'bike':
            v = Bike.objects.filter(pk=i.item_id).first() or Bike.objects.filter(name__icontains=i.item_title).first()

        start_km = v.start_km if v else 10000
        end_km = v.end_km if v else 10200
        allowed_km = v.allowed_km_per_day if v else 150
        extra_rate = float(v.extra_km_rate) if v else 15.0
        gps_lat = v.gps_lat if v else '21.7645'
        gps_lng = v.gps_lng if v else '72.1519'
        location_name = v.location_name if v else 'Bhavnagar Central Hub'
        engine_status = v.engine_status if v else 'UNLOCKED'
        ignition_status = v.ignition_status if v else 'OFF'

        days = i.num_days if (hasattr(i, 'num_days') and i.num_days > 0) else 1
        total_allowed = allowed_km * days
        driven_km = max(0, end_km - start_km)
        calc_extra_km = max(0, driven_km - total_allowed)

        extra_km_driven = i.extra_km_driven if (i.extra_km_driven and i.extra_km_driven > 0) else calc_extra_km
        extra_km_fee = float(i.extra_km_fee) if (i.extra_km_fee and i.extra_km_fee > 0) else float(extra_km_driven * extra_rate)

        total_val = 2499.0
        if i.guests_or_km:
            nums = re.findall(r'\d+', str(i.guests_or_km).replace(',', ''))
            if nums:
                total_val = float(nums[-1])

        price_per_day = float(v.price_per_day) if (v and hasattr(v, 'price_per_day') and v.price_per_day) else 1500.0

        bookings_data.append({
            'id': f"VG-{i.id}",
            'db_id': i.id,
            'user_id': i.user.id if i.user else None,
            'vehicle_id': i.item_id,
            'user': user_name,
            'email': user_email,
            'phone': user_phone,
            'verificationStatus': user_verification_status,
            'vehicle': i.item_title or 'Vehicle',
            'type': i.category_type.capitalize() if i.category_type else 'Car',
            'startDate': str(i.booking_date) if i.booking_date else 'Flexible Date',
            'endDate': i.appointment_time or 'Scheduled',
            'days': days,
            'dailyPrice': price_per_day,
            'startKm': start_km,
            'endKm': end_km,
            'allowedKmPerDay': allowed_km,
            'extraKmRate': extra_rate,
            'extraKmDriven': extra_km_driven,
            'extraKmFee': extra_km_fee,
            'extraFeeStatus': i.extra_fee_status or 'Pending',
            'total': total_val,
            'status': i.status or 'Pending',
            'prevImg': i.image_url or '/static/images/image/carimgs/thar1.jpg',
            'returnImg': i.image_url or '/static/images/image/carimgs/thar1.jpg',
            'gpsLat': gps_lat,
            'gpsLng': gps_lng,
            'locationName': location_name,
            'engineStatus': engine_status,
            'ignitionStatus': ignition_status,
        })

    return render(request, 'admin_app/manage_bookings.html', {
        'inquiries': inquiries,
        'bookings_json': json.dumps(bookings_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_status_updates_page(request):
    from booking_manager.models import BookingInquiry
    inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike', 'Car', 'Bike']).order_by('-id')
    bookings_data = [helper_build_booking_dict(i) for i in inquiries]

    return render(request, 'admin_app/manage_status_updates.html', {
        'bookings_json': json.dumps(bookings_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_view_inquiries_page(request):
    from booking_manager.models import BookingInquiry
    from property_rentals.models import EventHall
    import urllib.parse

    inquiries = BookingInquiry.objects.filter(category_type__in=['hall', 'house', 'office']).order_by('-id')
    inquiries_data = []
    for i in inquiries:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
        user_phone = i.phone_number or '+91 98765 43210'
        
        hall = EventHall.objects.filter(pk=i.item_id).first() if i.item_id else EventHall.objects.filter(name__icontains=i.item_title).first()
        
        location = i.location_preference or (hall.location if hall and hall.location else 'Palace Road, Central Sector')
        image = i.image_url
        price = f"₹{i.quoted_price:,.0f}" if i.quoted_price > 0 else (f"₹{hall.price_per_day:,.0f}" if hall else "Quote Pending")
        map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
        
        inquiries_data.append({
            'id': i.id,
            'hall': i.item_title or (hall.name if hall else 'Event Property'),
            'category': i.category_type,
            'location': location,
            'name': user_name,
            'phone': user_phone,
            'displayPhone': user_phone,
            'email': user_email,
            'eventDate': str(i.booking_date) if i.booking_date else 'Flexible Date',
            'duration': i.duration or '1 Day',
            'capacity': i.capacity_needed or i.guests_or_km or '500 Guests',
            'budgetMin': float(i.budget_min or 0),
            'budgetMax': float(i.budget_max or 0),
            'locationPref': i.location_preference or 'Bhavnagar Central',
            'apptTime': i.appointment_time or 'Scheduled Appointment',
            'guests': i.capacity_needed or i.guests_or_km or '500 Guests',
            'price': price,
            'quotedPrice': float(i.quoted_price or 0),
            'status': i.status or 'Pending',
            'image': image,
            'mapUrl': map_url,
            'req': i.special_requirements or 'No special requirements specified.',
            'repName': i.representative_name or '',
            'repPhone': i.representative_phone or '',
            'meetingType': i.meeting_type or 'Google Meet',
            'meetingLocation': i.meeting_location or '',
            'adminNotes': i.admin_notes or '',
        })

    return render(request, 'admin_app/view_inquiries.html', {
        'inquiries': inquiries,
        'inquiries_json': json.dumps(inquiries_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_hall_inquiries_api(request):
    try:
        from booking_manager.models import BookingInquiry
        from property_rentals.models import EventHall
        import urllib.parse

        inquiries = BookingInquiry.objects.filter(category_type__in=['hall', 'house', 'office']).order_by('-id')
        inquiries_data = []
        for i in inquiries:
            user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
            user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
            user_phone = i.phone_number or '+91 98765 43210'
            
            hall = EventHall.objects.filter(pk=i.item_id).first() if i.item_id else EventHall.objects.filter(name__icontains=i.item_title).first()
            
            location = i.location_preference or (hall.location if hall and hall.location else 'Palace Road, Central Sector')
            image = i.image_url
            price = f"₹{i.quoted_price:,.0f}" if i.quoted_price > 0 else (f"₹{hall.price_per_day:,.0f}" if hall else "Quote Pending")
            map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
            
            inquiries_data.append({
                'id': i.id,
                'hall': i.item_title or (hall.name if hall else 'Event Property'),
                'category': i.category_type,
                'location': location,
                'name': user_name,
                'phone': user_phone,
                'displayPhone': user_phone,
                'email': user_email,
                'eventDate': str(i.booking_date) if i.booking_date else 'Flexible Date',
                'duration': i.duration or '1 Day',
                'capacity': i.capacity_needed or i.guests_or_km or '500 Guests',
                'budgetMin': float(i.budget_min or 0),
                'budgetMax': float(i.budget_max or 0),
                'locationPref': i.location_preference or 'Bhavnagar Central',
                'apptTime': i.appointment_time or 'Scheduled Appointment',
                'guests': i.capacity_needed or i.guests_or_km or '500 Guests',
                'price': price,
                'quotedPrice': float(i.quoted_price or 0),
                'status': i.status or 'Pending',
                'image': image,
                'mapUrl': map_url,
                'req': i.special_requirements or 'No special requirements specified.',
                'repName': i.representative_name or '',
                'repPhone': i.representative_phone or '',
                'meetingType': i.meeting_type or 'Google Meet',
                'meetingLocation': i.meeting_location or '',
                'adminNotes': i.admin_notes or '',
            })

        return JsonResponse({'status': 'success', 'inquiries': inquiries_data, 'count': len(inquiries_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_respond_property_inquiry_api(request):
    if request.method == 'POST':
        try:
            from booking_manager.models import BookingInquiry
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('id')
            inquiry = BookingInquiry.objects.filter(pk=inquiry_id).first()
            if not inquiry:
                return JsonResponse({'status': 'error', 'message': 'Property inquiry not found.'}, status=404)

            status = data.get('status', inquiry.status).strip()
            rep_name = data.get('representative_name', '').strip()
            rep_phone = data.get('representative_phone', '').strip()
            meeting_type = data.get('meeting_type', 'Google Meet').strip()
            meeting_location = data.get('meeting_location', '').strip()
            
            try:
                quoted_price = float(data.get('quoted_price', 0))
            except (ValueError, TypeError):
                quoted_price = 0.0

            admin_notes = data.get('admin_notes', '').strip()

            # Auto-generate Google Meet URL if meeting_type is Google Meet and URL not provided
            if meeting_type == 'Google Meet' and not meeting_location:
                import random, string
                code1 = ''.join(random.choices(string.ascii_lowercase, k=3))
                code2 = ''.join(random.choices(string.ascii_lowercase, k=4))
                code3 = ''.join(random.choices(string.ascii_lowercase, k=3))
                meeting_location = f"https://meet.google.com/{code1}-{code2}-{code3}"

            inquiry.status = status
            inquiry.representative_name = rep_name
            inquiry.representative_phone = rep_phone
            inquiry.meeting_type = meeting_type
            inquiry.meeting_location = meeting_location
            inquiry.quoted_price = quoted_price
            inquiry.admin_notes = admin_notes
            inquiry.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Inquiry response & meeting details saved successfully!',
                'inquiry': {
                    'id': inquiry.id,
                    'status': inquiry.status,
                    'repName': inquiry.representative_name,
                    'repPhone': inquiry.representative_phone,
                    'meetingType': inquiry.meeting_type,
                    'meetingLocation': inquiry.meeting_location,
                    'quotedPrice': float(inquiry.quoted_price),
                    'adminNotes': inquiry.admin_notes,
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_view_house_inquiries_page(request):
    from booking_manager.models import BookingInquiry
    from property_rentals.models import House
    import urllib.parse

    inquiries = BookingInquiry.objects.filter(category_type='house').order_by('-id')
    inquiries_data = []
    for i in inquiries:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
        user_phone = i.phone_number or '+91 98980 11223'
        
        house = House.objects.filter(pk=i.item_id).first() if i.item_id else House.objects.filter(name__icontains=i.item_title).first()
        
        location = house.location if house and house.location else i.location_preference or 'Palace Road, Bhavnagar'
        image = i.image_url
        rent = f"₹{house.monthly_rent:,.0f}" if house else f"₹{i.budget_min:,.0f} - ₹{i.budget_max:,.0f}" if i.budget_max else "₹35,000"
        config = f"{house.bedrooms} BHK Villa" if house else "Residential House"
        map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
        
        inquiries_data.append({
            'id': i.id,
            'house': i.item_title or (house.name if house else 'Residential House Villa'),
            'location': location,
            'name': user_name,
            'phone': user_phone,
            'displayPhone': user_phone,
            'email': user_email,
            'config': config,
            'apptTime': i.booking_date or 'Move-in Pending',
            'rent': rent,
            'status': i.status or 'Pending',
            'image': image,
            'mapUrl': map_url,
            'req': i.special_requirements or 'No special requirements specified.',
            'quotedPrice': float(i.quoted_price) if i.quoted_price else 0.0,
            'representativeName': i.representative_name or '',
            'representativePhone': i.representative_phone or '',
            'meetingLocation': i.meeting_location or '',
            'adminNotes': i.admin_notes or '',
            'duration': i.duration or '12 Months Lease',
            'capacityNeeded': i.capacity_needed or '4 Occupants',
            'budgetMin': float(i.budget_min) if i.budget_min else 0.0,
            'budgetMax': float(i.budget_max) if i.budget_max else 0.0
        })

    return render(request, 'admin_app/view_house_inquiries.html', {
        'inquiries': inquiries,
        'house_inquiries_json': json.dumps(inquiries_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_house_inquiries_api(request):
    try:
        from booking_manager.models import BookingInquiry
        from property_rentals.models import House
        import urllib.parse

        inquiries = BookingInquiry.objects.filter(category_type='house').order_by('-id')
        inquiries_data = []
        for i in inquiries:
            user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
            user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
            user_phone = i.phone_number or '+91 98980 11223'
            
            house = House.objects.filter(pk=i.item_id).first() if i.item_id else House.objects.filter(name__icontains=i.item_title).first()
            
            location = house.location if house and house.location else i.location_preference or 'Palace Road, Bhavnagar'
            image = i.image_url
            rent = f"₹{house.monthly_rent:,.0f}" if house else f"₹{i.budget_min:,.0f} - ₹{i.budget_max:,.0f}" if i.budget_max else "₹35,000"
            config = f"{house.bedrooms} BHK Villa" if house else "Residential House"
            map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
            
            inquiries_data.append({
                'id': i.id,
                'house': i.item_title or (house.name if house else 'Residential House Villa'),
                'location': location,
                'name': user_name,
                'phone': user_phone,
                'displayPhone': user_phone,
                'email': user_email,
                'config': config,
                'apptTime': i.booking_date or 'Move-in Pending',
                'rent': rent,
                'status': i.status or 'Pending',
                'image': image,
                'mapUrl': map_url,
                'req': i.special_requirements or 'No special requirements specified.',
                'quotedPrice': float(i.quoted_price) if i.quoted_price else 0.0,
                'representativeName': i.representative_name or '',
                'representativePhone': i.representative_phone or '',
                'meetingLocation': i.meeting_location or '',
                'adminNotes': i.admin_notes or '',
                'duration': i.duration or '12 Months Lease',
                'capacityNeeded': i.capacity_needed or '4 Occupants',
                'budgetMin': float(i.budget_min) if i.budget_min else 0.0,
                'budgetMax': float(i.budget_max) if i.budget_max else 0.0
            })

        return JsonResponse({'status': 'success', 'inquiries': inquiries_data, 'count': len(inquiries_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_view_office_inquiries_page(request):
    from booking_manager.models import BookingInquiry
    from property_rentals.models import CommercialOffice
    import urllib.parse

    inquiries = BookingInquiry.objects.filter(category_type='office').order_by('-id')
    inquiries_data = []
    for i in inquiries:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
        user_phone = i.phone_number or '+91 97654 32109'
        
        office = CommercialOffice.objects.filter(pk=i.item_id).first() if i.item_id else CommercialOffice.objects.filter(name__icontains=i.item_title).first()
        
        location = office.location if office and office.location else i.location_preference or 'Palace Road, Bhavnagar'
        rent = f"₹{office.monthly_rent:,.0f}" if office else f"₹{i.budget_min:,.0f} - ₹{i.budget_max:,.0f}" if i.budget_max else "₹75,000"
        staff = i.capacity_needed or (f"{office.workstations} Workstations" if office else "25 Seats")
        business = i.duration or 'IT Tech Suite'
        move_in = i.booking_date or 'Possession Pending'
        map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
        
        inquiries_data.append({
            'id': i.id,
            'suite': i.item_title or (office.name if office else 'Commercial Office Space'),
            'location': location,
            'name': user_name,
            'phone': user_phone,
            'displayPhone': user_phone,
            'email': user_email,
            'business': business,
            'staff': staff,
            'moveIn': move_in,
            'rent': rent,
            'status': i.status or 'Pending',
            'image': i.image_url,
            'mapUrl': map_url,
            'req': i.special_requirements or 'No special requirements specified.',
            'quotedPrice': float(i.quoted_price) if i.quoted_price else 0.0,
            'representativeName': i.representative_name or '',
            'representativePhone': i.representative_phone or '',
            'meetingLocation': i.meeting_location or '',
            'adminNotes': i.admin_notes or '',
            'duration': i.duration or '12 Months Lease',
            'capacityNeeded': i.capacity_needed or '25 Workstation Seats',
            'budgetMin': float(i.budget_min) if i.budget_min else 0.0,
            'budgetMax': float(i.budget_max) if i.budget_max else 0.0
        })

    return render(request, 'admin_app/view_office_inquiries.html', {
        'inquiries': inquiries,
        'office_inquiries_json': json.dumps(inquiries_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_office_inquiries_api(request):
    try:
        from booking_manager.models import BookingInquiry
        from property_rentals.models import CommercialOffice
        import urllib.parse

        inquiries = BookingInquiry.objects.filter(category_type='office').order_by('-id')
        inquiries_data = []
        for i in inquiries:
            user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
            user_email = i.user.email if i.user and i.user.email else (i.email or 'N/A')
            user_phone = i.phone_number or '+91 97654 32109'
            
            office = CommercialOffice.objects.filter(pk=i.item_id).first() if i.item_id else CommercialOffice.objects.filter(name__icontains=i.item_title).first()
            
            location = office.location if office and office.location else i.location_preference or 'Palace Road, Bhavnagar'
            rent = f"₹{office.monthly_rent:,.0f}" if office else f"₹{i.budget_min:,.0f} - ₹{i.budget_max:,.0f}" if i.budget_max else "₹75,000"
            staff = i.capacity_needed or (f"{office.workstations} Workstations" if office else "25 Seats")
            business = i.duration or 'IT Tech Suite'
            move_in = i.booking_date or 'Possession Pending'
            map_url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
            
            inquiries_data.append({
                'id': i.id,
                'suite': i.item_title or (office.name if office else 'Commercial Office Space'),
                'location': location,
                'name': user_name,
                'phone': user_phone,
                'displayPhone': user_phone,
                'email': user_email,
                'business': business,
                'staff': staff,
                'moveIn': move_in,
                'rent': rent,
                'status': i.status or 'Pending',
                'image': i.image_url,
                'mapUrl': map_url,
                'req': i.special_requirements or 'No special requirements specified.',
                'quotedPrice': float(i.quoted_price) if i.quoted_price else 0.0,
                'representativeName': i.representative_name or '',
                'representativePhone': i.representative_phone or '',
                'meetingLocation': i.meeting_location or '',
                'adminNotes': i.admin_notes or '',
                'duration': i.duration or '12 Months Lease',
                'capacityNeeded': i.capacity_needed or '25 Workstation Seats',
                'budgetMin': float(i.budget_min) if i.budget_min else 0.0,
                'budgetMax': float(i.budget_max) if i.budget_max else 0.0
            })

        return JsonResponse({'status': 'success', 'inquiries': inquiries_data, 'count': len(inquiries_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_view_feedback_page(request):
    from booking_manager.models import BookingInquiry

    inquiries = BookingInquiry.objects.filter(category_type='feedback').order_by('-id')
    feedback_data = []
    for i in inquiries:
        user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
        category = i.guests_or_km if i.guests_or_km else 'Car'
        
        feedback_data.append({
            'id': i.id,
            'name': user_name,
            'rating': 5.0,
            'category': category.capitalize() if category else 'Car',
            'text': i.special_requirements or i.item_title or 'Great service & smooth experience!'
        })

    return render(request, 'admin_app/view_feedback.html', {
        'inquiries': inquiries,
        'feedback_json': json.dumps(feedback_data)
    })

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_feedback_api(request):
    try:
        from booking_manager.models import BookingInquiry

        inquiries = BookingInquiry.objects.filter(category_type='feedback').order_by('-id')
        feedback_data = []
        for i in inquiries:
            user_name = i.user.get_full_name() if i.user and i.user.get_full_name() else (i.user.username if i.user else i.applicant_name or 'Customer')
            category = i.guests_or_km if i.guests_or_km else 'Car'
            
            feedback_data.append({
                'id': i.id,
                'name': user_name,
                'rating': 5.0,
                'category': category.capitalize() if category else 'Car',
                'text': i.special_requirements or i.item_title or 'Great service & smooth experience!'
            })

        return JsonResponse({'status': 'success', 'feedback': feedback_data, 'count': len(feedback_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_hall_page(request):
    return render(request, 'admin_app/edit_hall.html')

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_house_page(request):
    return render(request, 'admin_app/edit_house.html')

@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_edit_office_page(request):
    return render(request, 'admin_app/edit_office.html')


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_categories_page(request):
    from vehicle_rentals.models import Car, Bike, VehicleCategory
    from django.contrib import messages

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
                messages.success(request, f"New category '{name}' for {vehicle_type.upper()} created! Add vehicles to this category to make it active on client pages.")
            else:
                messages.info(request, f"Category '{name}' already exists.")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f"Category '{name}' added successfully!"})

            return redirect('/admin-portal/manage-categories/')

    car_categories = VehicleCategory.objects.filter(vehicle_type='car').order_by('-created_at')
    bike_categories = VehicleCategory.objects.filter(vehicle_type='bike').order_by('-created_at')

    # Categories currently active on vehicles
    active_car_cats = sorted(list(set(Car.objects.values_list('category', flat=True).distinct())))
    active_bike_cats = sorted(list(set(Bike.objects.values_list('category', flat=True).distinct())))

    context = {
        'car_categories': car_categories,
        'bike_categories': bike_categories,
        'active_car_cats': active_car_cats,
        'active_bike_cats': active_bike_cats,
    }
    return render(request, 'admin_app/manage_categories.html', context)





@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_verifications_page(request):
    from user_accounts.models import UserProfile
    from booking_manager.models import BookingInquiry
    from django.utils import timezone

    profiles = UserProfile.objects.select_related('user').all().order_by('-created_at')
    
    verifications_data = []
    for p in profiles:
        user_name = p.user.get_full_name() or p.user.username
        email = p.user.email
        phone = p.phone_number or 'N/A'
        pending_bookings_count = BookingInquiry.objects.filter(
            user=p.user, status='Pending'
        ).count()
        
        verifications_data.append({
            'user_id': p.user.id,
            'profile_id': p.id,
            'username': p.user.username,
            'fullname': user_name,
            'email': email,
            'phone': phone,
            'role': p.role,
            'verification_status': p.verification_status,
            'id_document_type': p.id_document_type,
            'id_number': p.id_number or 'Not Submitted',
            'document_file': p.document_file or '',
            'rejection_reason': p.rejection_reason or '',
            'verified_at': p.verified_at.strftime('%Y-%m-%d %H:%M') if p.verified_at else 'N/A',
            'pending_bookings_count': pending_bookings_count,
            'date_joined': p.user.date_joined.strftime('%Y-%m-%d'),
        })

    return render(request, 'admin_app/manage_verifications.html', {
        'profiles': profiles,
        'verifications_json': json.dumps(verifications_data)
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_update_verification_api(request):
    if request.method == 'POST':
        try:
            from user_accounts.models import UserProfile
            from booking_manager.models import BookingInquiry
            from django.utils import timezone

            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            user_id = data.get('user_id')
            action = data.get('action', '').strip().lower() # 'approve' or 'reject'
            rejection_reason = data.get('rejection_reason', '').strip()

            if user_id and str(user_id).isdigit():
                profile = UserProfile.objects.filter(user_id=int(user_id)).first()
                if profile:
                    if action == 'approve':
                        profile.verification_status = 'Verified'
                        profile.verified_at = timezone.now()
                        profile.rejection_reason = ''
                        profile.save()

                        # Auto approve pending bookings for this verified user if requested
                        auto_approve_bookings = data.get('auto_approve_bookings', False)
                        if auto_approve_bookings:
                            BookingInquiry.objects.filter(user=profile.user, status='Pending').update(status='Approved')

                        return JsonResponse({
                            'status': 'success',
                            'message': f"Verification APPROVED for {profile.user.get_full_name() or profile.user.username}!",
                            'verification_status': 'Verified'
                        })
                    elif action == 'reject':
                        profile.verification_status = 'Rejected'
                        profile.rejection_reason = rejection_reason or 'Invalid or unreadable document uploaded.'
                        profile.save()

                        return JsonResponse({
                            'status': 'success',
                            'message': f"Verification REJECTED for {profile.user.get_full_name() or profile.user.username}.",
                            'verification_status': 'Rejected'
                        })
            return JsonResponse({'status': 'error', 'message': 'User profile not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_manage_payments_page(request):
    from booking_manager.models import BookingInquiry
    inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike', 'Car', 'Bike']).order_by('-id')
    bookings_data = [helper_build_booking_dict(i) for i in inquiries]

    return render(request, 'admin_app/manage_payments.html', {
        'inquiries': inquiries,
        'bookings_json': json.dumps(bookings_data)
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_verify_showroom_otp_api(request):
    if request.method == 'POST':
        try:
            from booking_manager.models import BookingInquiry
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            inquiry_id = data.get('id') or data.get('inquiry_id')
            submitted_otp = str(data.get('otp', '')).strip()

            inquiry = BookingInquiry.objects.filter(pk=inquiry_id).first()
            if not inquiry:
                return JsonResponse({'status': 'error', 'message': 'Booking inquiry not found.'}, status=404)

            expected_otp = str(inquiry.showroom_otp or (100000 + (inquiry.id * 73) % 899999)).strip()
            if submitted_otp and submitted_otp != expected_otp:
                return JsonResponse({'status': 'error', 'message': f'Invalid OTP entered! Expected: {expected_otp}'}, status=400)

            inquiry.extra_fee_status = 'Paid at Showroom'
            inquiry.extra_fee_payment_mode = 'Cash at Showroom'
            inquiry.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Showroom cash payment confirmed & verified successfully!',
                'extra_fee_status': inquiry.extra_fee_status
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required.'}, status=405)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_live_payments_api(request):
    try:
        from booking_manager.models import BookingInquiry
        inquiries = BookingInquiry.objects.filter(category_type__in=['car', 'bike', 'Car', 'Bike']).order_by('-id')
        bookings_data = [helper_build_booking_dict(i) for i in inquiries]
        return JsonResponse({'status': 'success', 'payments': bookings_data, 'count': len(bookings_data)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

