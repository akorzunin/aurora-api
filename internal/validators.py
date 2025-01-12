from typing import Annotated

from pydantic import AfterValidator


# https://xkcd.com/2170/
def round_to(ndigits: int) -> AfterValidator:
    return AfterValidator(lambda v: round(v, ndigits))


GeoFloat = Annotated[float, round_to(1)]
