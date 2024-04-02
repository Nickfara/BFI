import asyncio
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button

async def do_some_work():
    print('Work started')
    await asyncio.sleep(2)  # Асинхронно ждем 2 секунды
    print('Work finished')

class AsyncApp(App):
    def build(self):
        return Button(text="Do Work", on_press=self.on_button_press)

    def on_button_press(self, *args):
        asyncio.ensure_future(do_some_work())  # Запускаем асинхронную задачу

# Используем эту функцию для запуска цикла событий Kivy с интеграцией asyncio
def run_async():
    loop = asyncio.get_event_loop()

    # Запускаем цикл событий Kivy
    async_run = asyncio.ensure_future(asyncio.gather(AsyncApp().async_run(async_lib='asyncio')))
    # Планируем остановку цикла, когда Kivy App закроется
    async_run.add_done_callback(lambda *args: loop.stop())

    # Запускаем цикл событий asyncio
    loop.run_forever()

if __name__ == "__main__":
    run_async()