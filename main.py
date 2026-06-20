import flet as ft

def main(page: ft.Page):
    # 1. تطابق الشاشة مع حجم أي هاتف (Responsive Design)
    page.adaptive = True
    page.padding = 0
    page.spacing = 0
    
    # ضبط المحاذاة لتكون مرنة
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 2. طلب الأذونات فور فتح التطبيق
    # ملاحظة: Flet بيطلب الإشعارات والموقع أوتوماتيكياً لما بنضيف الـ Plugins في الـ build
    
    def play_azan(e):
        # تشغيل الأذان مرتبط بالوسائط (Music/Media) وليس التنبيهات
        # في Flet الـ Audio Player الافتراضي بيمشي مع حجم صوت الوسائط
        audio1.play()

    audio1 = ft.Audio(
        src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # استبدله برابط صوت الأذان بتاعك
        autoplay=False,
        volume=1.0, # أعلى مستوى في الوسائط
    )
    page.overlay.append(audio1)

    # واجهة مرنة تتمدد حسب حجم التليفون
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(name=ft.icons.MOSQUE, size=100, color=ft.colors.GREEN_800),
                        ft.Text("تطبيق الأذان", size=28, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("تجربة صوت الأذان", on_click=play_azan),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True, # يملأ الشاشة بالكامل لأي هاتف
            )
        )
    )

ft.app(target=main)
