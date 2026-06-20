import flet as ft
import datetime
import time
import threading
import requests
import json
import os

# دالة جلب مواقيت الصلاة من الإنترنت لمدينة دمنهور
def get_prayer_times():
    try:
        url = "http://api.aladhan.com/v1/timingsByCity?city=Damanhur&country=Egypt&method=5"
        response = requests.get(url).json()
        if response["code"] == 200:
            timings = response["data"]["timings"]
            return {
                "Fajr": timings["Fajr"],
                "Sunrise": timings["Sunrise"],
                "Dhuhr": timings["Dhuhr"],
                "Asr": timings["Asr"],
                "Maghrib": timings["Maghrib"],
                "Isha": timings["Isha"]
            }
    except:
        return {"Fajr": "03:15", "Sunrise": "04:55", "Dhuhr": "12:00", "Asr": "15:30", "Maghrib": "19:00", "Isha": "20:30"}

def تفعيل_المصحف_الأوفلاين_الكامل():
    file_path = "assets/quran_perfect_offline.json"
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            res_ar = requests.get("https://api.alquran.cloud/v1/quran/quran-simple").json()
            res_en = requests.get("https://api.alquran.cloud/v1/quran/en.sahih").json()
            if res_ar["code"] == 200 and res_en["code"] == 200:
                surahs_ar = res_ar["data"]["surahs"]
                surahs_en = res_en["data"]["surahs"]
                for s_idx in range(len(surahs_ar)):
                    for a_idx in range(len(surahs_ar[s_idx]["ayahs"])):
                        surahs_ar[s_idx]["ayahs"][a_idx]["text_en"] = surahs_en[s_idx]["ayahs"][a_idx]["text"]
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(surahs_ar, f, ensure_ascii=False)
        except:
            pass

