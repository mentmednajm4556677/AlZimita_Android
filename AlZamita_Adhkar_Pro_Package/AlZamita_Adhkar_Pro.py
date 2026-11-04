# -*- coding: utf-8 -*-
"""
الزميتة للأذكار - إصدار مطوّر
المتطلبات: Python 3 فقط (Tkinter وSQLite مدمجان مع بايثون).
التشغيل على Windows:
    python main.py

يحفظ التطبيق التسبيح والمفضلة والإعدادات في ملف adhkar_data.db
بجانب هذا الملف تلقائياً.
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3
import json
import webbrowser
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_FILE = APP_DIR / "adhkar_data.db"
BACKUP_FILE = APP_DIR / "tasbeeh_backup.json"

# ألوان الواجهة
LIGHT = {
    "bg": "#F3F7F4", "surface": "#FFFFFF", "surface2": "#E8F1EB",
    "primary": "#176B50", "primary_hover": "#10563F",
    "text": "#1F332A", "muted": "#718078", "border": "#DCE7DF",
    "gold": "#D6A64B", "danger": "#B94A48", "input": "#FFFFFF"
}
DARK = {
    "bg": "#17231E", "surface": "#22332B", "surface2": "#2B4035",
    "primary": "#238765", "primary_hover": "#2C9A75",
    "text": "#F0F5F1", "muted": "#B2C2B8", "border": "#3A5145",
    "gold": "#E5BD68", "danger": "#E17870", "input": "#2B4035"
}

# الأذكار المعروضة. يُفضّل مراجعة النصوص والتخريج قبل اعتماد إصدار للنشر.
AZKAR = {
    "أذكار الصباح": [
        ("أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", 1),
        ("اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ.", 1),
        ("رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ ﷺ نَبِيًّا.", 3),
        ("بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.", 3),
        ("حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ.", 7),
        ("اللَّهُمَّ مَا أَصْبَحَ بِي مِنْ نِعْمَةٍ أَوْ بِأَحَدٍ مِنْ خَلْقِكَ فَمِنْكَ وَحْدَكَ لَا شَرِيكَ لَكَ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْرُ.", 1),
        ("سُبْحَانَ اللَّهِ وَبِحَمْدِهِ.", 100),
        ("اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ.", 10),
    ],
    "أذكار المساء": [
        ("أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", 1),
        ("اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ.", 1),
        ("رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ ﷺ نَبِيًّا.", 3),
        ("بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ.", 3),
        ("أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ.", 3),
        ("حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ.", 7),
        ("سُبْحَانَ اللَّهِ وَبِحَمْدِهِ.", 100),
        ("اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ.", 10),
    ],
    "أذكار النوم": [
        ("بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا.", 1),
        ("اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ.", 1),
        ("سُبْحَانَ اللَّهِ.", 33),
        ("الْحَمْدُ لِلَّهِ.", 33),
        ("اللَّهُ أَكْبَرُ.", 34),
        ("آية الكرسي: سورة البقرة، الآية 255.", 1),
        ("قراءة سورة الإخلاص وسورة الفلق وسورة الناس، ثم النفث في الكفين ومسح ما استطاع من الجسد.", 3),
    ],
    "أذكار الاستيقاظ": [
        ("الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ.", 1),
        ("لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ، اللَّهُمَّ أَسْتَغْفِرُكَ لِذَنْبِي وَأَسْأَلُكَ رَحْمَتَكَ.", 1),
    ],
    "أذكار بعد الصلاة": [
        ("أَسْتَغْفِرُ اللَّهَ.", 3),
        ("اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ، تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ.", 1),
        ("سُبْحَانَ اللَّهِ.", 33),
        ("الْحَمْدُ لِلَّهِ.", 33),
        ("اللَّهُ أَكْبَرُ.", 33),
        ("لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", 1),
    ],
    "أذكار دخول المنزل والخروج": [
        ("بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى اللَّهِ رَبِّنَا تَوَكَّلْنَا.", 1),
        ("بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ.", 1),
    ],
    "أذكار المسجد": [
        ("اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ.", 1),
        ("اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ.", 1),
    ],
    "أذكار الوضوء": [
        ("بِسْمِ اللَّهِ.", 1),
        ("أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، وَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ.", 1),
        ("اللَّهُمَّ اجْعَلْنِي مِنَ التَّوَّابِينَ وَاجْعَلْنِي مِنَ الْمُتَطَهِّرِينَ.", 1),
    ],
    "أذكار متنوعة": [
        ("لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ.", 100),
        ("سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ.", 1),
        ("أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ.", 100),
        ("اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ.", 10),
    ]
}


class AdhkariApp:
    def __init__(self, root):
        self.root = root
        self.root.title("الزميتة للأذكار | رفيق الذكر اليومي")
        self.root.geometry("1100x760")
        self.root.minsize(850, 620)
        self.conn = sqlite3.connect(DB_FILE)
        self.create_database()

        self.dark = self.get_setting("dark", "0") == "1"
        self.font_size = int(self.get_setting("font_size", "15"))
        self.tasbeeh_count = self.load_tasbeeh_count()
        self.tasbeeh_target = int(self.get_setting("tasbeeh_target", "100"))
        self.current_category = None
        self.current_items = []
        self.item_index = 0
        self.item_count = 0
        self.page = None
        self.colors = DARK if self.dark else LIGHT

        self.root.configure(bg=self.colors["bg"])
        self.build_shell()
        self.show_home()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def create_database(self):
        with self.conn:
            self.conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS favorites (text TEXT PRIMARY KEY)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS daily_stats (day TEXT PRIMARY KEY, count INTEGER NOT NULL DEFAULT 0)")

    def get_setting(self, key, default):
        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else default

    def set_setting(self, key, value):
        self.conn.execute(
            "INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",
            (key, str(value))
        )
        self.conn.commit()

    def load_tasbeeh_count(self):
        """استعادة العداد من ملف النسخة الاحتياطية، ثم قاعدة البيانات."""
        try:
            if BACKUP_FILE.exists():
                data = json.loads(BACKUP_FILE.read_text(encoding="utf-8"))
                value = int(data.get("count", 0))
                if value >= 0:
                    return value
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass

        try:
            return max(0, int(self.get_setting("tasbeeh_count", "0")))
        except (ValueError, TypeError):
            return 0

    def save_tasbeeh_count(self):
        """حفظ فوري في SQLite وملف JSON احتياطي."""
        self.set_setting("tasbeeh_count", self.tasbeeh_count)
        temporary = BACKUP_FILE.with_suffix(".tmp")
        try:
            temporary.write_text(
                json.dumps({"count": self.tasbeeh_count}, ensure_ascii=False),
                encoding="utf-8"
            )
            temporary.replace(BACKUP_FILE)
        except OSError:
            # قاعدة البيانات تبقى نسخة الحفظ الأساسية إذا تعذر إنشاء الملف الاحتياطي.
            pass

    def palette(self):
        return DARK if self.dark else LIGHT

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def build_shell(self):
        c = self.palette()
        self.header = tk.Frame(self.root, bg=c["primary"], height=86)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        logo_box = tk.Frame(self.header, bg=c["primary"])
        logo_box.pack(side="right", padx=24, pady=10)
        logo_mark = tk.Canvas(logo_box, width=54, height=54, bg=c["primary"],
                              highlightthickness=0)
        logo_mark.pack(side="right", padx=(0, 10))
        logo_mark.create_oval(3, 3, 51, 51, outline="#E7C46F", width=3)
        logo_mark.create_text(27, 27, text="ذ", fill="white",
                              font=("Arial", 27, "bold"))
        logo_text = tk.Frame(logo_box, bg=c["primary"])
        logo_text.pack(side="right")
        self.brand = tk.Label(logo_text, text="الزميتة للأذكار", bg=c["primary"], fg="white",
                              font=("Arial", 23, "bold"))
        self.brand.pack(anchor="e")
        tk.Label(logo_text, text="رفيق الذكر والطمأنينة", bg=c["primary"],
                 fg="#E5F0E9", font=("Arial", 9)).pack(anchor="e")

        self.theme_button = tk.Button(self.header, text="☀" if self.dark else "☾",
                                      command=self.toggle_theme, font=("Arial", 17, "bold"),
                                      bg=c["surface"], fg=c["text"], relief="flat", width=3,
                                      cursor="hand2")
        self.theme_button.pack(side="left", padx=22, pady=20)

        self.body = tk.Frame(self.root, bg=c["bg"])
        self.body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.body, bg=c["surface"], width=220,
                                highlightthickness=1, highlightbackground=c["border"])
        self.sidebar.pack(side="right", fill="y", padx=(12, 0), pady=14)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="القائمة الرئيسية", bg=c["surface"], fg=c["muted"],
                 font=("Arial", 12, "bold")).pack(anchor="e", padx=18, pady=(22, 12))

        nav = [
            ("⌂  الرئيسية", self.show_home),
            ("🌅  أذكار الصباح", lambda: self.show_category("أذكار الصباح")),
            ("🌙  أذكار المساء", lambda: self.show_category("أذكار المساء")),
            ("😴  أذكار النوم", lambda: self.show_category("أذكار النوم")),
            ("🌄  الاستيقاظ", lambda: self.show_category("أذكار الاستيقاظ")),
            ("🕌  بعد الصلاة", lambda: self.show_category("أذكار بعد الصلاة")),
            ("🚪  المنزل", lambda: self.show_category("أذكار دخول المنزل والخروج")),
            ("🕌  المسجد", lambda: self.show_category("أذكار المسجد")),
            ("💧  الوضوء", lambda: self.show_category("أذكار الوضوء")),
            ("📿  المسبحة", self.show_tasbeeh),
            ("⭐  المفضلة", self.show_favorites),
            ("⚙  الإعدادات", self.show_settings),
        ]
        self.nav_buttons = []
        for label, command in nav:
            b = tk.Button(self.sidebar, text=label, command=command, anchor="e",
                          bg=c["surface"], fg=c["text"], activebackground=c["surface2"],
                          activeforeground=c["text"], relief="flat", bd=0,
                          font=("Arial", 12, "bold"), padx=15, pady=12, cursor="hand2")
            b.pack(fill="x", padx=8, pady=2)
            self.nav_buttons.append(b)

        tk.Label(self.sidebar, text="نسخة سطح المكتب", bg=c["surface"], fg=c["muted"],
                 font=("Arial", 9)).pack(side="bottom", pady=(3, 8))
        tk.Label(self.sidebar, text="المطور: أحمدو", bg=c["surface"], fg=c["text"],
                 font=("Arial", 10, "bold")).pack(side="bottom", pady=(10, 2))
        wa = tk.Label(self.sidebar, text="واتساب المطور: +22244995677",
                      bg=c["surface"], fg="#159B61", cursor="hand2",
                      font=("Arial", 9, "bold"))
        wa.pack(side="bottom", pady=3)
        wa.bind("<Button-1>", lambda event: self.open_whatsapp())

        self.content = tk.Frame(self.body, bg=c["bg"])
        self.content.pack(side="right", fill="both", expand=True, padx=18, pady=14)

        self.footer = tk.Label(self.root, text="اللهم أعنّا على ذكرك وشكرك وحسن عبادتك",
                               bg=c["surface"], fg=c["muted"], font=("Arial", 10),
                               pady=9)
        self.footer.pack(fill="x", side="bottom")

    def card(self, parent, bg=None, padx=18, pady=16):
        c = self.palette()
        return tk.Frame(parent, bg=bg or c["surface"], padx=padx, pady=pady,
                        highlightthickness=1, highlightbackground=c["border"])

    def heading(self, parent, title, subtitle=""):
        c = self.palette()
        tk.Label(parent, text=title, bg=c["bg"], fg=c["text"],
                 font=("Arial", 23, "bold"), anchor="e").pack(fill="x", pady=(5, 3))
        if subtitle:
            tk.Label(parent, text=subtitle, bg=c["bg"], fg=c["muted"],
                     font=("Arial", 11), anchor="e").pack(fill="x", pady=(0, 15))

    def make_button(self, parent, text, command, primary=True, width=None):
        c = self.palette()
        bg = c["primary"] if primary else c["surface2"]
        fg = "white" if primary else c["text"]
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground=c["primary_hover"] if primary else c["border"],
                         activeforeground="white" if primary else c["text"],
                         relief="flat", bd=0, padx=16, pady=10,
                         font=("Arial", 11, "bold"), cursor="hand2", width=width)

    def show_home(self):
        self.page = "home"
        self.clear_content()
        c = self.palette()
        self.heading(self.content, "مرحباً بك في الزميتة للأذكار",
                     "رفيقك اليومي للذكر والتسبيح والطمأنينة")
        summary = self.card(self.content, bg=c["primary"], padx=24, pady=22)
        summary.pack(fill="x", pady=(0, 18))
        tk.Label(summary, text="﴿ أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ ﴾",
                 bg=c["primary"], fg="white", font=("Arial", 19, "bold"),
                 wraplength=650, justify="center").pack(fill="x", pady=8)
        tk.Label(summary, text="ابدأ وردك اليومي واجعل لسانك رطباً بذكر الله",
                 bg=c["primary"], fg="#E6F4EC", font=("Arial", 11)).pack(pady=4)

        grid = tk.Frame(self.content, bg=c["bg"])
        grid.pack(fill="both", expand=True)
        entries = [
            ("🌅", "أذكار الصباح", lambda: self.show_category("أذكار الصباح"), "#2D8A62"),
            ("🌙", "أذكار المساء", lambda: self.show_category("أذكار المساء"), "#4F64B5"),
            ("😴", "أذكار النوم", lambda: self.show_category("أذكار النوم"), "#8954A5"),
            ("📿", "المسبحة الإلكترونية", self.show_tasbeeh, "#C17B27"),
            ("⭐", "الأذكار المفضلة", self.show_favorites, "#B94F78"),
            ("⚙", "الإعدادات", self.show_settings, "#607D8B"),
        ]
        for i, (icon, label, command, color) in enumerate(entries):
            tile = tk.Frame(grid, bg=c["surface"], padx=12, pady=18,
                            highlightthickness=1, highlightbackground=c["border"])
            tile.grid(row=i // 2, column=i % 2, padx=9, pady=9, sticky="nsew")
            tk.Label(tile, text=icon, bg=c["surface"], fg=color,
                     font=("Arial", 26)).pack(pady=(2, 6))
            tk.Button(tile, text=label, command=command, bg=color, fg="white",
                      activebackground=color, activeforeground="white",
                      relief="flat", font=("Arial", 12, "bold"),
                      padx=10, pady=10, cursor="hand2").pack(fill="x")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        for r in range(3):
            grid.grid_rowconfigure(r, weight=1)

    def show_category(self, category):
        self.page = "category"
        self.current_category = category
        self.current_items = AZKAR.get(category, [])
        self.item_index = 0
        self.item_count = 0
        self.render_adhkar()

    def render_adhkar(self):
        self.clear_content()
        c = self.palette()
        self.heading(self.content, self.current_category, "اقرأ الذكر وكرره بالعدد المحدد")
        if not self.current_items:
            return
        text, target = self.current_items[self.item_index]
        card = self.card(self.content, padx=25, pady=25)
        card.pack(fill="both", expand=True, pady=8)
        tk.Label(card, text=f"الذكر {self.item_index + 1} من {len(self.current_items)}",
                 bg=c["surface"], fg=c["muted"], font=("Arial", 11, "bold")).pack(pady=(4, 16))
        tk.Label(card, text=text, bg=c["surface"], fg=c["text"],
                 font=("Arial", self.font_size + 3, "bold"), wraplength=680,
                 justify="center", anchor="center").pack(fill="both", expand=True, pady=20)
        self.progress_label = tk.Label(card, text=f"التكرار: {self.item_count} / {target}",
                                       bg=c["surface"], fg=c["primary"],
                                       font=("Arial", 17, "bold"))
        self.progress_label.pack(pady=12)
        controls = tk.Frame(card, bg=c["surface"])
        controls.pack(pady=10)
        self.make_button(controls, "＋ احتساب تكرار", self.increment_adhkar).pack(side="right", padx=5)
        self.make_button(controls, "إضافة إلى المفضلة ☆", lambda: self.add_favorite(text), primary=False).pack(side="right", padx=5)
        bottom = tk.Frame(self.content, bg=c["bg"])
        bottom.pack(fill="x", pady=10)
        self.make_button(bottom, "السابق", self.previous_adhkar, primary=False).pack(side="right", padx=5)
        self.make_button(bottom, "التالي", self.next_adhkar).pack(side="right", padx=5)
        self.make_button(bottom, "العودة للرئيسية", self.show_home, primary=False).pack(side="left", padx=5)

    def increment_adhkar(self):
        target = self.current_items[self.item_index][1]
        if self.item_count < target:
            self.item_count += 1
        self.progress_label.configure(text=f"التكرار: {self.item_count} / {target}")
        if self.item_count == target:
            self.root.bell()

    def next_adhkar(self):
        if self.item_index < len(self.current_items) - 1:
            self.item_index += 1
            self.item_count = 0
            self.render_adhkar()
        else:
            messagebox.showinfo("أحسنت", "أكملت أذكار هذا القسم. تقبّل الله منك.")
            self.show_home()

    def previous_adhkar(self):
        if self.item_index > 0:
            self.item_index -= 1
            self.item_count = 0
            self.render_adhkar()

    def add_favorite(self, text):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO favorites(text) VALUES(?)", (text,))
            messagebox.showinfo("المفضلة", "تمت إضافة الذكر إلى المفضلة.")
        except sqlite3.IntegrityError:
            messagebox.showinfo("المفضلة", "هذا الذكر موجود بالفعل في المفضلة.")

    def show_favorites(self):
        self.page = "favorites"
        self.clear_content()
        c = self.palette()
        self.heading(self.content, "الأذكار المفضلة", "الأذكار التي حفظتها للوصول إليها سريعاً")
        rows = self.conn.execute("SELECT text FROM favorites ORDER BY rowid DESC").fetchall()
        if not rows:
            tk.Label(self.content, text="لا توجد أذكار مفضلة حتى الآن.",
                     bg=c["bg"], fg=c["muted"], font=("Arial", 14)).pack(pady=50)
            return
        for (text,) in rows:
            card = self.card(self.content, padx=16, pady=12)
            card.pack(fill="x", pady=6)
            tk.Label(card, text=text, bg=c["surface"], fg=c["text"],
                     font=("Arial", self.font_size, "bold"), wraplength=650,
                     justify="right").pack(fill="x", pady=6)
            self.make_button(card, "حذف من المفضلة", lambda t=text: self.remove_favorite(t),
                             primary=False).pack(anchor="e")

    def remove_favorite(self, text):
        with self.conn:
            self.conn.execute("DELETE FROM favorites WHERE text=?", (text,))
        self.show_favorites()

    def show_tasbeeh(self):
        self.page = "tasbeeh"
        self.clear_content()
        c = self.palette()
        self.heading(self.content, "المسبحة الإلكترونية", "اضغط على الزر الكبير لزيادة عدد التسبيحات")
        card = self.card(self.content, padx=25, pady=25)
        card.pack(fill="both", expand=True, pady=8)
        tk.Label(card, text="سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
                 bg=c["surface"], fg=c["text"], font=("Arial", 21, "bold")).pack(pady=(15, 12))
        self.counter_label = tk.Label(card, text=str(self.tasbeeh_count),
                                      bg=c["surface"], fg=c["primary"],
                                      font=("Arial", 52, "bold"))
        self.counter_label.pack(pady=12)
        tk.Label(card, text=f"الهدف الحالي: {self.tasbeeh_target}",
                 bg=c["surface"], fg=c["muted"], font=("Arial", 12)).pack(pady=4)
        tk.Label(card, text="يُحفظ العدد تلقائياً بعد كل ضغطة، حتى بعد إغلاق التطبيق",
                 bg=c["surface"], fg=c["muted"], font=("Arial", 9)).pack(pady=2)
        self.make_button(card, "📿  تسبيحة جديدة", self.add_tasbeeh).pack(pady=14)
        row = tk.Frame(card, bg=c["surface"])
        row.pack(pady=8)
        self.make_button(row, "تصفير العداد", self.reset_tasbeeh, primary=False).pack(side="right", padx=5)
        self.make_button(row, "تغيير الذكر", self.change_dhikr, primary=False).pack(side="right", padx=5)
        self.make_button(row, "العودة للرئيسية", self.show_home, primary=False).pack(side="right", padx=5)

    def add_tasbeeh(self):
        self.tasbeeh_count += 1
        self.save_tasbeeh_count()  # حفظ بعد كل ضغطة مباشرة
        self.counter_label.configure(text=str(self.tasbeeh_count))
        if self.tasbeeh_count == self.tasbeeh_target:
            self.root.bell()
            messagebox.showinfo("اكتمل الهدف", "أحسنت! وصلت إلى هدفك من التسبيح.")

    def reset_tasbeeh(self):
        if messagebox.askyesno("تأكيد", "هل تريد تصفير عداد التسبيح؟"):
            self.tasbeeh_count = 0
            self.save_tasbeeh_count()
            self.counter_label.configure(text="0")

    def change_dhikr(self):
        choices = ["سُبْحَانَ اللَّهِ", "الْحَمْدُ لِلَّهِ", "اللَّهُ أَكْبَرُ",
                   "لَا إِلَهَ إِلَّا اللَّهُ", "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ"]
        win = tk.Toplevel(self.root)
        win.title("اختر الذكر")
        win.configure(bg=self.palette()["bg"])
        win.geometry("420x360")
        tk.Label(win, text="اختر الذكر الذي تريد ترديده", bg=self.palette()["bg"],
                 fg=self.palette()["text"], font=("Arial", 14, "bold")).pack(pady=15)
        for item in choices:
            self.make_button(win, item, lambda t=item: self.set_dhikr_label(t, win),
                             primary=False).pack(fill="x", padx=25, pady=5)

    def set_dhikr_label(self, text, win):
        win.destroy()
        # تحديث عنوان الذكر في صفحة المسبحة
        self.show_tasbeeh()
        for child in self.content.winfo_children():
            pass
        # حفظ الاختيار وعرضه في الصفحة التالية
        self.set_setting("selected_dhikr", text)
        self.show_tasbeeh()
        # العنوان هو أول Label داخل بطاقة المسبحة
        for widget in self.content.winfo_children():
            self._replace_dhikr_label(widget, text)

    def _replace_dhikr_label(self, widget, text):
        for child in widget.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") in (
                "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "سُبْحَانَ اللَّهِ",
                "الْحَمْدُ لِلَّهِ", "اللَّهُ أَكْبَرُ",
                "لَا إِلَهَ إِلَّا اللَّهُ", "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ"
            ):
                child.configure(text=text)
            self._replace_dhikr_label(child, text)

    def show_settings(self):
        self.page = "settings"
        self.clear_content()
        c = self.palette()
        self.heading(self.content, "الإعدادات", "خصّص مظهر التطبيق وطريقة عرض الأذكار")
        card = self.card(self.content)
        card.pack(fill="x", pady=8)
        tk.Label(card, text="المظهر", bg=c["surface"], fg=c["text"],
                 font=("Arial", 14, "bold")).pack(anchor="e", pady=8)
        self.make_button(card, "تبديل الوضع الليلي / النهاري", self.toggle_theme,
                         primary=False).pack(anchor="e", pady=5)
        tk.Label(card, text="حجم خط الأذكار", bg=c["surface"], fg=c["text"],
                 font=("Arial", 14, "bold")).pack(anchor="e", pady=(18, 5))
        scale = tk.Scale(card, from_=12, to=25, orient="horizontal",
                         command=self.change_font_size, bg=c["surface"],
                         fg=c["text"], highlightthickness=0, length=300)
        scale.set(self.font_size)
        scale.pack(anchor="e")
        tk.Label(card, text="حول التطبيق: الزميتة للأذكار - المطور أحمدو",
                 bg=c["surface"], fg=c["muted"], font=("Arial", 10)).pack(anchor="e", pady=(20, 4))
        tk.Label(card, text="مصادر الأذكار: حصن المسلم (سعيد بن وهف القحطاني) ومراجع السنة المذكورة في صفحات المصدر.",
                 bg=c["surface"], fg=c["muted"], font=("Arial", 9),
                 wraplength=650, justify="right").pack(anchor="e", pady=3)
        source_link = tk.Label(card, text="فتح النسخة العربية من حصن المسلم",
                               bg=c["surface"], fg=c["primary"], cursor="hand2",
                               font=("Arial", 10, "underline"))
        source_link.pack(anchor="e", pady=3)
        source_link.bind("<Button-1>", lambda event: webbrowser.open(
            "https://risala.prh.gov.sa/ar/content/51"))
        wa_link = tk.Label(card, text="التواصل مع المطور أحمدو عبر واتساب: +22244995677",
                           bg=c["surface"], fg="#159B61", cursor="hand2",
                           font=("Arial", 10, "bold"))
        wa_link.pack(anchor="e", pady=5)
        wa_link.bind("<Button-1>", lambda event: self.open_whatsapp())
        self.make_button(self.content, "العودة للرئيسية", self.show_home).pack(anchor="e", pady=10)

    def change_font_size(self, value):
        self.font_size = int(float(value))
        self.set_setting("font_size", self.font_size)

    def toggle_theme(self):
        self.dark = not self.dark
        self.set_setting("dark", "1" if self.dark else "0")
        # إعادة بناء الواجهة بالألوان الجديدة مع الاحتفاظ بالبيانات
        for widget in self.root.winfo_children():
            widget.destroy()
        self.colors = self.palette()
        self.root.configure(bg=self.colors["bg"])
        self.build_shell()
        if self.page == "tasbeeh":
            self.show_tasbeeh()
        elif self.page == "favorites":
            self.show_favorites()
        elif self.page == "settings":
            self.show_settings()
        elif self.page == "category" and self.current_category:
            self.render_adhkar()
        else:
            self.show_home()

    def open_whatsapp(self):
        """فتح محادثة واتساب مع المطور أحمدو."""
        webbrowser.open("https://wa.me/22244995677")

    def close(self):
        # حفظ أخير قبل إغلاق النافذة
        self.save_tasbeeh_count()
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = AdhkariApp(window)
    window.mainloop()
