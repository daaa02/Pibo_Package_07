import os, sys, subprocess
import numpy as np
import pandas as pd
import random
import csv
import time
from datetime import datetime

from openpibo.audio import Audio
from openpibo.motion import Motion
from openpibo.oled import Oled


sys.path.append('/home/pi')
from schedule_update import UpdateSchedule
from Pibo_Package_07.Pibo_Conversation.data.text_to_speech import TextToSpeech, text_to_speech
from Pibo_Package_07.Pibo_Conversation.src.drive_upload import drive_upload

# sys.path.append('/home/pi/Pibo_Package_07/Pibo_Conversation/')
from Pibo_Package_07.Pibo_Conversation.data.c_conversation_manage import ConversationManage, WordManage
from Pibo_Package_07.Pibo_Conversation.data.text_to_speech import TextToSpeech, text_to_speech
import Pibo_Package_07.Pibo_Conversation.data.behavior.behavior_list as behavior


cm = ConversationManage()
wm = WordManage()
audio = TextToSpeech()


us = UpdateSchedule()
pibo_audio = Audio()
motion = Motion()
oled = Oled()


class RunSchedule():
    
    def __init__(self):
        self.path = '/home/pi/Pibo_Package_07'
        self.completion = int
        self.act = ''


    def day(self):
        UDfolder = "/home/pi/UserData"
        file = open(f"{UDfolder}/aa.csv", 'r', newline='', encoding='latin-1')
        cr = csv.reader((row.replace('\0', '').replace('\x00', '') for row in file),
                        delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')
        # cr = csv.reader(file, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')
        
        data1 = []
        data2 = []
        data3 = []
        
        for row in cr:
            # print(row[2:])      
            data1.append(row[2:])                       # 모든 행의 세 번째 열부터 취급
            
        data2 = data1[1:]
        # print(data2)                                  # [점수], [점수], ...
        self.completion = len(data2)
        print('완료한 활동 개수:', self.completion)
        
        
        cm.tts(bhv="do_question_S", string=f"활동 이름을 말씀해 주세요.")
        answer = cm.responses_proc(re_bhv="do_waiting_A", re_q="활동 이름을 말씀해 주세요.")
        print(answer)
        
        # 키워드 단순화
        
        # 1. 대화-자기소개
        if "소개" in answer[0][1] or "만나" in answer[0][1]:
            self.act = 'Pibo_Conversation/src/greeting.py'
        
        # 2. 대화-QR코드()
        if "카드" in answer[0][1] or "코드" in answer[0][1] or "예절" in answer[0][1]:
           self.act = 'Pibo_Conversation/src/Etiquette/03_cough.py'
        
        # 3. 놀이-춤추는유령
        if "춤" in answer[0][1] or "유령" in answer[0][1]:
            self.act = 'Pibo_Play/src/Com/com_4.py'
        
        # 4. 놀이-휴지길
        if "휴지" in answer[0][1] or "길" in answer[0][1]:
            self.act = 'Pibo_Play/src/Cog/cog_1.py'
        
        
        
        try:
            folder = "/home/pi/UserData"
            logfile = f'(P07)_{datetime.now().strftime("%m%d_%H%M")}.txt'   #('P<PACKAGE_NUMBER>_DATE.txt')   
            f = open(f'{folder}/{logfile}','w')
            
            # os.system(f'python3 {self.path}/{self.act}')
            out = subprocess.check_output([f'python3 {self.path}/{self.act}'], shell=True, stderr=subprocess.STDOUT, encoding="utf-8")  
            
            f.write(out)
            f.close()            
            
            try:
                drive_upload(filepath=f'{folder}/{logfile}', filename=logfile)
                
            except Exception as e:
                print(e)
            
            # 더 하고 싶다고 하면 여기서부터
            if self.completion >= 12:
                pass
            
            else:
                text_to_speech(text="파이보랑 또 놀자!")            
                motion.set_motion("m_wakeup", 1)
                subprocess.run(['python3 /home/pi/Pibo_Package_07/Pibo_Conversation/src/start_touch.py'], shell=True)
            # 여기까지 주석!! 대신 다음 활동 하려면 매번 재부팅 해야함
            
        except Exception as ex:
            with open('/home/pi/pibo_errmsg', 'w') as f:
                f.write(f'[{time.ctime()}]\n{ex}')
                
        
        



if __name__ == '__main__':
    
    # pibo_audio.mute(True)
    
    rs = RunSchedule()
    rs.day()