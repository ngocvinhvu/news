from beanie import Document, Granularity, TimeSeriesConfig, Indexed
from pydantic import Field
from datetime import datetime


class BasedDocument(Document):
    created: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    updated: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    deleted: bool = False

    class Settings:
        _created_timeseries = TimeSeriesConfig(
            time_field="created",  # Required
            granularity=Granularity.hours,  # Optional
            expire_after_seconds=2  # Optional
        )

        _updated_timeseries = TimeSeriesConfig(
            time_field="updated",  # Required
            granularity=Granularity.hours,  # Optional
            expire_after_seconds=2  # Optional
        )
