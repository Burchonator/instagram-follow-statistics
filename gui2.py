from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from functions import check_valid_password_length, login_to_instagram


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        # adds usename label
        labelUsername = Label(text='User Name')
        self.add_widget(labelUsername)
        # adds username input
        inputUsername = TextInput(multiline=False)
        self.add_widget(inputUsername)
        # adds password alabel
        labelPassword = Label(text='password')
        self.add_widget(labelPassword)
        # adds password input
        inputPassword = TextInput(password=True, multiline=False)
        self.add_widget(inputPassword)
        # self.add_widget(Button(text='Login'))
        btnLogin = (Button(text='Login'))
        self.add_widget(btnLogin)
        btnLogin.bind(on_press=lambda x: LoginButton.on_press(
            inputUsername.text, inputPassword.text))


class HomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


class LoginButton:
    def __init__(self, **kwargs):
        super(LoginButton, self).__init__(**kwargs)
        # self.source = 'atlas://data/images/defaulttheme/checkbox_off'

    def on_press(username, password):
        if check_valid_password_length(username, password):
            pass
        else:
            return
        if login_to_instagram(username, password):
            pass
        else:
            return
        return HomeScreen()


class MyApp(App):

    def build(self):
        # if the login was successful the user no longer needs log in and goes straight to homescreen.
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
