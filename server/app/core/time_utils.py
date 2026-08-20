from datetime import datetime, timezone


def utc_now() -> datetime:
    """מחזיר את הזמן הנוכחי כ-datetime מודע לאזור זמן (UTC)."""
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime | None) -> datetime | None:
    """
    מנרמל datetime ל-UTC כדי למנוע השוואה בין נאיבי למודע.
    קלט נאיבי (למשל query param בלי אזור זמן) נחשב כ-UTC.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
