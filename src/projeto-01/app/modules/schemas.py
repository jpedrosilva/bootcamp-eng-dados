import pandera as pa
from pandera.typing import Series


class ImportWeatherStationSchema(pa.SchemaModel):
    """
    Defines the schema for importing weather station data.

    Attributes:
        city (pandas.Series[str]): The city where the weather station is located.
        value (pandas.Series[float], optional): The value measured by the weather station,
            constrained to be greater than or equal to -1000 and less than or equal to 1000.

    Config:
        coerce (bool): Whether to coerce values to the specified types.
    """

    city: Series[str]
    value: Series[float] = pa.Field(ge=-1000, le=1000)

    class Config:
        coerce = True


class TransformWeatherStationSchema(pa.SchemaModel):
    """
    Schema for transforming weather station data.

    Attributes:
        city (Series[str]): The city name.
        max_value (Series[float]): The maximum temperature value.
        min_value (Series[float]): The minimum temperature value.
        avg_value (Series[float]): The average temperature value.

    Config:
        coerce (bool): Whether to coerce values to the specified types.
    """

    city: Series[str]
    max_value: Series[float]
    min_value: Series[float]
    avg_value: Series[float]

    class Config:
        coerce = True
