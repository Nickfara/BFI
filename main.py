from os import listdir
from os.path import isfile, join
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivymd.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivymd.uix.textfield import MDTextField

onlyfiles = [f for f in listdir('documents') if isfile(join('documents', f))]

from copy import copy

import DB_Func
import autoclick


class Demo(MDApp):
    def __init__(self, **kwargs):  # Переменные класса
        super().__init__()
        self.shops = None  # Названия поставщиков
        self.btn_select_shop = None  # Выбранный поставщик
        self.doc = None
        self.dialog = None
        self.item_name = None
        self.name_ = None
        self.items = None  # Список товаров из iIko
        self.end_docList = None  # Готовая накладная, готовая к заведению
        self.list_items = None  # Лэйбл списка товаров на экране
        self.drop = None
        self.menu_select_item = None  # Хранит в себе название товара если он один в поиске
        self.enter_for_save = False
        # ______________________________Переключатели
        self.switch_name = Switch(active=True, size_hint_x=None, width='100dp')
        self.switch_type = Switch(active=True, size_hint_x=None, width='100dp')
        self.switch_count = Switch(active=True, size_hint_x=None, width='100dp')
        self.switch_cost = Switch(active=True, size_hint_x=None, width='100dp')

    def build(self):
        # ______________________________Выбор поставщика
        def add_button_shops():
            self.shops = ['Чек', 'КОФ (Передний лист)', 'КОФ (Полный список)', 'METRO', 'Матушка',
                          'Хозы']  # Названия поставщиков
            self.btn_select_shop = MDRectangleFlatButton(text='Поставщик')
            menu_items = []
            for shop in self.shops:
                menu_items.append({
                    "text": f"{shop}",
                    "on_release": lambda x=f"{shop}": self.func_select_shop_active(x),
                })
            self.dropdown = MDDropdownMenu(items=menu_items)
            self.dropdown.caller = self.btn_select_shop
            self.btn_select_shop.bind(on_release=self.func_select_shop)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self.btn_select_shop, 'text', x))

        # _______________________________Выбор накладной
        def add_button_doc():
            self.btn_input_doc_name = MDRectangleFlatButton(text='Накладная')
            menu_items = []
            for doc_name in onlyfiles:
                menu_items.append({
                    "text": f"{doc_name}",
                    "on_release": lambda x=f"{doc_name}": self.func_select_doc_active(x),
                })
            self.dropdown2 = MDDropdownMenu(items=menu_items)
            self.dropdown2.caller = self.btn_input_doc_name
            self.btn_input_doc_name.bind(on_release=self.func_select_doc)
            self.dropdown2.bind(on_select=lambda instance, x: setattr(self.btn_input_doc_name, 'text', x))

        # _______________________________Переключатели
        def switched():
            switch_name_text = MDLabel(text='Ввод названия', valign="center", halign="right")
            switch_type_text = MDLabel(text='Ввод типа', valign="center", halign="right")
            switch_count_text = MDLabel(text='Ввод количества', valign="center", halign="right")
            switch_cost_text = MDLabel(text='Ввод цены', valign="center", halign="right")
            switch_name_layout = BoxLayout(orientation='horizontal')
            switch_type_layout = BoxLayout(orientation='horizontal')
            switch_count_layout = BoxLayout(orientation='horizontal')
            switch_cost_layout = BoxLayout(orientation='horizontal')
            switch_name_layout.add_widget(switch_name_text)
            switch_name_layout.add_widget(self.switch_name)
            switch_type_layout.add_widget(switch_type_text)
            switch_type_layout.add_widget(self.switch_type)
            switch_count_layout.add_widget(switch_count_text)
            switch_count_layout.add_widget(self.switch_count)
            switch_cost_layout.add_widget(switch_cost_text)
            switch_cost_layout.add_widget(self.switch_cost)
            switch_all_layout = BoxLayout(orientation='vertical')
            switch_all_layout.add_widget(switch_name_layout)
            switch_all_layout.add_widget(switch_type_layout)
            switch_all_layout.add_widget(switch_count_layout)
            switch_all_layout.add_widget(switch_cost_layout)
            return switch_all_layout

        # _______________________________Остальные кнопки__________________________________________________
        btn_doc_read = MDRectangleFlatButton(text="Считать", on_release=self.func_doc_read)
        btn_doc_convert = MDRectangleFlatButton(text="Конвертировать", on_release=self.func_doc_convert_new)
        btn_launch_autoclick = MDRectangleFlatButton(text="Запустить автокликер", on_release=self.func_launch_autoclick)
        btn_menu_item = MDRectangleFlatButton(text="Редактировать товар", on_release=self.func_dialog_open)

        self.list_items = MDLabel(text='Тут будет накладная')

        def sort_layouts():
            add_button_doc()
            add_button_shops()
            btn_layout = BoxLayout(orientation='vertical')
            btn_layout.add_widget(self.btn_select_shop)
            btn_layout.add_widget(self.btn_input_doc_name)
            btn_layout.add_widget(btn_doc_read)
            btn_layout.add_widget(btn_doc_convert)
            btn_layout.add_widget(btn_launch_autoclick)
            btn_layout.add_widget(btn_menu_item)

            top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='220dp')
            top_layout.add_widget(btn_layout)
            top_layout.add_widget(switched())

            scroll_layout = BoxLayout(orientation='vertical', spacing=0)
            scroll_layout.size_hint_y = None
            scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
            scroll_layout.add_widget(self.list_items)
            scroll = ScrollView(size_hint=(1, 1),
                                do_scroll_x=False)
            scroll.add_widget(scroll_layout)

            layout = BoxLayout(orientation='vertical')
            layout.add_widget(top_layout)
            layout.add_widget(scroll)
            screen = Screen()
            screen.add_widget(layout)
            return screen

        self.items = copy(DB_Func.take_items())
        print(onlyfiles)
        return sort_layouts()

    def func_doc_read(self, obj):  # Считать накладную
        from Scan_Doc import doc
        if self.btn_select_shop != 'Выбрать поставщика':
            if self.btn_select_shop.text == 'Чек':
                self.temp = doc(self.btn_select_shop.text, f"documents/{self.btn_input_doc_name.text}")
                self.doc = self.temp['items']

            else:
                self.list_items.text = ''
                self.doc = doc(self.btn_select_shop.text, f"documents/{self.btn_input_doc_name.text}")
            if self.doc == False:
                self.list_items.text = 'Поставщик введён неверно!'
                self.doc = None
        else:
            self.list_items.text = 'Поставщик не выбран!'

    def func_doc_convert_new(self, obj):  # Первое выполнение конвертации
        self.end_docList = []
        self.func_doc_convert_repeat(obj)

    def func_doc_convert_repeat(self, obj):  # Продолжение конвертации после не найденого товара
        self.end_docList = []
        if self.doc is None:
            self.list_items.text = 'Накладная не загружена'
        else:
            self.ind_convert_item = 0
            for i in self.doc:
                response = DB_Func.get_item(i)
                self.name_ = i
                if response == False:
                    self.func_dialog_open(obj)
                    break
                else:
                    temp = copy(i)
                    temp['name'] = response['item']
                    self.end_docList.append(temp)
                self.ind_convert_item += 1
                self.list_items.text = ''
                if self.btn_select_shop.text == 'Чек':
                    self.list_items.text = f'Дата: {self.temp["date"]}\n'
                    self.list_items.text += f'Чек : {self.temp["check"]}\n\n'
                for i1 in self.end_docList:
                    self.list_items.text += '\n' + str(i1)

    def func_add_item(self, obj):  # Добавить товар
        print(self.list_.text)
        DB_Func.add_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    def func_clear_item(self, obj):  # Очистить товар
        print(self.list_.text)
        DB_Func.clear_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    def func_delete_item(self, obj):  # Удалить товар
        print(self.list_.text)
        DB_Func.delete_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    @mainthread
    def func_launch_autoclick(self, obj):  # Запуск автокликера
        print(self.switch_name.active)
        checkboxs = {'name': self.switch_name.active, 'type': self.switch_type.active,
                     'count': self.switch_count.active, 'cost': self.switch_cost.active}
        autoclick.start(self.end_docList, self.btn_select_shop, checkboxs)

    def func_dialog_open(self, obj):
        self.enter_for_save = False
        btn_item_add = MDRectangleFlatButton(text="Добавить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_add_item)
        btn_item_delete = MDRectangleFlatButton(text="Удалить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_delete_item)
        btn_item_clear = MDRectangleFlatButton(text="Очистить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_clear_item)
        name = self.name_['name'] if type(self.name_) == dict else 'none'
        text = f"Товар с наименованием: '{name}', не найден, выберите его из списка ниже! "
        if type(obj) is not int:
            if obj.text == 'Редактировать товары':
                text = 'Выберите товар из списка, для редактирования!'
        btn_skip = MDFlatButton(text="Пропустить", text_color=self.theme_cls.primary_color,
                                on_release=self.func_dialog_close)
        btn_save = MDRectangleFlatButton(text="Сохранить", text_color=self.theme_cls.primary_color,
                                         on_release=self.func_dialog_save)
        self.list_ = MDTextField(hint_text="Поиск товара", on_text_validate=self.func_dialog_enter)
        self.list_.bind(text=self.func_dialog_load)
        self.dialog_layout = BoxLayout(spacing="12dp", size_hint_y=None, height="220dp", orientation='vertical')

        def sort_():
            btn_layout = BoxLayout(orientation='horizontal')
            btn_layout.add_widget(btn_skip)
            btn_layout.add_widget(btn_save)

            btn_item_layout = BoxLayout(orientation='horizontal')
            btn_item_layout.add_widget(btn_item_delete)
            btn_item_layout.add_widget(btn_item_clear)
            btn_item_layout.add_widget(btn_item_add)

            self.dialog_layout.add_widget(MDLabel(text=text))
            self.dialog_layout.add_widget(self.list_)

            if type(obj) is not int:
                if obj.text == 'Редактировать товары':
                    btn_layout.remove_widget(btn_skip)
                    btn_layout.remove_widget(btn_save)
                    btn_layout.add_widget(MDFlatButton(text="Закрыть", text_color=self.theme_cls.primary_color,
                                                       on_release=self.func_dialog_close))
            self.dialog_layout.add_widget(btn_item_layout)
            self.dialog_layout.add_widget(btn_layout)

            return self.dialog_layout

        title_text = "Товар не найден!"
        if type(obj) is not int:
            if obj.text == 'Редактировать товары':
                title_text = 'Настройки товаров!'

        self.dialog = MDDialog(title=title_text, type="custom", content_cls=sort_())
        self.dialog.open()

    def func_dialog_close(self, obj):
        if obj.text == 'Закрыть':
            self.dialog.dismiss()
            self.enter_for_save = False
        else:
            self.doc.pop(self.ind_convert_item)
            self.dialog.dismiss()
            self.func_doc_convert_repeat(obj)
            self.enter_for_save = False

    def func_dialog_save(self, obj):
        response = DB_Func.update_items(self.item_name, self.name_)
        self.enter_for_save = False
        if response != False:
            DB_Func.get_item(self.name_)
            self.dialog.dismiss()
            self.func_doc_convert_repeat(obj)

    def func_dialog_save_enter(self, window, key, *args):
        if self.enter_for_save:
            print('Сработала функция нажатия Enter')
            if key == 13:
                self.func_dialog_save(key)

    def func_dialog_select(self, obj):
        print('Выбран: ', str(obj))
        self.list_.text = str(obj)
        self.item_name = str(obj)
        self.drop.dismiss()
        self.root_window.bind(on_key_down=self.func_dialog_save_enter)
        if obj != '':
            self.enter_for_save = True
        else:
            self.enter_for_save = False

    def func_dialog_load(self, obj=None, item=None):
        if self.drop:
            self.drop.dismiss()
        text = self.list_.text.split(' ')
        menu_items = []
        for i in self.items:
            if text[0].lower() in i['item'].lower():
                if len(text) == 2:
                    if text[1].lower() in i['item'].lower():
                        menu_items.append({
                            "text": f"{i['item']}",
                            "on_release": lambda x=f"{i['item']}": self.func_dialog_select(x),
                        })
                else:
                    menu_items.append({
                        "text": f"{i['item']}",
                        "on_release": lambda x=f"{i['item']}": self.func_dialog_select(x),
                    })
        if len(menu_items) > 0:
            self.menu_select_item = menu_items[0]['text']
        self.drop = MDDropdownMenu(items=menu_items)
        self.drop.caller = self.list_
        self.drop.open()

    def func_dialog_enter(self, obj):
        obj = self.menu_select_item
        self.func_dialog_select(obj=obj)

    def func_select_shop(self, obj):
        self.dropdown.open()

    def func_select_shop_active(self, shop):
        self.dropdown.dismiss()
        self.btn_select_shop.text = shop

    def func_select_doc(self, name):
        self.dropdown2.open()

    def func_select_doc_active(self, name):
        self.dropdown2.dismiss()
        self.btn_input_doc_name.text = name

    def pass_(self, window, key, *args):
        pass


if __name__ == "__main__":
    Demo().run()
