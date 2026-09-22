import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import EventHall
from booking_manager.models import BookingInquiry

def seed_default_halls_if_needed():
    pass

def hallrent_page(request):
    seed_default_halls_if_needed()
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

    available_halls = EventHall.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_halls.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))

    return render(request, 'property_rentals/hallrent.html', {
        'halls': halls,
        'halls_json': json.dumps(halls_data),
        'available_categories': available_categories,
        'available_categories_json': json.dumps(available_categories),
    })

def client_live_halls_api(request):
    seed_default_halls_if_needed()
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
    available_halls = EventHall.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_halls.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))
    return JsonResponse({
        'status': 'success',
        'halls': halls_data,
        'available_categories': available_categories,
        'count': len(halls_data)
    })

def create_hall_inquiry_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name') or data.get('full_name') or 'Customer'
            phone = data.get('phone') or data.get('phone_number') or '+91 98765 43210'
            email = data.get('email', '')
            inquiry_type = 'hall' # Fixed to Event Hall

            hall_id = int(data.get('hall_id', 0)) if str(data.get('hall_id', 0)).isdigit() else 0
            hall_title = data.get('hall_title') or data.get('property_title') or 'Event Banquet Hall'
            
            try:
                num_days = int(data.get('num_days', 1))
            except (ValueError, TypeError):
                num_days = 1

            start_date = data.get('start_date') or data.get('event_date') or data.get('preferred_date') or '2026-10-15'
            end_date = data.get('end_date') if num_days > 1 else start_date
            hours_needed = data.get('hours_needed', '') if num_days == 1 else ''

            if num_days == 1:
                duration_str = f"1 Day ({hours_needed})" if hours_needed else "1 Day"
                booking_date_display = start_date
            else:
                duration_str = f"{num_days} Days ({start_date} to {end_date})"
                booking_date_display = f"{start_date} to {end_date}"

            capacity_needed = data.get('capacity_needed') or data.get('guest_count') or data.get('guests') or '500 Guests'
            
            try:
                budget_min = float(data.get('budget_min', 0))
            except (ValueError, TypeError):
                budget_min = 0.0

            try:
                budget_max = float(data.get('budget_max', 0))
            except (ValueError, TypeError):
                budget_max = 0.0

            location_preference = data.get('location_preference') or data.get('location') or 'Bhavnagar Central Sector'
            requirements = data.get('requirements') or data.get('special_requirements') or 'Banquet Hall booking inquiry'
            
            user = request.user if request.user.is_authenticated else None

            inquiry = BookingInquiry.objects.create(
                user=user,
                category_type='hall',
                inquiry_type='hall',
                item_title=hall_title,
                item_id=hall_id,
                applicant_name=name,
                phone_number=phone,
                email=email,
                num_days=num_days,
                start_date=start_date,
                end_date=end_date,
                hours_needed=hours_needed,
                booking_date=booking_date_display,
                appointment_time=f"{booking_date_display} (Scheduled)",
                duration=duration_str,
                capacity_needed=capacity_needed,
                budget_min=budget_min,
                budget_max=budget_max,
                location_preference=location_preference,
                guests_or_km=capacity_needed,
                special_requirements=requirements,
                status='Pending'
            )
            return JsonResponse({'status': 'success', 'inquiry_id': inquiry.id, 'message': 'Hall inquiry submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

def hall_details_page(request):
    return render(request, 'property_rentals/hall_details.html')

def hall_inquiry_page(request):
    return render(request, 'property_rentals/hall_inquiry.html')

# === HOUSE RENTALS ===
def seed_default_houses_if_needed():
    pass

def houserent_page(request):
    from .models import House
    seed_default_houses_if_needed()
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
    available_houses = House.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_houses.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))
    return render(request, 'property_rentals/houserent.html', {
        'houses': houses,
        'houses_json': json.dumps(houses_data),
        'available_categories': available_categories,
        'available_categories_json': json.dumps(available_categories),
    })

def client_live_houses_api(request):
    from .models import House
    seed_default_houses_if_needed()
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
    available_houses = House.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_houses.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))
    return JsonResponse({'status': 'success', 'houses': houses_data, 'available_categories': available_categories, 'count': len(houses_data)})