def main(page: ft.Page):
    page.title = "تطبيق المؤذن والأذكار والقرآن الكريم"
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # طلب أذونات الإشعارات للموبايل فور فتح التطبيق
    if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
        try:
            page.request_permission(ft.PermissionType.NOTIFICATION)
        except:
            pass

    threading.Thread(target=تفعيل_المصحف_الأوفلاين_الكامل, daemon=True).start()

    prayer_times = get_prayer_times()
    azkar_list = ["سبحان الله", "الحمد لله", "لا إله إلا الله", "الله أكبر", "أستغفر الله العظيم"]
    state = {"index": 0, "count": 0}

    morning_azkar = [
        {"text": "أصْبَحْنَا وَأَصْبَحَ المُلْكُ للهِ وَالحَمْدُ للهِ، لا إلَهَ إلَّا اللهُ وَحْدَهُ لا شَرِيكَ له، له المُلْكُ وَله الحَمْدُ وَهو علَى كُلِّ شيءٍ قَدِيرٌ.", "count": 1},
        {"text": "آية الكرسي: اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ...", "count": 1},
        {"text": "قُلْ هُوَ اللَّهُ أَحَدٌ... قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ... قُلْ أَعُوذُ بِرَبِّ النَّاسِ...", "count": 3},
        {"text": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عهدِكَ ووَعْدِكَ مَا اسْتَطَعْتُ...", "count": 1},
        {"text": "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.", "count": 3}
    ]

    evening_azkar = [
        {"text": "أمْسَيْنَا وَأَمْسَى المُلْكُ للهِ وَالحَمْدُ للهِ، لا إلَهَ إلَّا اللهُ وَحْدَهُ لا شَرِيكَ له...", "count": 1},
        {"text": "آية الكرسي: اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...", "count": 1},
        {"text": "قُلْ هُوَ اللَّهُ أَحَدٌ... قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ... قُلْ أَعُوذُ بِرَبِّ النَّاسِ...", "count": 3},
        {"text": "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ.", "count": 3},
        {"text": "حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ ۖ عَلَيْهِ تَوَكَّلْتُ ۖ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ.", "count": 7}
    ]

    # دالة تشغيل الصوت المتوافقة مع جميع أنظمة الموبايل والكمبيوتر عبر سطر أوامر آمن
    def play_sound_universal(file_name):
        try:
            # تشغيل الصوت للكمبيوتر (ويندوز)
            if page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.MACOS, ft.PagePlatform.LINUX] or page.platform is None:
                clean_path = os.path.abspath(f"assets/audio/{file_name}")
                os.system(f'start /min powershell -c (New-Object Media.SoundPlayer "{clean_path}").PlaySync();')
            else:
                # للموبايل: نستخدم وسيلة بث الصوت المدمجة الخاصة بالمتصفح/الهاتف عبر تشغيل غير مرئي
                page.play_media(f"/audio/{file_name}")
        except:
            pass

    def close_adhan_dialog(e):
        adhan_dialog.open = False
        page.update()

    adhan_dialog = ft.AlertDialog(
        content=ft.Container(
            width=300, height=380,
            content=ft.Stack([
                ft.Image(src="images/kaaba.png", fit="cover", expand=True),
                ft.Container(
                    bgcolor="black54", alignment=ft.Alignment(0, 0),
                    content=ft.Column([
                        ft.Text("حان الآن وقت الأذان", size=22, color="amber", weight="bold", text_align="center"),
                        ft.Container(height=15),
                        ft.Text("بصوت الشيخ محمد رفعت", size=15, color="white", text_align="center"),
                        ft.Container(height=35),
                        ft.ElevatedButton("إغلاق النافذة ✖", bgcolor="amber800", color="white", on_click=close_adhan_dialog)
                    ], alignment="center", horizontal_alignment="center")
                )
            ]), border_radius=15
        ), modal=True
    )
    page.overlay.append(adhan_dialog)

    def send_android_notification(title, message):
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"🔔 {title}: {message}"), open=True))

    def trigger_adhan(prayer_name):
        adhan_dialog.open = True
        page.update()
        
        if prayer_name == "الشروق":
            send_android_notification("شروق الشمس", "حان الآن وقت شروق الشمس")
            threading.Thread(target=play_sound_universal, args=("birds.mp3",), daemon=True).start()
        else:
            send_android_notification("نداء الصلاة", f"حان الآن موعد أذان {prayer_name}")
            threading.Thread(target=play_sound_universal, args=("refat.mp3",), daemon=True).start()

    def get_next_prayer_info():
        now = datetime.datetime.now()
        current_time_str = now.strftime("%H:%M")
        current_sec = now.strftime("%S")
        
        if current_sec == "00":
            for name, p_time in prayer_times.items():
                if current_time_str == p_time:
                    names_ar = {"Fajr": "الفجر", "Sunrise": "الشروق", "Dhuhr": "الظهر", "Asr": "العصر", "Maghrib": "المغرب", "Isha": "العشاء"}
                    trigger_adhan(names_ar.get(name, name))
                    break

        next_prayer_name = "الفجر"
        next_prayer_time_str = prayer_times["Fajr"]
        
        for name, p_time in prayer_times.items():
            p_hour, p_minute = map(int, p_time.split(':'))
            p_datetime = now.replace(hour=p_hour, minute=p_minute, second=0, microsecond=0)
            if p_datetime > now:
                next_prayer_name = name
                next_prayer_time_str = p_time
                break
        
        names_ar = {"Fajr": "الفجر", "Sunrise": "الشروق", "Dhuhr": "الظهر", "Asr": "العصر", "Maghrib": "المغرب", "Isha": "العشاء"}
        next_prayer_name_ar = names_ar.get(next_prayer_name, next_prayer_name)
        
        p_hour, p_minute = map(int, next_prayer_time_str.split(':'))
        target_time = now.replace(hour=p_hour, minute=p_minute, second=0, microsecond=0)
        if target_time < now:
            target_time += datetime.timedelta(days=1)
            
        remaining_time = target_time - now
        secs = remaining_time.seconds
        hours = secs // 3600
        mins = (secs % 3600) // 60
        seconds = secs % 60
        
        return next_prayer_name_ar, f"{hours:02d}:{mins:02d}:{seconds:02d}"

    def update_clock():
        while True:
            try:
                now_str = datetime.datetime.now().strftime("%H:%M:%S")
                prayer_name, time_left = get_next_prayer_info()
                clock_label.value = f"الوقت الحالي: {now_str}"
                next_prayer_label.value = f"الصلاة القادمة: {prayer_name}\nالمتبقي لها: {time_left}"
                page.update()
            except:
                pass
            time.sleep(1)

    # دالات السبحة
    def count_up(e):
        state["count"] += 1
        counter_text.value = str(state["count"])
        page.update()

    def reset_counter(e):
        state["count"] = 0
        counter_text.value = "0"
        page.update()

    def next_zekr(e):
        state["index"] = (state["index"] + 1) % len(azkar_list)
        zekr_label.value = azkar_list[state["index"]]
        state["count"] = 0
        counter_text.value = "0"
        page.update()

    # تصفح المصحف الشريف
    def open_surah_view(surah_number, surah_name, ayahs_list):
        quran_view.controls.clear()
        quran_view.controls.append(ft.Text(f"سورة {surah_name}", size=24, color="amber", weight="bold"))
        quran_view.controls.append(ft.Container(height=10))
        for ayah in ayahs_list:
            text_ar = ayah.get("text", "")
            text_en = ayah.get("text_en", "")
            quran_view.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{text_ar} ({ayah.get('numInSurah', ayah.get('numberInSurah', ''))})", size=20, color="white", text_align="right", rtl=True),
                        ft.Container(height=5),
                        ft.Text(f"{text_en}", size=14, color="white70", text_align="left"),
                        ft.Divider(color="white10")
                    ]), padding=10
                )
            )
        page.update()

    def handle_surah_click(surah_number, surah_name):
        file_path = "assets/quran_perfect_offline.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                surahs = json.load(f)
                open_surah_view(surah_number, surah_name, surahs[surah_number - 1]["ayahs"])

    def open_quran(e):
        quran_view.controls.clear()
        quran_sheet.open = True
        page.update()
        quran_view.controls.append(ft.Text("المصحف الشريف", size=20, color="amber", weight="bold"))
        grid = ft.GridView(expand=True, runs_count=2, max_extent=150, child_aspect_ratio=2.5)
        surah_names = ["الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"]
        for id, name in enumerate(surah_names, start=1):
            grid.controls.append(
                ft.ElevatedButton(
                    content=ft.Text(f"{id}. {name}", color="black", weight="bold", size=12),
                    bgcolor="white",
                    on_click=lambda e, s_num=id, s_name=name: handle_surah_click(s_num, s_name)
                )
            )
        quran_view.controls.append(grid)
        page.update()

    # أذكار حصن المسلم
    def load_azkar_type(azkar_data, title):
        azkar_view.controls.clear()
        azkar_view.controls.append(ft.Text(title, size=22, color="amber", weight="bold"))
        azkar_view.controls.append(ft.Container(height=10))
        for item in azkar_data:
            current_repeat = [item["count"]]
            text_display = ft.Text(item["text"], size=16, color="white", text_align="right", rtl=True)
            btn_counter = ft.ElevatedButton(text=f"التكرار المطلوب: {current_repeat[0]}", bgcolor="brown700", color="white")
            def on_item_click(e, btn=btn_counter, rep=current_repeat):
                if rep[0] > 1:
                    rep[0] -= 1
                    btn.text = f"المتبقي: {rep[0]}"
                else:
                    btn.text = "تم بحمد الله ✅"
                    btn.bgcolor = "green700"
                page.update()
            btn_counter.on_click = on_item_click
            azkar_view.controls.append(
                ft.Card(content=ft.Container(content=ft.Column([text_display, ft.Container(height=5), btn_counter], horizontal_alignment="center"), padding=15, bgcolor="black"), margin=10)
            )
        page.update()

    def open_azkar_sheet(e):
        azkar_view.controls.clear()
        azkar_sheet.open = True
        page.update()
        azkar_view.controls.append(
            ft.Row([
                ft.ElevatedButton("🌅 أذكار الصباح", bgcolor="amber800", color="white", on_click=lambda e: load_azkar_type(morning_azkar, "أذكار الصباح")),
                ft.ElevatedButton("🌌 أذكار المساء", bgcolor="brown800", color="white", on_click=lambda e: load_azkar_type(evening_azkar, "أذكار المساء")),
            ], alignment="center", spacing=15)
        )
        page.update()

    # عناصر الواجهة الرئيسية
    clock_label = ft.Text(value="", size=14, color="white70", weight="bold")
    next_prayer_label = ft.Text(value="جاري حساب المواقيت...", size=20, color="white", weight="bold", text_align="center")
    zekr_label = ft.Text(value=azkar_list[state["index"]], size=24, color="amber", weight="bold", text_align="center")
    counter_text = ft.Text(value="0", size=28, color="white", weight="bold")

    counter_btn = ft.Container(content=counter_text, alignment=ft.Alignment(0, 0), width=100, height=100, bgcolor="amber800", border_radius=50, on_click=count_up)
    control_buttons = ft.Row([
        ft.TextButton(content=ft.Text("تصفير 🔄", color="white"), on_click=reset_counter),
        ft.TextButton(content=ft.Text("الذكر التالي ⬅️", color="amber"), on_click=next_zekr),
    ], alignment="center", spacing=20)

    menu_buttons = ft.Row([
        ft.ElevatedButton(content=ft.Text("📖 المصحف", color="white", weight="bold"), bgcolor="brown800", on_click=open_quran),
        ft.ElevatedButton(content=ft.Text("✨ حصن المسلم", color="white", weight="bold"), bgcolor="amber800", on_click=open_azkar_sheet),
    ], alignment="center", spacing=15)

    quran_view = ft.Column(expand=True, scroll="always", horizontal_alignment="center")
    quran_sheet = ft.BottomSheet(ft.Container(content=quran_view, padding=20, bgcolor="black", height=450), open=False)
    page.overlay.append(quran_sheet)

    azkar_view = ft.Column(expand=True, scroll="always", horizontal_alignment="center")
    azkar_sheet = ft.BottomSheet(ft.Container(content=azkar_view, padding=20, bgcolor="black", height=450), open=False)
    page.overlay.append(azkar_sheet)

    page.add(
        ft.Stack([
            ft.Image(src="images/allah.png", fit="cover", expand=True),
            ft.Container(
                bgcolor="black54", alignment=ft.Alignment(0, 0),
                content=ft.Column([
                    clock_label, ft.Container(height=5),
                    next_prayer_label, ft.Container(height=10),
                    menu_buttons, ft.Divider(color="white24", height=25),
                    ft.Text("السبحة الإلكترونية", size=12, color="white54"),
                    zekr_label, ft.Container(height=10),
                    counter_btn, ft.Container(height=10),
                    control_buttons,
                ], alignment="center", horizontal_alignment="center")
            )
        ], expand=True)
    )

    threading.Thread(target=update_clock, daemon=True).start()

ft.app(target=main, assets_dir="assets")