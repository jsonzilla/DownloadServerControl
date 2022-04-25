from datetime import datetime
from fastapi import HTTPException, status

DEFAULT_FORMAT_UTC = "%Y-%m-%d %H:%M:%S.%f"


class DatetimeCodec(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v is None:
            return v
        d = datetime.strptime(v, DEFAULT_FORMAT_UTC)
        if d is None:
            raise ValueError("Invalid date")
        return d.timestamp().isoformat()

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def now_in_range(begin: str, end: str):
    return _validate_datetime(
        _convert_datetime_to_timestamp(begin),
        _convert_datetime_to_timestamp(end)
    )


def _validate_datetime(begin: float, end: float):
    now: float = datetime.utcnow().timestamp()
    return begin < now and end > now


def _convert_datetime_to_timestamp(date_str: str):
    try:
        return datetime.strptime(date_str, DEFAULT_FORMAT_UTC).timestamp()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect data format, should be YYYY-MM-DD HH:MM:SS.sss UTC")
