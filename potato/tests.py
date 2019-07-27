from django.test import TestCase

# Create your tests here.
from datetime import datetime, timedelta, timezone

local = datetime.now()
gmt_07 = local - timedelta(hours=15)
print(local)
print(gmt_07)
print('-' * 20)

tz_gmt_07 = timezone(timedelta(hours=-15))
now = datetime.now()
print(now)
dt = now.replace(tzinfo=tz_gmt_07)
print(dt)
print('-' * 20)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
la_dt = utc_dt.astimezone(timezone(timedelta(hours=-7)))
print(la_dt)
print('-' * 20)

bj_time = datetime.now()
print(bj_time)
la_time = bj_time.astimezone(timezone(timedelta(hours=-7)))
print(la_time)
