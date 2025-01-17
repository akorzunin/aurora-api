from tortoise import fields, models
from tortoise.validators import MaxValueValidator, MinValueValidator

# Table customers
# id (primary key) uuid4
# current_geo_lat float (.1) = selected_geo_lat
# current_geo_long float (.1) = selected_geo_lon
# selected_geo_lat float (.1)
# selected_geo_long float (.1)
# locale string(2) #ch ru


class Customers(models.Model):
    id = fields.IntField(primary_key=True)
    current_geo_lat = fields.FloatField(
        null=True,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
    )
    current_geo_long = fields.FloatField(
        null=True,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
    )
    selected_geo_lat = fields.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
    )
    selected_geo_long = fields.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
    )
    locale = fields.CharField(max_length=2, default="ru")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "customers"


# Table subscriptions
# id (pk) # not used
# cust_id (foreign key)
# email string
# cust_name string
# cust_surname optional string
# cust_patronymic optional string
# cust_fullname = cust_name + cust_surname + cust_patronymic

# alert_probability int(0-100) # порог который выбран пользователем
# sub_type int # 1,2,3,4 тиры подписок (1 день 3 д 7д 30д)
# geo_push_type string (SELECTED | CURRENT)

# active boolean


class Subscriptions(models.Model):
    id = fields.UUIDField(primary_key=True)
    cust = fields.ForeignKeyField(
        "models.Customers",
        related_name="subscriptions",
    )  # cust_id in db
    email = fields.CharField(max_length=255, unique=True)
    cust_name = fields.CharField(max_length=255)
    cust_surname = fields.CharField(max_length=255, null=True)
    cust_patronymic = fields.CharField(max_length=255, null=True)

    def cust_fullname(self) -> str:
        return f"{self.cust_name} {self.cust_surname or ''} {self.cust_patronymic or ''}".strip()  # noqa: E501

    alert_probability = fields.IntField(min_value=0, max_value=100)
    sub_type = fields.IntField(min_value=1, max_value=4)
    geo_push_type = fields.CharField(
        max_length=255, choices=["SELECTED", "CURRENT"]
    )
    active = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "subscriptions"


class Cities(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    lat = fields.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
    )
    long = fields.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
    )
