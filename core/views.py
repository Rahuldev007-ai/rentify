from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from vehicle_rentals.models import Car, Bike
from property_rentals.models import EventHall, House, CommercialOffice
from booking_manager.models import BookingInquiry

def home_page(request):
    featured_cars = Car.objects.all()[:3]
    featured_bikes = Bike.objects.all()[:3]
    featured_halls = EventHall.objects.all()[:2]
    featured_houses = House.objects.all()[:2]
    featured_offices = CommercialOffice.objects.all()[:2]
    
    total_cars_count = Car.objects.count()
    total_bikes_count = Bike.objects.count()
    total_properties_count = (
        EventHall.objects.count() + House.objects.count() + CommercialOffice.objects.count()
    )

    context = {
        'featured_cars': featured_cars,
        'featured_bikes': featured_bikes,
        'featured_halls': featured_halls,
        'featured_houses': featured_houses,
        'featured_offices': featured_offices,
        'total_cars_count': total_cars_count,
        'total_bikes_count': total_bikes_count,
        'total_properties_count': total_properties_count,
    }
    return render(request, 'core/one.html', context)


def aboutus_page(request):
    return render(request, 'core/aboutus.html')


def gallery_page(request):
    return render(request, 'core/gallery.html')


def feedback_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        BookingInquiry.objects.create(
            user=request.user if request.user.is_authenticated else None,
            category_type='feedback',
            item_title='Customer Feedback',
            applicant_name=name or 'Anonymous User',
            email=email,
            special_requirements=message,
            status='Approved'
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Thank you for your valuable feedback!'})

        messages.success(request, 'Thank you for your valuable feedback!')
        return redirect('/feedback/')

    return render(request, 'core/feedback.html')


def search_suggestions_api(request):
    query = request.GET.get('q', '').strip().lower()
    if not query:
        return JsonResponse({'status': 'success', 'results': []})

    results = []

    cars = Car.objects.filter(name__icontains=query)[:4]
    for c in cars:
        results.append({
            'title': c.name,
            'category': 'Car',
            'status': c.status,
            'price': f"₹{c.price_per_day:,.0f}/day",
            'url': f"/vehicles/car-details/?id={c.id}",
            'image': c.image or '/static/images/image/carimgs/thar1.jpg'
        })

    bikes = Bike.objects.filter(name__icontains=query)[:4]
    for b in bikes:
        results.append({
            'title': b.name,
            'category': 'Bike',
            'status': b.status,
            'price': f"₹{b.price_per_day:,.0f}/day",
            'url': f"/vehicles/bike-details/?id={b.id}",
            'image': b.image or '/static/images/image/bikeimg/bullet.jpg'
        })

    halls = EventHall.objects.filter(name__icontains=query)[:3]
    for h in halls:
        results.append({
            'title': h.name,
            'category': 'Hall',
            'status': h.status,
            'price': f"₹{h.price_per_day:,.0f}/day",
            'url': "/properties/halls/",
            'image': h.image or '/static/images/image/c1.jpg'
        })

    houses = House.objects.filter(name__icontains=query)[:3]
    for house in houses:
        results.append({
            'title': house.name,
            'category': 'House',
            'status': house.status,
            'price': f"₹{house.monthly_rent:,.0f}/mo",
            'url': "/properties/houses/",
            'image': house.image or '/static/images/image/c1.jpg'
        })

    offices = CommercialOffice.objects.filter(name__icontains=query)[:3]
    for o in offices:
        results.append({
            'title': o.name,
            'category': 'Office',
            'status': o.status,
            'price': f"₹{o.monthly_rent:,.0f}/mo",
            'url': "/properties/offices/",
            'image': o.image or '/static/images/image/c1.jpg'
        })

    return JsonResponse({'status': 'success', 'results': results})

