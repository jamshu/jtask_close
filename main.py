import kivy
kivy.require('1.0.9')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.app import App
import xmlrpclib
from kivy.storage.jsonstore import JsonStore

store = JsonStore('hello.json')
Builder.load_string('''
#:import JsonStore kivy.storage.jsonstore
#:import random random.random
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import WipeTransition kivy.uix.screenmanager.WipeTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import RiseInTransition kivy.uix.screenmanager.RiseInTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition
<HelloWorldScreen>:
    BoxLayout:
        orientation:'vertical'
        Label:
            id:status
            text: 'HI '
        Label:
            id:username
            text:'Good Day '
        Button:
            text: 'Close My Task'
            on_release: root.my_callback()
        Button:
            text:'Quit'
            on_release:App.on_stop()
        Button:
    	    text:'Config'
            on_release:root.manager.current = 'config'

<Configure>:
    BoxLayout:
        orientation:'vertical'
        Label:
            text:'Welcome To Configure Page'
        TextInput:
            id:username
            text:root.get_user()
            hint_text:'Username'
            size_hint_y:None
            height:120
        TextInput:
            id:pwd
            text:root.get_pwd()
            hint_text:'Password'
            size_hint_y:None
            height:120
        Button:
            text:'Save'
            on_release:root.save()
        Button:
            text:'Back'
            on_release:root.manager.current = 'first'

''')

class HelloWorldScreen(Screen):
    def my_callback(self):
        ip='support.orchiderp.com'
        db='orchid_support'
        user=''
        passwd='123'
        if not self.get_data():
            self.ids.status.text = 'Plz configure First'
            return True
        user,passwd = self.get_data()
        self.ids.username.text = user
        sock_common = xmlrpclib.ServerProxy ('http://'+ip+'/xmlrpc/common', allow_none=True)
        uid = sock_common.login(db, user, passwd)
        sock= xmlrpclib.ServerProxy('http://'+ip+'/xmlrpc/object', allow_none=True)
        task_id=sock.execute(db, uid, passwd, 'od.project.task', 'search', [('user_id','=',uid),('stage_id','!=',5)] )
        if not task_id:
            self.ids.status.text = 'There is no task to close'
            return True
        sock.execute(db, uid, passwd, 'od.project.task', 'write',task_id,{'stage_id':5})
        self.ids.status.text = 'Successfully Closed Your Task'
    def get_data(self):
        if store.exists('tito'):
            username =  store.get('tito')['username']
            pwd = store.get('tito')['pwd']
            return username,pwd
        return False
class Configure(Screen):
    def get_user(self):
        username =  store.get('tito')['username'] or ''
        return username
    def get_pwd(self):
        pwd = store.get('tito')['pwd'] or ''
        return pwd
    def save(self):
        name = self.ids.username.text
        pwd = self.ids.pwd.text
        # data_dir = getattr(self, 'user_data_dir') #get a writable path to save the file
        # store = JsonStore(join(data_dir, 'user.json'))
        store.put('tito', username=name, pwd=pwd)
        self.manager.current = 'first'


class HelloWorldApp(App):
    def build(self):
        root = ScreenManager()
        root.add_widget(HelloWorldScreen(name='first'))
        root.add_widget(Configure(name='config'))
        return root

if __name__ == '__main__':
    HelloWorldApp().run()