def create_house_inquiry_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name') or data.get('full_name') or 'Customer'
            phone = data.get('phone') or data.get('phone_number') or '+91 98765 43210'
            email = data.get('email', '')
            house_id = int(data.get('house_id', 0)) if str(data.get('house_id', 0)).isdigit() else 0
            house_title = data.get('house_title') or data.get('property_title') or 'Residential House Rental'
            movein_date = data.get('movein_date') or data.get('preferred_date') or '2026-11-01'
            lease_months = data.get('lease_duration') or '6 Months'
            occupants = data.get('occupants') or data.get('capacity_needed') or '4 Occupants'
            furnishing = data.get('furnishing') or 'Fully Furnished'
            
            try:
                budget_min = float(data.get('budget_min', 0))
            except (ValueError, TypeError):
                budget_min = 0.0

            try:
                budget_max = float(data.get('budget_max', 0))
            except (ValueError, TypeError):
                budget_max = 0.0

            location_preference = data.get('location_preference') or data.get('location') or 'Palace Road, Bhavnagar'
            requirements = data.get('requirements') or f"Residential house lease query ({furnishing}, {occupants})"
            
            user = request.user if request.user.is_authenticated else None

            inquiry = BookingInquiry.objects.create(
                user=user,
                category_type='house',
                inquiry_type='house',
                item_title=house_title,
                item_id=house_id,
                applicant_name=name,
                phone_number=phone,
                email=email,
                start_date=movein_date,
                end_date=f"+{lease_months}",
                booking_date=movein_date,
                appointment_time=f"{movein_date} (Scheduled Move-in)",
                duration=f"{lease_months} ({furnishing})",
                capacity_needed=occupants,
                budget_min=budget_min,
                budget_max=budget_max,
                location_preference=location_preference,
                guests_or_km=occupants,
                special_requirements=requirements,
                status='Pending'
            )
            return JsonResponse({'status': 'success', 'inquiry_id': inquiry.id, 'message': 'House inquiry submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

def house_details_page(request):
    return render(request, 'property_rentals/house_details.html')


# === COMMERCIAL OFFICE RENTALS ===
def seed_default_offices_if_needed():
    pass

def officerent_page(request):
    from .models import CommercialOffice
    seed_default_offices_if_needed()
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
    available_offices = CommercialOffice.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_offices.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))
    return render(request, 'property_rentals/officerent.html', {
        'offices': offices,
        'offices_json': json.dumps(offices_data),
        'available_categories': available_categories,
        'available_categories_json': json.dumps(available_categories),
    })

def client_live_offices_api(request):
    from .models import CommercialOffice
    seed_default_offices_if_needed()
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
    available_offices = CommercialOffice.objects.filter(status='Available')
    available_categories = sorted(list(set([c.strip() for c in available_offices.exclude(category='').values_list('category', flat=True).distinct() if c and c.strip()])))
    return JsonResponse({'status': 'success', 'offices': offices_data, 'available_categories': available_categories, 'count': len(offices_data)})

def create_office_inquiry_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            name = data.get('name') or data.get('full_name') or 'Customer'
            phone = data.get('phone') or data.get('phone_number') or '+91 98765 43210'
            email = data.get('email', '')
            office_id = int(data.get('office_id', 0)) if str(data.get('office_id', 0)).isdigit() else 0
            office_title = data.get('office_title') or data.get('property_title') or 'Commercial Office Space'
            possession_date = data.get('possession_date') or data.get('preferred_date') or '2026-11-15'
            lease_term = data.get('lease_term') or data.get('lease_duration') or '12 Months'
            staff_seats = data.get('staff_seats') or data.get('capacity_needed') or '30 Workstation Seats'
            office_layout = data.get('office_layout') or 'IT Tech Suite'
            
            try:
                budget_min = float(data.get('budget_min', 0))
            except (ValueError, TypeError):
                budget_min = 0.0

            try:
                budget_max = float(data.get('budget_max', 0))
            except (ValueError, TypeError):
                budget_max = 0.0

            location_preference = data.get('location_preference') or data.get('location') or 'Palace Road, Bhavnagar'
            requirements = data.get('requirements') or f"Commercial office lease inquiry ({office_layout}, {staff_seats})"
            
            user = request.user if request.user.is_authenticated else None

            inquiry = BookingInquiry.objects.create(
                user=user,
                category_type='office',
                inquiry_type='office',
                item_title=office_title,
                item_id=office_id,
                applicant_name=name,
                phone_number=phone,
                email=email,
                start_date=possession_date,
                end_date=f"+{lease_term}",
                booking_date=possession_date,
                appointment_time=f"{possession_date} (Scheduled Possession)",
                duration=f"{lease_term} ({office_layout})",
                capacity_needed=staff_seats,
                budget_min=budget_min,
                budget_max=budget_max,
                location_preference=location_preference,
                guests_or_km=staff_seats,
                special_requirements=requirements,
                status='Pending'
            )
            return JsonResponse({'status': 'success', 'inquiry_id': inquiry.id, 'message': 'Office inquiry submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST method required.'}, status=405)

def office_details_page(request):
    return render(request, 'property_rentals/office_details.html')
