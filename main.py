import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.text import LabelBase
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime, timedelta, timezone
import os
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
    
# 📁 مسار المشروع
BASE_DIR = os.path.dirname(__file__)

# 🔍 اختبار وجود الخط
#print("PATH:", os.path.join(BASE_DIR, "Cairo-Regular.ttf"))
#print("EXISTS:", os.path.exists(os.path.join(BASE_DIR, "Cairo-Regular.ttf")))

# 🅰️ تسجيل الخط العربي
LabelBase.register(
    name="Arabic",
    fn_regular=r"C:\Windows\Fonts\arial.ttf"
)

# 📦 دوالك
from prayertime_core import salat_times


def parse_time_to_seconds(t):
    if t is None:
        return 0

    ts = str(t).strip()

    if ":" in ts:
        parts = ts.split(":")

        h = int(parts[0]) if len(parts) > 0 else 0
        m = int(parts[1]) if len(parts) > 1 else 0
        s = int(parts[2]) if len(parts) > 2 else 0

        return h * 3600 + m * 60 + s

    return 0


def get_next_prayer(times, tz):
    now = datetime.now(timezone.utc) + timedelta(hours=tz)
    current = now.hour * 3600 + now.minute * 60 + now.second

    arr = []
    for name, t in times.items():
        sec = parse_time_to_seconds(t)
        arr.append((name, sec))

    arr.sort(key=lambda x: x[1])

    for name, sec in arr:
        if current < sec:
            return name, sec - current

    name, sec = arr[0]
    return name, (86400 - current) + sec


# 🕌 التطبيق
class PrayerApp(App):

    
    def build(self):
        self.muted = False
        self.sound = SoundLoader.load("adhan.wav")
        self.last_adhan = None
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_label = Label(
        text=ar("🕌 مواقيت الصلاة"),
        font_name="Arabic",
        font_size=28
        )

        self.label = Label(
        text="...",
        font_name="Arabic",
        font_size=22
        )

        self.btn_mute = Button(
        text="🔊 الصوت يعمل",
        size_hint=(1, 0.2)
        )
        self.btn_mute.bind(on_press=self.toggle_mute)

        root.add_widget(self.title_label)
        root.add_widget(self.label)
        root.add_widget(self.btn_mute)

        Clock.schedule_interval(self.update, 1)

        return root
        print(self.title_label)
        print(type(self.title_label))

    def toggle_mute(self, instance):
        self.muted = not self.muted

        if self.muted:
            self.btn_mute.text = ar("🔇 مكتوم")
        else:
            self.btn_mute.text = ar("🔊 الصوت يعمل")
        
    def play_adhan(self):
        if self.muted:
            return
        if self.sound:
            self.sound.play()

    def update(self, dt):
        lat = 14.6937
        lon = -17.4441
        tz = 0

        today = datetime.now()
        times = salat_times(lon, tz, lat, today)

        next_prayer, remaining = get_next_prayer(times, tz)

        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        seconds = int(remaining % 60)
        if remaining <= 1:
            self.play_adhan()
            self.last_adhan = next_prayer
            
        text = ""

        for name, t in times.items():
            text += ar(f"{name} : {t}") + "\n"

        text += "\n------------------\n"
        text += ar(f"⏭ القادمة: {next_prayer}") + "\n"
        text += ar(f"⏳ المتبقي: {hours:02}:{minutes:02}:{seconds:02}")

        self.label.text = text

def ar(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ▶️ التشغيل
if __name__ == "__main__":
    PrayerApp().run()
