from datetime import datetime, UTC 
from math import degrees as dg, radians as rd, asin, acos, atan, atan2, sin, cos, tan, pi, floor

def decimal_to_time(decimal_hours):
    sign = "-" if decimal_hours < 0 else ""
    decimal_hours = abs(decimal_hours)

    h = int(decimal_hours)

    minutes_decimal = (decimal_hours - h) * 60
    m = int(minutes_decimal)

    seconds_decimal = (minutes_decimal - m) * 60
    s = int(round(seconds_decimal))

    # 🔥 معالجة overflow (أهم إصلاح)
    if s == 60:
        s = 0
        m += 1

    if m == 60:
        m = 0
        h += 1

    # ⏱️ ضبط داخل 24 ساعة
    h = h % 24

    return f"{sign}{h:02d}:{m:02d}:{s:02d}"


#دالة_التاريخ_والوقت
def dateetheure(year=None, month=None, day=None):
    if year is None:
        return datetime.now(UTC)

    try:
        return datetime(year, month, day, tzinfo=UTC)
    except Exception:
        # fallback آمن
        return datetime.now(UTC)

#دالة_اليوم_اليولياني
def julian(year=None, month=None, day=None):
    from datetime import datetime, UTC

    # 📅 تحديد التاريخ
    if year is None:
        now = datetime.now(UTC)
    else:
        now = datetime(year, month, day, tzinfo=UTC)

    y = now.year
    m = now.month
    d = now.day

    h = now.hour
    mn = now.minute
    sc = now.second

    # 🔁 تحويل الأشهر
    if m <= 2:
        y -= 1
        m += 12

    a = floor(y / 100)
    b = 2 - a + floor(a / 4)

    # 🧠 اليوم بدون وقت (Julian Day at 0h UT)
    jd0 = (
        floor(365.25 * (y + 4716))
        + floor(30.6001 * (m + 1))
        + b + d
        - 1524.5
    )

    # ⏱️ إضافة الوقت
    day_fraction = (h / 24) + (mn / 1440) + (sc / 86400)

    jd = jd0 + day_fraction

    return jd, jd0

#دالة_الطول_السماوي
def ecliptiquelongitude():

    jd, jd0 = julian()

    n = jd - 2444238.5
    n0 = jd0 - 2444238.5

    L = (278.83352 + 0.985647 * n) % 360
    L0 = (278.83352 + 0.985647 * n0) % 360

    C = sin(rd(L - 282.596403)) * ((360/pi) * 0.016718)
    C0 = sin(rd(L0 - 282.596403)) * ((360/pi) * 0.016718)

    true_long = (L + C) % 360
    true_long0 = (L0 + C0) % 360

    return L, L0, true_long, true_long0

#دالة_الميل
def declinaison():

    ob = 23.4393
    sin_ob = sin(rd(ob))

    _, _, l, l0 = ecliptiquelongitude()

    dec = dg(asin(sin(rd(l)) * sin_ob))
    dec0 = dg(asin(sin(rd(l0)) * sin_ob))

    return dec, dec0

#دالة_الطلوع_المستفيم
def alpha():

    ob = 23.4393

    _, _, l, l0 = ecliptiquelongitude()

    a = dg(atan2(cos(rd(ob)) * sin(rd(l)), cos(rd(l)))) % 360
    a0 = dg(atan2(cos(rd(ob)) * sin(rd(l0)), cos(rd(l0)))) % 360

    a /= 15
    a0 /= 15

    return a, a0, decimal_to_time(a), decimal_to_time(a0)

#دالة_تعديل_الزمن
def analima():

    L, L0, _, _ = ecliptiquelongitude()
    _, a0, _, _ = alpha()

    eot = L0 - 0.0057183 - (a0 * 15)

    if eot > 180:
        eot -= 360
    elif eot < -180:
        eot += 360

    eot = -eot * 4 / 60

    return eot, decimal_to_time(eot)

# دالة الزوال (الزوال الحقيقي للشمس)
#def zwl(longitude, timezone):

    #eot, _ = analima()
    #zawal_decimal = 12 + (-longitude / 15) + eot + timezone

    #return zawal_decimal, decimal_to_time(zawal_decimal)

# دالة غاية الزوال (أقصى ارتفاع للشمس)
def ghaya(latitude):

    dec, _ = declinaison()

    r = dec + (90 - latitude)

    if r > 90:
        r = 180 - r

    return r

# دالة الظلال (جميع الظلال المحسوبة في الكتاب)
def ombres(latitude):

    r = ghaya(latitude)

    shadow_zawal = 60 / tan(rd(r))
    shadow_asr = 60 + shadow_zawal
    shadow_asr_end = 120 + shadow_zawal

    return shadow_zawal, shadow_asr, shadow_asr_end

