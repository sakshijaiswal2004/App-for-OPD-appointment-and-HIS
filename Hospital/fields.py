from datetime import timedelta
from django.db.models import DateTimeField


class DateTruncMixin:

    def truncate_date(self, dt):
        return dt

    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            return self.truncate_date(value)
        return value


class MinuteDateTimeField(DateTruncMixin, DateTimeField):

    def truncate_date(self, dt):
        return dt.replace(second=0, microsecond=0)