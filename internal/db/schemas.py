from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, Field
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
)

from internal.db.models import Cities, Customers, Subscriptions
from internal.validators import GeoFloat


class Message(BaseModel):
    detail: str


if TYPE_CHECKING:

    class Customer_Pydantic(Customers, BaseModel):
        pass

else:
    Customer_Pydantic = pydantic_model_creator(
        Customers,
        name="Customers",
    )


class Cust(Customer_Pydantic):
    pass


if TYPE_CHECKING:

    class CustomerIn_Pydantic(Customers, BaseModel):
        pass

else:
    CustomerIn_Pydantic = pydantic_model_creator(
        Customers,
        name="CustomersIn",
        exclude_readonly=True,
    )


class CustIn(CustomerIn_Pydantic):
    current_geo_lat: float = Field(le=90, ge=-90, default=None)
    current_geo_long: float = Field(le=180, ge=-180, default=None)
    selected_geo_lat: float = Field(le=90, ge=-90)
    selected_geo_long: float = Field(le=180, ge=-180)
    locale: str = Field(max_length=2, default="ru")


if TYPE_CHECKING:

    class Subscription_Pydantic(Subscriptions, BaseModel):
        pass

else:
    Subscription_Pydantic = pydantic_model_creator(
        Subscriptions,
        name="Subscriptions",
    )


class Sub(Subscription_Pydantic):
    pass


if TYPE_CHECKING:

    class SubscriptionIn_Pydantic(Subscriptions, BaseModel):
        pass

else:
    SubscriptionIn_Pydantic = pydantic_model_creator(
        Subscriptions,
        name="SubscriptionsIn",
        exclude_readonly=True,
    )


class SubIn(SubscriptionIn_Pydantic):
    cust_id: int = Field(gt=0)
    email: EmailStr = Field(max_length=255)


if TYPE_CHECKING:

    class City_Pydantic(Cities, BaseModel):
        pass

else:
    City_Pydantic = pydantic_model_creator(
        Cities,
        name="Cities",
    )


class City(City_Pydantic):
    pass


if TYPE_CHECKING:

    class CityIn_Pydantic(Cities, BaseModel):
        pass

else:
    CityIn_Pydantic = pydantic_model_creator(
        Cities,
        name="CitiesIn",
        exclude_readonly=True,
    )


class CityIn(CityIn_Pydantic):
    name: str = Field(max_length=255)
    lat: GeoFloat = Field(le=90, ge=-90)
    long: GeoFloat = Field(le=180, ge=-180)
