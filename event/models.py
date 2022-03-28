
from django.db import models
from django.contrib.gis.db import models as md
import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions"
headers = {
    'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
    'x-rapidapi-key': "f1d17c9651msh1ec454d0575be47p14f413jsn324aaaf4458c"
}


# Cached records

class PowerOn(models.Model):
    hard_boots = models.CharField(max_length=100)
    crashes = models.CharField(max_length=100)
    time = models.DateTimeField()
    sequence_number = models.IntegerField()
    driver = models.ForeignKey('eld.DRIVERS', on_delete=models.CASCADE)



class NewTime(models.Model):
    previous_time = models.DateTimeField()
    time = models.DateTimeField()
    sequence_number = models.IntegerField()


class EngineCache(models.Model):
    choose_type = [
        ('engine_on', 1),
        ('engine_off', 2),
        ('newVin', 3),
    ]
    vin = models.CharField(max_length=150)
    odometer = models.FloatField()
    engine_hours = models.FloatField()
    time = models.BigIntegerField()
    sequence_number = models.IntegerField()
    type = models.IntegerField(choices=choose_type)  # this  cover 3 points(engineOn, engineOF, NewVine)

    class Meta:
        permissions = [
            ("driver", "can add status")
        ]


class MotionPeriodic(models.Model):
    choose_type = [
        (1, 'motion_start'),
        ('motion_stop', 2),
        ('periodic', 3),

    ]
    rpm = models.FloatField()
    speed = models.FloatField()
    odometer = models.FloatField()
    engineHours = models.FloatField()
    point = md.PointField()
    gps_speed = models.IntegerField()
    course = models.IntegerField(null=True)
    numsats = models.IntegerField(null=True)
    altitude = models.IntegerField(null=True)
    dop = models.FloatField(null=True)
    time = models.BigIntegerField(null=True)
    sequence_number = models.IntegerField(null=True)
    country = models.CharField(max_length=500, null=True, blank=True, editable=False)
    driver = models.ForeignKey("eld.DRIVERS", on_delete=models.CASCADE, null=True, blank=True)
    type = models.IntegerField(choices=choose_type)

    def save(self, *args, **kwargs):
        lat = str(self.point[0])
        long = str(self.point[1])
        querystring = {"location": f"{'+'+ long if float(long) > 0 else long}"
                                   f"{'+'+ lat if float(lat) > 0 else lat}"}

        response = requests.request("GET", url, headers=headers, params=querystring).json()['data'][0]
        self.country = response['country'] + " " + response['region'] + response['name']

        super(MotionPeriodic, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver} & {self.country}"


# Buffer Records
class BufferRecord(models.Model):
    sequence_start = models.IntegerField()
    sequence_end = models.IntegerField()
    total = models.IntegerField()
    storage = models.IntegerField()


