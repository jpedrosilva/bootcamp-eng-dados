import pandera as pa
from pandera.typing import Series


class ImportWeatherStationSchema(pa.SchemaModel):
    city: Series[str]
    value: Series[float] = pa.Field(ge=-1000, le=1000)

    class Config:
        coerce = True


class TransformWeatherStationSchema(pa.SchemaModel):
    city: Series[str]
    max_value: Series[float]
    min_value: Series[float]
    avg_value: Series[float]

    class Config:
        coerce = True
