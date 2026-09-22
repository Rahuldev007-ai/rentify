from django.db import models

class Car(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Under Maintenance'),
    )
    INSPECTION_CHOICES = (
        ('Verified', 'Verified'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, default='SUV')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    seats = models.IntegerField(default=5)
    transmission = models.CharField(max_length=20, default='Automatic')
    fuel_type = models.CharField(max_length=30, default='Petrol')
    start_km = models.IntegerField(default=10000)
    end_km = models.IntegerField(default=10200)
    allowed_km_per_day = models.IntegerField(default=150)
    extra_km_rate = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    inspection_status = models.CharField(max_length=30, choices=INSPECTION_CHOICES, default='Verified')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    description = models.TextField(blank=True, default='Feature-loaded vehicle for comfortable city commuting and highway road trips.')
    features = models.TextField(blank=True, default='4x4 Drive, Climate Control AC, Touchscreen Infotainment, Dual Airbags, ABS with EBD')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    image = models.TextField(blank=True, default='/static/images/image/carimgs/thar1.jpg')
    return_image = models.TextField(blank=True, default='/static/images/image/carimgs/thar1.jpg')

    # GPS Anti-Theft Protection Fields
    gps_lat = models.CharField(max_length=50, default='21.7645')
    gps_lng = models.CharField(max_length=50, default='72.1519')
    location_name = models.CharField(max_length=150, default='Bhavnagar Central Hub')
    engine_status = models.CharField(max_length=20, default='UNLOCKED')
    ignition_status = models.CharField(max_length=20, default='OFF')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Bike(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
        ('Maintenance', 'Under Maintenance'),
    )
    INSPECTION_CHOICES = (
        ('Verified', 'Verified'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, default='Cruiser')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    engine_cc = models.CharField(max_length=50, default='350cc')
    power_hp = models.CharField(max_length=50, default='20.2 BHP')
    average_mileage = models.CharField(max_length=50, default='38 kmpl')
    fuel_type = models.CharField(max_length=30, default='Petrol')
    start_km = models.IntegerField(default=5000)
    end_km = models.IntegerField(default=5200)
    allowed_km_per_day = models.IntegerField(default=120)
    extra_km_rate = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)
    inspection_status = models.CharField(max_length=30, choices=INSPECTION_CHOICES, default='Verified')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    description = models.TextField(blank=True, default='High performance two-wheeler built for smooth riding, excellent fuel efficiency, and road comfort.')
    features = models.TextField(blank=True, default='Dual Channel ABS, Electric Start, Digital Console, Alloy Wheels, Disc Brakes')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    image = models.TextField(blank=True, default='/static/images/image/bikeimg/bullet.jpg')
    return_image = models.TextField(blank=True, default='/static/images/image/bikeimg/bullet.jpg')

    # GPS Anti-Theft Protection Fields
    gps_lat = models.CharField(max_length=50, default='21.7645')
    gps_lng = models.CharField(max_length=50, default='72.1519')
    location_name = models.CharField(max_length=150, default='Bhavnagar Station Road')
    engine_status = models.CharField(max_length=20, default='UNLOCKED')
    ignition_status = models.CharField(max_length=20, default='OFF')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VehicleCategory(models.Model):
    CATEGORY_TYPES = (
        ('car', 'Car Category'),
        ('bike', 'Bike Category'),
    )

    name = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='car')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vehicle Categories"

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"


class VehicleFeature(models.Model):
    FEATURE_TYPES = (
        ('car', 'Car Feature'),
        ('bike', 'Bike Feature'),
    )

    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=FEATURE_TYPES, default='car')
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vehicle Features"

    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"



