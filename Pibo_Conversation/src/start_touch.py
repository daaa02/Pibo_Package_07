#!/usr/bin/python3

# python module
import os, sys
import time

# openpibo module
from openpibo.device import Device
from openpibo.oled import Oled
from openpibo.motion import Motion
from openpibo.audio import Audio

motion = Motion()
device = Device()
oled = Oled()
pibo_audio = Audio()
# pibo_audio.mute(True)

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Package_07/Pibo_Conversation/')
from data.c_conversation_manage import ConversationManage, WordManage
from data.text_to_speech import TextToSpeech, text_to_speech
import data.behavior.behavior_list as behavior

cm = ConversationManage()
wm = WordManage()
audio = TextToSpeech()

count = 0
state = ''


for i in range(0, 2):
    device.eye_off(); time.sleep(0.5); 
    device.eye_on(255,255,255); time.sleep(0.5)
    
while True:
    time.sleep(1)
    oled.clear()
    oled.set_font(size=17)
    oled.draw_text((20,15), "얼굴 가운데를")
    oled.draw_text((25,35), "쓰다듬어줘")
    oled.show()
    
    data = device.send_cmd(device.code_list['SYSTEM']).split(':')[1].split('-')
    result = data[1] if data[1] else "No signal"
    
    if result == "touch":
        count += 1
        print("touch:", count)
        
        if count >=1 :
            
            for i in range(0, 2):
                device.eye_off(); time.sleep(0.5); 
                device.eye_on(255,255,255); time.sleep(0.5) 
                
            break
            
os.system('python3 /home/pi/Pibo_Package_07/Pibo_Conversation/src/schedule_run.py')
    
