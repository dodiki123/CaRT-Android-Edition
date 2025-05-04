import os
import json
import math
import datetime
import locale
import webbrowser

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget

SETTINGS_FILE = "config.json"
TRANSLATIONS_DIR = "lang"

class TriangleApp(MDApp):
    def build(self):
        self.state = self.load_state()
        self.language = self.get_system_language()
        self.translations = self.load_language(self.language)
        self.theme_mode = self.state.get("theme", "Dark")
        self.history = self.state.get("history", [])

        self.theme_cls.theme_style = self.theme_mode.capitalize()
        self.theme_cls.primary_palette = "BlueGray"

        screen = MDScreen()
        self.tabs = MDBottomNavigation()

        # Check tab
        self.check_tab = MDBottomNavigationItem(name='check', text=self.t('check_title'), icon='triangle')
        self.input_a = MDTextField(hint_text=self.t("side_a"), mode="rectangle")
        self.input_b = MDTextField(hint_text=self.t("side_b"), mode="rectangle")
        self.input_c = MDTextField(hint_text=self.t("side_c"), mode="rectangle")
        self.result = MDLabel(text="", halign="center")
        self.solution = MDLabel(text=self.t("triangle_formula"), halign="center")
        self.check_btn = MDRaisedButton(text=self.t("check"), on_release=self.check_triangle, pos_hint={"center_x": 0.5})

        check_layout = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="35dp", spacing="25dp")
        check_layout.bind(minimum_height=check_layout.setter("height"))
        for widget in [self.input_a, self.input_b, self.input_c, self.check_btn, self.result, self.solution]:
            check_layout.add_widget(widget)
        scroll = MDScrollView()
        scroll.add_widget(check_layout)
        self.check_tab.add_widget(scroll)

        # History tab
        self.history_tab = MDBottomNavigationItem(name='history', text=self.t('history'), icon='history')
        self.history_list = MDScrollView()
        self.update_history_list()
        self.history_tab.add_widget(self.history_list)

        # Settings tab
        self.settings_tab = MDBottomNavigationItem(name='settings', text=self.t('settings'), icon='cog')
        settings_layout = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="25dp", spacing="25dp", size_hint_y=None)
        settings_layout.bind(minimum_height=settings_layout.setter("height"))

        self.lang_menu = MDDropdownMenu(
            caller=None,
            items=[{"text": lang, "on_release": lambda x=lang: self.change_language(x)} for lang in ["uk", "en", "de", "it", "es", "fr"]],
            width_mult=4
        )
        self.lang_btn = MDRaisedButton(text=self.language, on_release=lambda x: self.lang_menu.open(), pos_hint={"center_x": 0.5})
        self.lang_menu.caller = self.lang_btn

        self.theme_menu = MDDropdownMenu(
            caller=None,
            items=[{"text": theme, "on_release": lambda x=theme: self.change_theme(x)} for theme in ["Light", "Dark"]],
            width_mult=4
        )
        self.theme_btn = MDRaisedButton(text=self.theme_mode, on_release=lambda x: self.theme_menu.open(), pos_hint={"center_x": 0.5})
        self.theme_menu.caller = self.theme_btn
        
        self.change_lang = MDLabel(text=self.t("change_lang"), halign="center")
        self.switch_theme = MDLabel(text=self.t("switch_theme"), halign="center")
        
        for widget in [self.change_lang, self.lang_btn, self.switch_theme, self.theme_btn]:
            settings_layout.add_widget(widget)
        
        scroll_settings = MDScrollView()
        scroll_settings.add_widget(settings_layout)
        self.settings_tab.add_widget(scroll_settings)

        # About tab
        self.about_tab = MDBottomNavigationItem(name='about', text=self.t('about'), icon='information')
        about_layout = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="50dp", spacing="70dp", size_hint_y=None)
        about_layout.bind(minimum_height=about_layout.setter("height"))

        self.about_title = MDLabel(text=self.t("check_title"), halign="center")
        self.about_info = MDLabel(text=self.t("about_info"), halign="center")
        self.author_label = MDLabel(text=self.t("author"), halign="center")
        self.version_label = MDLabel(text=self.t("app_version"), halign="center")
        self.website_btn = MDRaisedButton(text=self.t("visit_site"), on_release=lambda x: self.open_website(), pos_hint={"center_x": 0.5})

        for widget in [self.about_title, self.about_info, self.author_label, self.version_label, self.website_btn]:
            about_layout.add_widget(widget)

        scroll_about = MDScrollView()
        scroll_about.add_widget(about_layout)
        self.about_tab.add_widget(scroll_about)

        for tab in [self.check_tab, self.history_tab, self.settings_tab, self.about_tab]:
            self.tabs.add_widget(tab)

        screen.add_widget(self.tabs)
        return screen

    def get_system_language(self):
        lang = locale.getdefaultlocale()[0]
        if lang and lang.startswith("ru"):
            return "uk"
        return self.state.get("language", "uk")

    def load_language(self, lang_code):
        path = os.path.join(TRANSLATIONS_DIR, f"{lang_code}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        if lang_code != "en":
            return self.load_language("en")
        return {}

    def t(self, key):
        return self.translations.get(key, key)

    def check_triangle(self, instance):
        try:
            a = float(self.input_a.text)
            b = float(self.input_b.text)
            c = float(self.input_c.text)
            if a <= 0 or b <= 0 or c <= 0:
                self.result.text = self.t("negative")
                return
            a2, b2, c2 = a ** 2, b ** 2, c ** 2
            s = a2 + b2
            self.solution.text = self.t("solution").format(a2=round(a2, 2), b2=round(b2, 2), sum=round(s, 2), c2=round(c2, 2))
            if math.isclose(s, c2, rel_tol=1e-9):
                self.result.text = self.t("right")
            else:
                self.result.text = self.t("not_right")
            entry = f"a={a}, b={b}, c={c} — {self.result.text} — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.history.append(entry)
            self.save_state()
            self.update_history_list()
        except ValueError:
            self.result.text = self.t("invalid")

    def update_history_list(self):
        scroll_box = MDBoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
        scroll_box.bind(minimum_height=scroll_box.setter('height'))

        for item in reversed(self.history[-100:]):
            scroll_box.add_widget(OneLineListItem(text=item, _no_ripple_effect=True))

        scroll = MDScrollView(size_hint=(1, 1))
        scroll.add_widget(scroll_box)

        clear_button = MDRaisedButton(
            text=self.t("clear_history"),
            on_release=self.clear_history,
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            width="40dp",
            height="10dp"
        )

        container = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        container.add_widget(scroll)
        container.add_widget(clear_button)

        self.history_list.clear_widgets()
        self.history_list.add_widget(container)


    def clear_history(self, *args):
        self.history.clear()
        self.save_state()
        self.update_history_list()

    def change_language(self, lang):
        self.language = lang
        self.translations = self.load_language(lang)
        self.lang_menu.caller.text = lang
        self.save_state()
        self.update_texts()

    def update_texts(self):
        self.check_tab.text = self.t("check_title")
        self.history_tab.text = self.t("history")
        self.settings_tab.text = self.t("settings")
        self.about_tab.text = self.t("about")

        self.input_a.hint_text = self.t("side_a")
        self.input_b.hint_text = self.t("side_b")
        self.input_c.hint_text = self.t("side_c")
        self.solution.text = self.t("triangle_formula")
        self.result.text = ""
        self.check_btn.text = self.t("check")
        self.lang_btn.text = self.language
        self.theme_btn.text = self.theme_mode
        self.change_lang.text = self.t("change_lang")
        self.switch_theme.text = self.t("switch_theme")

        self.about_title.text = self.t("check_title")
        self.about_info.text = self.t("about_info")
        self.author_label.text = self.t("author")
        self.version_label.text = self.t("app_version")
        self.website_btn.text = self.t("visit_site")

        self.update_history_list()

    def change_theme(self, theme):
        self.theme_mode = theme
        self.theme_cls.theme_style = self.theme_mode
        self.save_state()

    def open_website(self):
        webbrowser.open("https://sites.google.com/view/checking-a-right-triangle/%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BD%D0%B0-%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0")  # Замени на нужную ссылку

    def load_state(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_state(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "history": self.history,
                "language": self.language,
                "theme": self.theme_mode
            }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    TriangleApp().run()
