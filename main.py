from os import listdir
from os.path import isfile, join
from kivy.clock import mainthread
from kivymd.uix.boxlayout import MDBoxLayout as BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch as Switch
from kivymd.uix.textfield import MDTextField

onlyfiles = [f for f in listdir('documents') if isfile(join('documents', f))]

from copy import copy

import DB_Func
import autoclick


class Demo(MDApp):
    def __init__(self, **kwargs):  # Переменные класса
        super().__init__()
        # Оформление
        self.color_acent_1 = '#fefefe'
        self.color_acent_2 = '#fe433e'
        self.color_panel = '#272a2f'
        self.color_background = '#212429'
        self.scroll_layout = None
        self.shops = None  # Названия поставщиков
        self.btn_select_shop = None  # Выбранный поставщик
        self.doc = None # Накладная в словаре
        self.dialog = None # Диалоговое окно
        self.item_name = None # Выбранный из списка товар
        self.name_ = None # Наименование товара
        self.items = None  # Список товаров из iIko
        self.end_docList = None  # Готовая накладная, готовая к заведению
        self.drop = None
        self.menu_select_item = None  # Хранит в себе название товара если он один в поиске
        self.enter_for_save = False
        self.shops = ['Чек', 'КОФ (Передний лист)', 'КОФ (Полный список)', 'METRO', 'Матушка',
                      'Хозы', 'Юнит', 'Выпечка', 'Айсбери', 'ДЕСАН', 'Виста', 'Кофе', 'Арома']  # Названия поставщиков
        self.shops = sorted(self.shops)  # Сортировка
        # ______________________________Переключатели
        self.switch_name = Switch(width='64', track_color_active=self.color_acent_2, thumb_color_inactive=self.color_acent_2, thumb_color_active=self.color_background)
        self.switch_name.active = True
        self.switch_type = Switch(size_hint=(None, None), width='10dp', track_color_active=self.color_acent_2, thumb_color_inactive=self.color_acent_2, thumb_color_active=self.color_background)
        self.switch_type.active = True
        self.switch_count = Switch(size_hint=(None, None), width='10dp', track_color_active=self.color_acent_2, thumb_color_inactive=self.color_acent_2, thumb_color_active=self.color_background)
        self.switch_cost = Switch(size_hint=(None, None), width='10dp', track_color_active=self.color_acent_2, thumb_color_inactive=self.color_acent_2, thumb_color_active=self.color_background)
        self.switch_version = Switch(active=False, size_hint=(None, None), width='10dp', track_color_active=self.color_background, track_color_inactive=self.color_background, thumb_color_inactive=self.color_acent_1, thumb_color_active=self.color_acent_1)
        self.switch_version.bind(active=self.func_switch_version)
        switched = (self.switch_name, self.switch_type, self.switch_count, self.switch_cost, self.switch_version)

    def build(self):
        # ______________________________Выбор поставщика
        def add_button_shops():
            self.btn_select_shop = MDRectangleFlatButton(text='Поставщик', size_hint=(1, None), icon='plus', text_color=self.color_acent_1, line_color=self.color_acent_2)
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
            self.btn_input_doc_name = MDRectangleFlatButton(text='Накладная', size_hint=(1, None), text_color=self.color_acent_1, line_color=self.color_acent_2)
            menu_items = []
            for doc_name in onlyfiles:
                if doc_name.split('.')[1] in ['json', 'xls', 'xlsx']:
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
            switch_name_text = MDLabel(text='Название:', valign="center", halign="right", theme_text_color = 'Custom', text_color=self.color_acent_1)
            switch_type_text = MDLabel(text='Тип:', valign="center", halign="right", theme_text_color = 'Custom', text_color=self.color_acent_1)
            switch_count_text = MDLabel(text='Количество:', valign="center", halign="right", theme_text_color = 'Custom', text_color=self.color_acent_1)
            switch_cost_text = MDLabel(text='Цена:', valign="center", halign="right", theme_text_color = 'Custom', text_color=self.color_acent_1)
            switch_version_text = MDLabel(text='Режим:', valign="center", halign="right", theme_text_color = 'Custom', text_color=self.color_acent_1)
            switch_name_layout = BoxLayout(orientation='horizontal')
            switch_type_layout = BoxLayout(orientation='horizontal')
            switch_count_layout = BoxLayout(orientation='horizontal')
            switch_cost_layout = BoxLayout(orientation='horizontal')
            switch_version_layout = BoxLayout(orientation='horizontal')
            switch_name_layout.add_widget(switch_name_text)
            switch_name_layout.add_widget(self.switch_name)
            switch_type_layout.add_widget(switch_type_text)
            switch_type_layout.add_widget(self.switch_type)
            switch_count_layout.add_widget(switch_count_text)
            switch_count_layout.add_widget(self.switch_count)
            switch_cost_layout.add_widget(switch_cost_text)
            switch_cost_layout.add_widget(self.switch_cost)
            switch_version_layout.add_widget(switch_version_text)
            switch_version_layout.add_widget(self.switch_version)
            switch_all_layout = BoxLayout(orientation='vertical', padding=(0,0,50,0), size_hint_x=None, width=200, md_bg_color=self.color_panel)
            switch_all_layout.add_widget(switch_name_layout)
            switch_all_layout.add_widget(switch_type_layout)
            switch_all_layout.add_widget(switch_count_layout)
            switch_all_layout.add_widget(switch_cost_layout)
            switch_all_layout.add_widget(switch_version_layout)
            return switch_all_layout

        # _______________________________Остальные кнопки__________________________________________________
        btn_doc_read = MDRectangleFlatButton(text="Считать", on_release=self.func_doc_read, size_hint=(1, None), text_color=self.color_acent_1, line_color=self.color_acent_2)
        btn_doc_convert = MDRectangleFlatButton(text="Конвертировать", on_release=self.func_doc_convert_new, size_hint=(1, None), text_color=self.color_acent_1, line_color=self.color_acent_2)
        btn_launch_autoclick = MDRectangleFlatButton(text="Запустить автокликер", on_release=self.func_launch_autoclick, size_hint=(1, None), text_color=self.color_acent_1, line_color=self.color_acent_2)
        btn_menu_item = MDRectangleFlatButton(text="Редактировать товар", on_release=self.func_dialog_open, size_hint=(1, None), text_color=self.color_acent_1, line_color=self.color_acent_2)

        def sort_layouts():
            add_button_doc()
            add_button_shops()
            btn_select_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.btn_select_shop.height)
            btn_select_layout.add_widget(self.btn_select_shop)
            btn_select_layout.add_widget(self.btn_input_doc_name)
            btn_read_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.btn_select_shop.height)
            btn_read_layout.add_widget(btn_doc_read)
            btn_read_layout.add_widget(btn_doc_convert)
            btn_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=280, padding=10, spacing=10, md_bg_color=self.color_panel)
            btn_layout.add_widget(btn_select_layout)
            btn_layout.add_widget(btn_read_layout)
            btn_layout.add_widget(btn_menu_item)
            btn_layout.add_widget(BoxLayout())
            btn_layout.add_widget(btn_launch_autoclick)

            top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='285dp', md_bg_color=self.color_background)
            top_layout.add_widget(btn_layout)
            top_layout.add_widget(BoxLayout())
            top_layout.add_widget(switched())

            self.scroll_layout = BoxLayout(orientation='vertical', spacing=0)
            self.scroll_layout.size_hint_y = None
            self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
            scroll = ScrollView(size_hint=(1, 1),
                                do_scroll_x=False)
            scroll.add_widget(self.scroll_layout)

            layout = BoxLayout(orientation='vertical')
            layout.add_widget(top_layout)
            layout.add_widget(scroll)
            screen = Screen()
            screen.add_widget(layout)
            return screen

        self.items = copy(DB_Func.take_items())
        print(onlyfiles)
        return sort_layouts()

    # Считать накладную
    def func_doc_read(self, obj):
        from Scan_Doc import doc
        self.scroll_layout.clear_widgets()
        if self.btn_select_shop != 'Выбрать поставщика':
            if self.btn_select_shop.text == 'Чек':
                self.temp = doc(self.btn_select_shop.text, f"documents/{self.btn_input_doc_name.text}")
                self.doc = self.temp['items']
            else:
                self.doc = doc(self.btn_select_shop.text, f"documents/{self.btn_input_doc_name.text}")
            if self.doc == False:
                text = MDLabel(text='Поставщик введён неверно!')
                self.scroll_layout.clear_widgets()
                self.doc = None
        else:
            text = MDLabel(text='Поставщик не выбран!')
            self.scroll_layout.clear_widgets(text)

    # Первое выполнение конвертации
    def func_doc_convert_new(self, obj):
        self.end_docList = []
        self.func_doc_convert_repeat(obj)

    # Продолжение конвертации после не найденого товара
    def func_doc_convert_repeat(self, obj):
        self.end_docList = []
        if self.doc is None:
            self.scroll_layout.clear_widgets()
            self.scroll_layout.add_widget(MDLabel(text='Накладная не считана'))
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
                    temp['original'] = i['name']
                    self.end_docList.append(temp)
                self.ind_convert_item += 1
                self.scroll_layout.clear_widgets()
                if self.btn_select_shop.text == 'Чек':
                    list_items_text3 = MDLabel(text=f'Дата: {self.temp["date"]}\n')
                    list_items_text3.text += f'\nЧек : {self.temp["check"]}\n\n'
                    data_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='120dp')
                    data_layout.add_widget(list_items_text3)
                    self.scroll_layout.add_widget(data_layout)
            for i1 in self.end_docList:
                list_items_text1 = MDLabel(text = '\n' + f"{i1['id']}. {i1['original']} ||||| {i1['name']} |||||")
                list_items_text2 = MDLabel(text = '\n' + f"{i1['count']} X {i1['cost']} = {i1['sum'] if self.btn_select_shop == 'Чек' else ''}", halign="right", size_hint_x = None, width='190dp')
                text_item_Layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
                text_item_Layout.add_widget(list_items_text1)
                text_item_Layout.add_widget(list_items_text2)
                self.scroll_layout.add_widget(text_item_Layout)

    # Добавить товар
    def func_add_item(self, obj):
        print(self.list_.text)
        DB_Func.add_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    # Очистить товар
    def func_clear_item(self, obj):
        print(self.list_.text)
        DB_Func.clear_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    # Удалить товар
    def func_delete_item(self, obj):
        print(self.list_.text)
        DB_Func.delete_item(item=self.list_.text)
        self.items = copy(DB_Func.take_items())

    # Запуск автокликера
    def func_launch_autoclick(self, obj):
        print(self.switch_name.active)
        checkboxs = {'name': self.switch_name.active, 'type': self.switch_type.active,
                     'count': self.switch_count.active, 'cost': self.switch_cost.active}
        autoclick.start(self.end_docList, self.btn_select_shop, checkboxs)

    # Диалоговое окно - Открытие
    def func_dialog_open(self, obj):
        self.enter_for_save = False
        self.item_name = None
        btn_item_add = MDRectangleFlatButton(text="Добавить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_add_item)
        btn_item_delete = MDRectangleFlatButton(text="Удалить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_delete_item)
        btn_item_clear = MDRectangleFlatButton(text="Очистить товар", pos_hint={
            'center_x': 0.5, 'center_y': 0.6}, on_release=self.func_clear_item)
        name = self.name_['name'] if type(self.name_) == dict else 'none'
        text = f"Товар с наименованием: '{name}', не найден, выберите его из списка ниже! "
        if type(obj) is not int:
            if obj.text == 'Редактировать товар':
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
                if obj.text == 'Редактировать товар':
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

    # Диалоговое окно - Закрытие
    def func_dialog_close(self, obj):
        if obj.text == 'Закрыть':
            self.dialog.dismiss()
            self.enter_for_save = False
        else:
            self.doc.pop(self.ind_convert_item)
            self.dialog.dismiss()
            self.func_doc_convert_repeat(obj)
            self.enter_for_save = False

    # Диалоговое окно - Кнопка сохранить
    def func_dialog_save(self, obj):
        item = {self.item_name: self.items[self.item_name]}
        response = DB_Func.update_items(item, self.name_, self.items)
        self.enter_for_save = False
        if response != False:
            DB_Func.get_item(self.name_)
            self.dialog.dismiss()
            self.func_doc_convert_repeat(obj)

    # Диалоговое окно - Сохранить на ентер
    def func_dialog_save_enter(self, window, key, *args):
        if self.enter_for_save:
            print('Сработала функция нажатия Enter')
            if key == 13:
                self.func_dialog_save(key)

    # Диалоговое окно - Кнопка-название товара
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

    # Диалоговое окно - Кнопка-название товара (Активация через ентер)
    def func_dialog_enter(self, obj):
        obj = self.menu_select_item
        self.func_dialog_select(obj=obj)

    # Загрузка, поиск и отображение товаров в выпадающем списке
    def func_dialog_load(self, obj=None, item=None):
        if self.drop:
            self.drop.dismiss()
        text = self.list_.text.split(' ')
        menu_items = []
        for i in self.items:
            check = True
            for find_obj in text:
                if find_obj.lower() in i.lower():
                    pass
                else:
                    check = False

            if check:
                menu_items.append({
                    "text": f"{i}",
                    "on_release": lambda x=f"{i}": self.func_dialog_select(x),
                })

        if len(menu_items) > 0:
            self.menu_select_item = menu_items[0]['text']
        self.drop = MDDropdownMenu(items=menu_items)
        self.drop.caller = self.list_
        self.drop.open()

    # Кнопка выбора поставщика - Открытие диалогового окна
    def func_select_shop(self, obj):
        self.dropdown.open()

    # Кнопка-название поставщика - выбор поставщика и закрытие диалогового окна
    def func_select_shop_active(self, shop):
        self.dropdown.dismiss()
        self.btn_select_shop.text = shop

    # Кнопка выбора документа
    def func_select_doc(self, name):
        self.dropdown2.open()

    # Кнопка-название документа
    def func_select_doc_active(self, name):
        self.dropdown2.dismiss()
        self.btn_input_doc_name.text = name

    # Пустая функция
    def pass_(self, window, key, *args):
        pass

    # Переключатель режима автокликера
    def func_switch_version(self, obj, pos):
        self.switch_name.active = (False if pos else True)
        self.switch_type.active = (False if pos else True)
        self.switch_count.active = (True if pos else False)
        self.switch_cost.active = (True if pos else False)


if __name__ == "__main__":
    Demo().run()
