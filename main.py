from fake_useragent import UserAgent
from requests import Session
from ttkbootstrap import *


class DiscordWebhook:
    user_agent = UserAgent()

    def __init__(self, *, url: str) -> None:
        self.url = url

    def send_message(self, message_text: str) -> None:
        with Session() as session:
            session.headers['User-Agent'] = self.user_agent.random

            session.post(url=self.url, json={'content': message_text})


class GUI:
    theme = 'superhero'

    def __init__(self, *, webhook: DiscordWebhook):
        self.window = Window(themename=self.theme, title='Webhook Dashboard')
        self.webhook = webhook

        ######
        self.window.iconbitmap('bin/icons/icon.ico')
        self.window.resizable(width=False, height=False)
        self.window.geometry('461x686+720+150')

        ######
        self.instruction_text = Label(self.window, text='Введите сообщение', font=('Arial', 17))
        self.messagebox = Entry(self.window, width=30)
        self.send_button = Button(self.window, text='Отправить', width=10, style='success', command=self.send)
        self.clear_button = Button(self.window, text='Отменить', width=10, style='danger', command=self.clear)

    def send(self):
        message_text = self.messagebox.get()
        self.clear()

        self.webhook.send_message(message_text=message_text)

    def clear(self):
        self.messagebox.delete(first=0, last=END)

    def place_widgets(self):
        self.instruction_text.place(relx=0.16, rely=0.20)
        self.messagebox.place(relx=0.16, rely=0.30)
        self.clear_button.place(relx=0.57, rely=0.40)
        self.send_button.place(relx=0.16, rely=0.40)

    def mainloop(self):
        self.place_widgets()
        self.window.mainloop()


class AuthorisationLoader:
    @staticmethod
    def load(file_path: str) -> str:
        with open(file=file_path, mode='r', encoding='UTF-8') as file:
            token = file.readline()

        return token


class Application:
    webhook = AuthorisationLoader.load(file_path='bin/authorisation/webhook.txt')

    @classmethod
    def launch(cls):
        webhook = DiscordWebhook(url=cls.webhook)
        interface = GUI(webhook=webhook)

        interface.mainloop()


if __name__ == '__main__':
    Application.launch()
