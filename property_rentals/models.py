from django.db import models

class EventHall(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Under Maintenance'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='Marriage Banquet')
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2)
    capacity = models.IntegerField(default=500)
    ac_type = models.CharField(max_length=50, default='Central AC')
    parking = models.CharField(max_length=100, default='150 Vehicles')
    catering_policy = models.CharField(max_length=100, default='In-House Pure Veg')
    stage_dj_setup = models.CharField(max_length=200, default='LED Stage Screen + DJ Console Included')
    location = models.CharField(max_length=255)
    amenities = models.TextField(blank=True, default='2 Luxury AC Bridal Rooms, 24/7 Power Backup, Valet Parking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.TextField(blank=True, default='/static/images/image/c1.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class House(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Rented', 'Rented'),
        ('Maintenance', 'Under Maintenance'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='Luxury Villa')
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField(default=3)
    bathrooms = models.IntegerField(default=3)
    area_sqft = models.CharField(max_length=50, default='2400 sq.ft')
    furnishing = models.CharField(max_length=50, default='Fully Furnished')
    parking = models.CharField(max_length=100, default='2 Car Covered Garage')
    location = models.CharField(max_length=255)
    amenities = models.TextField(blank=True, default='Private Swimming Pool, Solar Power, 24/7 Gated Security')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.TextField(blank=True, default='/static/images/image/c1.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CommercialOffice(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Under Maintenance'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='IT Tech Suite')
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    workstations = models.IntegerField(default=25)
    conference_rooms = models.IntegerField(default=2)
    area_sqft = models.CharField(max_length=50, default='1800 sq.ft')
    ac_type = models.CharField(max_length=50, default='VRV Central AC')
    parking = models.CharField(max_length=100, default='4 Underground Slots')
    location = models.CharField(max_length=255)
    amenities = models.TextField(blank=True, default='High-Speed Fiber Internet, Server Room, Pantry, 24/7 Biometric Access')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    image = models.TextField(blank=True, default='/static/images/image/c1.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
