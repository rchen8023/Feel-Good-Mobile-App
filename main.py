# resources: https://kivy.org/doc/stable/ 

import json, glob, random
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior

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
        else:
            self.ids.login_wrong.text = "Wrong username or password"

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        with open("users.json",'w') as file:
            json.dump(users,file)

        self.manager.current = "sign_up_done"
    def cancel_sign_up(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class SignUpDone(Screen):
    def go_to_main(self):
        # change the movement of the screen change. 
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class HomePage(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quotes(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("Texts/*txt") # get all the .txt files in Text file
        # if filename is "Text/happy.txt", Path(filename).stem = happy
        available_feelings = [Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(f"Texts/{feel}.txt",'r') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(HoverBehavior, ButtonBehavior, Image): # ButtonBehavior need to appear before Image
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()