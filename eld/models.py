from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


# Create superuser with email instead of username
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(default="/default.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def is_company(self):
        try:
            return bool(Company.objects.get(email=self.email))
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return self.email


class Company(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=100, unique=True)
    usdot = models.IntegerField()
    time_zone = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    image = models.ForeignKey(CustomUser, models.CASCADE)
    org_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} & {self.email}"

    class Meta:
        verbose_name_plural = "Companies"


class VehicleManager(models.Manager):
    def for_company(self, user):
        # try:
        if not user.is_company():
            user = DRIVERS.objects.get(email=user)
            client = Company.objects.get(id=user.company_id)
        else:
            client = Company.objects.get(email=user)
        # except ObjectDoesNotExist:
        #     return None

        # print(client)
        return self.filter(company_id=client.id)


class ELD(models.Model):
    serial_number = models.CharField(max_length=30)
    notes_eld = models.CharField(blank=True, null=True, default='', max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    objects = VehicleManager()

    def __str__(self):
        return self.serial_number


class Vehicle(models.Model):
    vehicle_id = models.CharField(unique=True, max_length=200)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    license_plate_num = models.IntegerField(unique=True)
    license_plate_issue_state = models.CharField(max_length=100)
    vin = models.CharField(blank=True, max_length=30, null=True)
    eld_id = models.OneToOneField(ELD, unique=True, on_delete=models.CASCADE)
    notes_vehicle = models.CharField(blank=True, null=True, default='', max_length=200)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    objects = VehicleManager()

    def __str__(self):
        return self.model

class Trailer(models.Model):
    trailer_number = models.CharField(max_length=50)
    company = models.ForeignKey(Company, models.CASCADE)

    def __str__(self):
        return self.trailer_number

class Notes(models.Model):
    text = models.TextField()
    driver = models.ForeignKey("DRIVERS", models.CASCADE)


class DRIVERS(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    image = models.ForeignKey(CustomUser , on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=30)
    driver_license_number = models.CharField(max_length=250)
    dr_li_issue_state = models.CharField(max_length=100)
    co_driver = models.ForeignKey("self",on_delete=models.SET_NULL,blank=True, null=True)
    home_terminal_address = models.CharField(max_length=200, null=True, blank=True)
    home_terminal_time_zone = models.CharField(max_length=200)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE,)
    status = models.BooleanField(default=True)
    trail_number = models.ManyToManyField(Trailer,blank=True,null=True)
    enable_dr_eld = models.BooleanField(default=False)
    enable_dr_elog = models.BooleanField(default=False)
    allow_yard = models.BooleanField(default=False)
    allow_personal_c = models.BooleanField(default=False)
    activated = models.TimeField(auto_created=True, blank=True, null=True)
    terminated = models.TimeField(default=None, blank=True, null=True)
    app_version = models.CharField(max_length=200, blank=True, null=True)
    device_version = models.CharField(max_length=500, blank=True, null=True)
    main_office = models.CharField(max_length=700, null=True)
    company = models.ForeignKey("Company", models.CASCADE)
    objects = VehicleManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Drivers"


class RegisterCheck(models.Model):
    email = models.EmailField(unique=True)
    time = models.TimeField(default=None, blank=True, null=True)
    code = models.IntegerField()
    password = models.CharField(max_length=150)
    count = models.IntegerField(default=0)


class EventDriver(models.Model):
    engine_state = models.CharField(max_length=45, null=True, blank=True)
    vin = models.CharField(max_length=50, null=True, blank=True)
    speed_kmh = models.CharField(max_length=50, null=True, blank=True)
    odometer_km = models.CharField(max_length=50, null=True, blank=True)
    trip_distance_km = models.CharField(max_length=50, null=True, blank=True)
    hours = CharField(max_length=50, null=True, blank=True)
    trip_hours = CharField(max_length=50)
    voltage = CharField(max_length=50)
    date = models.DateTimeField()
    time = models.DateTimeField()
    latitude = CharField(max_length=50)
    longitude = CharField(max_length=50)
    gps_speed_kmh = CharField(max_length=50)
    course_deg = CharField(max_length=50)
    namsats = CharField(max_length=50)
    altitude = CharField(max_length=50)
    drop = CharField(max_length=50)
    sequence = CharField(max_length=50)
    firmware = CharField(max_length=50)
    driver = models.ForeignKey("DRIVERS", on_delete=models.CASCADE)

    def __str__(self):
        return self.driver