# دالة الارتفاعات الشمسية
def alts(latitude):

    shadow_zawal, shadow_asr, shadow_asr_end = ombres(latitude)

    altitude_fajr = -18
    altitude_sunrise = -50 / 60

    altitude_asr = dg(atan(60 / shadow_asr))
    altitude_asr_end = dg(atan(60 / shadow_asr_end))

    altitude_maghrib = -50 / 60
    altitude_extra = -5

    return (
        altitude_fajr,
        altitude_sunrise,
        altitude_asr,
        altitude_asr_end,
        altitude_maghrib,
        altitude_extra
    )

# دالة تحويل الارتفاع إلى زاوية ساعة
def converttoheure(altitude, latitude):

    _, dec = declinaison()

    cosH = (
        (sin(rd(altitude))
        - (sin(rd(latitude)) * sin(rd(dec))))
        /
        (cos(rd(latitude)) * cos(rd(dec)))
    )

    # 🔥 حماية من الخطأ الرياضي
    cosH = max(-1, min(1, cosH))

    hour_angle = dg(acos(cosH)) / 15

    return hour_angle, decimal_to_time(hour_angle)

# دالة الفجر
def fajr(longitude, timezone, latitude, date=None):

    zawal_decimal = zwl(longitude, timezone, date)

    altitude_fajr, _, _, _, _, _ = alts(latitude)

    hour_angle_fajr, _ = converttoheure(altitude_fajr, latitude)

    return decimal_to_time(zawal_decimal - hour_angle_fajr)

# دالة الشروق
def chrouq(longitude, timezone, latitude, date=None):

    zawal_decimal = zwl(longitude, timezone, date)

    _, altitude_sunrise, _, _, _, _ = alts(latitude)

    hour_angle, _ = converttoheure(altitude_sunrise, latitude)

    return decimal_to_time(zawal_decimal - hour_angle)

# دالة الزوال والظهر
def zwl(longitude, timezone, date=None):

    eot, _ = analima()
    
    zawal_decimal = 12 + (-longitude / 15) + eot + timezone
    #zawal_time = decimal_to_time(zawal_decimal)
    return zawal_decimal
#print(zwl(-16.14583334, -1, 2026-4-20))

def zwlt(longitude, timezone, date=None):

    eot, _ = analima()
    
    zawal_decimal = zwl(longitude, timezone, date)
    zawal_time = decimal_to_time(zawal_decimal)
    return zawal_time
#print(zwlt(-16.14583334, -1, 2026-4-20))


# دالة العصر وآخر العصر
def asr(longitude, timezone, latitude, date=None):

    zawal_decimal = zwl(longitude, timezone, date)

    _, _, altitude_asr, altitude_asr_end, _, _ = alts(latitude)

    h_asr, _ = converttoheure(altitude_asr, latitude)
    h_end, _ = converttoheure(altitude_asr_end, latitude)

    return (
        decimal_to_time(zawal_decimal + h_asr),
        decimal_to_time(zawal_decimal + h_end)
    )
#print(asr(-16.14583334, -1, 15.05916667, 2026-4-20))

# دالة الغروب والمغرب
def ghroup(lon, timezone, lat, date=None):

    z = zwl(lon, timezone, date)

    _, _, _, _, alt_maghrib, _ = alts(lat)

    h, _ = converttoheure(alt_maghrib, lat)

    ghurub = z + h
    maghrib = ghurub + (2 / 60)

    return decimal_to_time(ghurub), decimal_to_time(maghrib)
#print(ghroup(-16.14583334, -1, 15.05916667, 2026-4-20))
# دالة العشاء
def ichat(lon, timezone, lat, date=None):

    z = zwl(lon, timezone, date)

    _, _, _, _, alt_maghrib, _ = alts(lat)

    h, _ = converttoheure(alt_maghrib, lat)

    ghurub = z + h

    icha = ghurub + (90 / 60)

    return decimal_to_time(icha)

def format_time(t):
    if isinstance(t, tuple):
        h, m = t
        return f"{int(h):02d}:{int(m):02d}"
    return t
#print(ichat(-16.14583334, -1, 15.05916667, 2026-4-20))
# دالة جدول الصلوات
def salat_times(lon, tz, lat, date=None):
    from datetime import datetime

    if date is None:
        date = datetime.now()
        
    fajr_time = fajr(lon, tz, lat)
    sunrise_time = chrouq(lon, tz, lat)

    zawal_time = zwlt(lon, tz, lat)

    asr_time, asr_end = asr(lon, tz, lat)

    ghurub_time, maghrib_time = ghroup(lon, tz, lat)

    isha_time = ichat(lon, tz, lat)
    
    return {
    "الفجر": fajr_time,
    "الشروق": sunrise_time,
    "الظهر": zawal_time,
    "العصر": asr_time,
    "المغرب": maghrib_time,
    "العشاء": isha_time
}