# Live Records
class LiveData(models.Model):
    engine_state = models.BooleanField()
    vin = models.CharField(max_length=255)
    speed = models.FloatField()
    odometer = models.FloatField()
    trip_distance = models.FloatField()
    engine_hours = models.FloatField()
    trip_hours = models.FloatField()
    battery_voltage = models.FloatField()
    date = models.FloatField()
    point = md.PointField()
    gps_speed = models.IntegerField()
    course = models.IntegerField()
    number_of_satellites = models.IntegerField()
    altitude = models.FloatField()
    dop = models.FloatField()
    sequence_number = models.IntegerField()
    firmware_version = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey('eld.DRIVERS', models.CASCADE)
    truck = models.ForeignKey('eld.Vehicle', models.CASCADE, null=True)
    country = models.CharField(max_length=500, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        lat = str(self.point[0])
        long = str(self.point[1])
        querystring = {"location": f"{'+'+ long if float(long) > 0 else long}"
                                   f"{'+'+ lat if float(lat) > 0 else lat}"}

        response = requests.request("GET", url, headers=headers, params=querystring).json()['data'][0]
        self.country = response['country'] + " " + response['region'] + response['name']

        super(LiveData, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver_id}, {self.id}"


class DriverBehavior(models.Model):
    cruise_type = [
        ('cruise_accelerate', 1),
        ('cruise_accelerate_override', 2),
        ('cruise_decelerate', 3),
        ('cruise_hold', 4),
        ('cruise_invalid', 5),
        ('cruise_na', 6),
        ('cruise_off', 7),
        ('cruise_resume', 8),
        ('cruise_set', 9),
    ]
    seat_type = [
        ('belt_invalid', 1),
        ('belt_locked', 2),
        ('belt_na', 3),
        ('belt_unknown', 4),
        ('belt_unlocked', 5)
    ]
    abs_type = [
        ('abc_active', 1),
        ('abc_invalid', 2),
        ('abc_na', 3),
        ('abc_passive', 4),
        ('abc_reserved', 5)
    ]
    traction_type = [
        ('traction_error', 1),
        ('traction_invalid', 2),
        ('traction_na', 3),
        ('traction_off', 4),
        ('traction_on', 5)
    ]
    stability_type = [
        ('stability_active', 1),
        ('stability_invalid', 2),
        ('stability_na', 3),
        ('stability_passive', 4),
        ('stability_reserved', 5),
    ]
    cruise_control_speed = models.FloatField()
    cruise_control_status = models.SmallIntegerField(choices=cruise_type)  # 9 options
    throttle_position = models.FloatField()  # contain percent(%)
    acceleration_position = models.FloatField()
    brake = models.FloatField()
    seat = models.SmallIntegerField(choices=seat_type)  # contains 5 positions
    steering_wheel = models.FloatField()
    abc_status = models.SmallIntegerField(choices=abs_type)
    traction_status = models.SmallIntegerField(choices=traction_type)
    stability_status = models.SmallIntegerField(choices=stability_type)
    break_system_pressure = models.FloatField()


class Emission(models.Model):
    regeneration_type = [
        ('dpf_regen_active', 1),
        ('dpf_regen_invalid', 2),
        ('dpf_regen_na', 3),
        ('dpf_regen_not_active', 4),
        ('dpf_regen_passive', 5),
    ]
    scr_inducement_fault_type = [
        ('scrinducement_inactive', 1),
        ('scrinducement_invalid', 2),
        ('scrinducement_level_1', 3),
        ('scrinducement_level_2', 4),
        ('scrinducement_level_3', 5),
        ('scrinducement_level_4', 6),
        ('scrinducement_level_5', 7),
        ('scrinducement_na', 8),
        ('scrinducement_temporary_override', 9),
    ]
    nox_inlet = models.FloatField()
    nox_outlet = models.FloatField()
    ash_load = models.FloatField()
    dpf_soot = models.FloatField()
    dpf_regeneration = models.SmallIntegerField()
    dpf_differential_pressure = models.FloatField()
    egr_valve_position = models.FloatField()
    after_treatment_fuel_pressure = models.FloatField()
    engine_exhaust_temperature = models.FloatField()
    exhaust_temperature_1 = models.FloatField()
    exhaust_temperature_2 = models.FloatField()
    exhaust_temperature_3 = models.FloatField()
    def_level = models.FloatField()
    def_tank_temperature = models.FloatField()
    scr_inducement_fault_state = models.SmallIntegerField(choices=scr_inducement_fault_type)


class EngineRecordLive(models.Model):
    oil_pressure = models.FloatField()
    turbo_boost = models.FloatField()
    intake_pressure = models.FloatField()
    fuel_pressure = models.FloatField()
    load = models.FloatField()
    mass_air_flow = models.FloatField()
    turbo_rpm = models.FloatField()
    intake_temperature = models.FloatField()
    coolant_temperature = models.FloatField()
    oil_temperature = models.FloatField()
    fuel_temperature = models.FloatField()
    change_cooler_temperature = models.FloatField()
    torque = models.FloatField()
    oil_level = models.FloatField()
    coolant_level = models.FloatField()
    trip_fuel = models.FloatField()
    fuel_economy = models.FloatField()


class FuelRecord(models.Model):
    state_type = [
        ('bad', 1),
        ('good', 2),
        ('invalid', 3),
        ('normal', 4),
        ('terrible', 5),
        ('warming', 6),
    ]
    fuel_level = models.FloatField()
    integrated_fuel = models.FloatField()
    total_fuel_consumed = models.FloatField()
    fuel_rate = models.FloatField()
    idle_fuel_consumed = models.FloatField()
    idle_time = models.FloatField()
    high_rpm_state = models.SmallIntegerField(choices=state_type)
    unsteady_state = models.SmallIntegerField(choices=state_type)
    engine_power_state = models.SmallIntegerField(choices=state_type)
    accel_state = models.SmallIntegerField(choices=state_type)
    eco = models.SmallIntegerField(choices=state_type)
    anticipate_state = models.SmallIntegerField(choices=state_type)


class Transmission(models.Model):
    torque_converter_lockup_type = [
        ('torque_cnv_lockup_disengaged', 1),
        ('torque_cnv_lockup_engaged', 2),
        ('torque_cnv_lockup_error', 3),
        ('torque_cnv_lockup_invalid', 4),
        ('torque_cnv_lockup_na', 5),
    ]
    output_shaft_rpm = models.FloatField()
    gear = models.IntegerField()
    request_gear_status = models.IntegerField()
    transmission_oil_temperature = models.FloatField()
    torque_converter_lockup_status = models.SmallIntegerField(choices=torque_converter_lockup_type)


class DriverStatus(models.Model):
    mychoices = (
        ("OFF","OFF"),
        ("ON","ON"),
        ("SB","SB"),
        ("D","D")
    )
    driver = models.ForeignKey('eld.DRIVERS', models.CASCADE,related_name='driver_status')
    status = models.CharField(max_length=150,choices=mychoices)
    point = md.PointField(blank=True,null=True)
    note = models.TextField(blank=True)
    cr_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status} in {self.cr_time}"



class GeneralMain(models.Model):
    driver = models.ForeignKey('eld.DRIVERS', on_delete = models.SET_NULL,null=True)
    distance  = models.CharField(max_length=50)
    shipping_doc = models.CharField(max_length=150)
    vehicles = models.ForeignKey('eld.Vehicle', models.SET_NULL, null=True)
    trailers = models.ManyToManyField('eld.Trailer',null=True,blank=True)
    carrier = models.CharField(max_length=150)
    main_ofice = models.CharField(max_length=150)
    home_terminal_address = models.CharField(max_length=150)
    co_driver = models.CharField(max_length=150)
    from_address = models.CharField(max_length=150)
    to_address = models.CharField(max_length=150)
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
