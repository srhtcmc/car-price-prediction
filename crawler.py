# get the data from script
import time
import webbrowser
import random
import pyautogui as pya
import pyperclip
from pynput.keyboard import Key, Controller



class GetNewPageUrl:
    
    def __init__(self,url):
        self.page_source = self.get_inf_from_webpage(url)
        
            
    def copy_clipboard(self):
        pya.hotkey('ctrl', 'c')
        time.sleep(.5)  # ctrl-c is usually very fast but your program may execute faster
        return pyperclip.paste()
    
    
    def get_inf_from_webpage(self,url):
        keybord = Controller()
        webbrowser.open(url)
        num = random.randint(5,7)
        
        time.sleep(num)
        
        keybord.press(Key.ctrl_l)
        keybord.press('u')
        keybord.release('u')
        keybord.release(Key.ctrl_l)
        
        time.sleep(num)
    
        
        keybord.press(Key.ctrl_l)
        keybord.press('a')
        keybord.release('a')
        keybord.release(Key.ctrl_l)
        
        time.sleep(0.5)
        
        var = self.copy_clipboard()
        pya.hotkey('alt', 'f4')
        return var
    

