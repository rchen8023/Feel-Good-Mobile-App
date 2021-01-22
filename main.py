# resources: https://kivy.org/doc/stable/ 

import json
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
from datetime import datetime

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        # self is the object of LoginScreen class
        # manager is a property of the Screen
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "home_page"



class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        with open("users.json",'w') as file:
            json.dump(users,file)

        self.manager.current = "sign_up_done"

class SignUpDone(Screen):
    def go_to_main(self):
        # change the movement of the screen change. 
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class HomePage(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()