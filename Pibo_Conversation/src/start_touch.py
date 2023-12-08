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
                
            cm.tts(bhv="do_question_S", string=f"활동 이름을 말씀해 주세요.")
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q="활동 이름을 말씀해 주세요.")
            print(answer)
            
            # 키워드 단순화
            # 1. 대화-자기소개
            if "소개" in answer[0][1] or "만나" in answer[0][1]:
                os.system('python3 /home/pi/Pibo_Package_07/Pibo_Conversation/src/greeting.py')
                break
            
            # 2. 대화-QR코드()
            if "카드" in answer[0][1] or "코드" in answer[0][1] or "예절" in answer[0][1]:
                cm.tts(bhv="do_question_L", string=f"잠시만 기다려줘.")
                os.system('python3 /home/pi/Pibo_Package_07/Pibo_Conversation/src/Etiquette/03_cough.py') 
                break
            
            # 3. 놀이-춤추는유령
            if "춤" in answer[0][1] or "유령" in answer[0][1]:
                cm.tts(bhv="do_question_L", string=f"잠시만 기다려줘.")
                os.system('python3 /home/pi/Pibo_Package_07/Pibo_Play/src/Com/com_4.py') 
                break
            
            # 4. 놀이-휴지길
            if "휴지" in answer[0][1] or "길" in answer[0][1]:
                cm.tts(bhv="do_question_L", string=f"잠시만 기다려줘.")
                os.system('python3 /home/pi/Pibo_Package_07/Pibo_Play/src/Cog/cog_1.py') 
                break
            
            else:
                oled.clear()
                continue
            
            # else:    
            #     cm.tts(bhv="do_question_L", string=f"새로운 활동을 시작해볼까?")
            #     answer = cm.responses_proc(re_bhv="do_question_L", re_q="오늘의 활동을 시작해볼까?",
            #                             pos_bhv="do_stop", pos=f"시작하자~", 
            #                             neg_bhv="do_stop", neg=f"알겠어. 나랑 놀고 싶다면 다시 쓰다듬어줘")
                
            #     time.sleep(1)
            #     if answer[0][0] == 'positive' or answer[0][0] == 'action':
            #         cm.tts(bhv="do_stop", string=f"잠시만 기다려줘. 재미있는 활동을 생각해볼께!")
            #         break
                    
            #     else:
            #         oled.clear()
            #         continue
            
            
# os.system('python3 /home/pi/Pibo_Package_07/Pibo_Conversation/src/schedule_run.py')
    
