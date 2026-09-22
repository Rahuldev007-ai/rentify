from django.db import models
from django.contrib.auth.models import User

class BookingInquiry(models.Model):
    CATEGORY_CHOICES = (
        ('car', 'Car Rental'),
        ('bike', 'Bike Rental'),
        ('hall', 'Event Hall'),
        ('house', 'Residential House'),
        ('office', 'Commercial Office'),
        ('feedback', 'Customer Feedback'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='car')
    item_title = models.CharField(max_length=200)
    item_id = models.IntegerField(default=0)
    
    applicant_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    
    booking_date = models.CharField(max_length=100, blank=True, null=True)
    appointment_time = models.CharField(max_length=100, blank=True, null=True)
    guests_or_km = models.CharField(max_length=100, blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    
    payment_method = models.CharField(max_length=50, default='COD at Showroom')
    payment_status = models.CharField(max_length=50, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    # Extra Driven KM Fee & Settlement Fields
    extra_km_driven = models.IntegerField(default=0)
    extra_km_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    extra_fee_status = models.CharField(max_length=50, default='No Extra Fee') # Choices: 'No Extra Fee', 'Pending Payment', 'Paid Online', 'Paid at Showroom', 'Settlement Confirmed'
    extra_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    showroom_otp = models.CharField(max_length=10, blank=True, null=True)
    extra_fee_payment_mode = models.CharField(max_length=50, default='Razorpay')

    # Property Inquiry Specific Parameters
    inquiry_type = models.CharField(max_length=20, default='hall')
    num_days = models.IntegerField(default=1)
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    hours_needed = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    capacity_needed = models.CharField(max_length=100, blank=True, null=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    location_preference = models.CharField(max_length=200, blank=True, null=True)

    # Admin Response & Meeting Scheduling Fields
    representative_name = models.CharField(max_length=150, blank=True, null=True)
    representative_phone = models.CharField(max_length=30, blank=True, null=True)
    meeting_type = models.CharField(max_length=50, default='Google Meet')
    meeting_location = models.CharField(max_length=300, blank=True, null=True)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    admin_notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category_type.upper()} Inquiry - {self.applicant_name} ({self.status})"

    @property
    def image_url(self):
        title_lower = (self.item_title or '').lower()
        if self.category_type == 'car':
            from vehicle_rentals.models import Car
            car = Car.objects.filter(pk=self.item_id).first()
            if car and car.image:
                return car.image
            if 'thar' in title_lower:
                return '/static/images/image/carimgs/thar1.jpg'
            if 'creta' in title_lower:
                return '/static/images/image/car2.jpg'
            if 'audi' in title_lower:
                return '/static/images/image/carimgs/audi.avif'
            if 'verna' in title_lower:
                return '/static/images/image/carimgs/verna1.jpg'
            if 'swift' in title_lower:
                return '/static/images/image/carimgs/swift1.jpg'
            if 'fortuner' in title_lower:
                return '/static/images/image/carimgs/i20.jpg'
            return '/static/images/image/carimgs/thar1.jpg'
        elif self.category_type == 'bike':
            from vehicle_rentals.models import Bike
            bike = Bike.objects.filter(pk=self.item_id).first()
            if bike and bike.image:
                return bike.image
            if 'bullet' in title_lower:
                return '/static/images/image/bikeimg/bullet.jpg'
            if 'hunter' in title_lower:
                return '/static/images/image/bikeimg/hunter.jpg'
            if 'jawa' in title_lower:
                return '/static/images/image/bikeimg/jawa1.jpg'
            if 'duke' in title_lower:
                return '/static/images/image/bikeimg/duke.jpg'
            if 'hayabusa' in title_lower:
                return '/static/images/image/bikeimg/hayabusa.jpg'
            if 'r15' in title_lower:
                return '/static/images/image/bikeimg/r15.jpg'
            return '/static/images/image/bikeimg/bullet.jpg'
        elif self.category_type == 'hall':
            from property_rentals.models import EventHall
            hall = EventHall.objects.filter(pk=self.item_id).first() or EventHall.objects.filter(name__icontains=self.item_title).first()
            if hall and hall.image:
                return hall.image
            return '/static/images/image/c1.jpg'
        elif self.category_type == 'house':
            from property_rentals.models import House
            house = House.objects.filter(pk=self.item_id).first() or House.objects.filter(name__icontains=self.item_title).first()
            if house and house.image:
                return house.image
            return '/static/images/image/houseimg/i1.jpg'
        elif self.category_type == 'office':
            from property_rentals.models import CommercialOffice
            office = CommercialOffice.objects.filter(pk=self.item_id).first() or CommercialOffice.objects.filter(name__icontains=self.item_title).first()
            if office and office.image:
                return office.image
            return '/static/images/image/officeimg/o1.jpg'
        return '/static/images/image/c1.jpg'

