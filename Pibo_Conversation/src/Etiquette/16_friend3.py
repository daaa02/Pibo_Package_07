# -*- coding: utf-8 -*-

# 사회기술-친구를 도와줘요

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Package_07/Pibo_Conversation/')
from data.c_conversation_manage import ConversationManage, WordManage, NLP
from data.speech_to_text import speech_to_text
from data.text_to_speech import TextToSpeech, text_to_speech
from data.spread import google_spread_sheet
from openpibo.vision import Camera
from openpibo.vision import Detect


pibo_camera = Camera()
pibo_detect = Detect()

cm = ConversationManage()
wm = WordManage()
nlp = NLP()
audio = TextToSpeech()
gss = google_spread_sheet()

folder = "/home/pi/UserData"
filename = os.path.basename(__file__).strip('.py')
today = datetime.now().strftime('%y%m%d_%H%M')
csv_conversation = open(f'{folder}/{today}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')


class Etiquette():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.correct = ['도와', '도우', '도울']
        self.ox = ''
                
        
    def Friend3(self):
        
        # 2.1 카드 대화
        pibo = cm.tts(bhv="do_question_L", string="이 카드의 어린이는 무엇을 잘못했을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="이 카드의 어린이는 무엇을 잘못했을까?",
                                   neg_bhv="do_suggestion_S", neg="같이 다시 한번 볼까?",
                                   neu_bhv="do_suggestion_S", neu="같이 다시 한번 볼까?")             
        
        if answer[0][0] == "action":            
            
            for i in range(len(self.correct)):
                if self.correct[i] in answer[0][1]:
                    self.ox = "(right)"                    
            if len(self.ox) == 0:
                self.ox = "(wrong ㅠㅠ)"
              
            if self.ox == "(right)":
                print(self.ox)
                pibo = cm.tts(bhv="do_compliment_S", string="맞아! 아주 똑똑한 걸?")
            else:
                print(self.ox)
                pibo = cm.tts(bhv="do_suggestion_S", string="또 무엇을 잘못했을까?")
                answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q="또 무엇을 잘못했을까?")
                
                if answer[0][0] == "action":        
                                
                    for i in range(len(self.correct)):
                        if self.correct[i] in answer[0][1]:
                            self.ox = "(right)"                    
                    if len(self.ox) == 0:
                        self.ox = "(wrong ㅠㅠ)"
                    
                    if self.ox == "(right)":
                        print(self.ox)
                        pibo = cm.tts(bhv="do_compliment_S", string="맞아! 아주 똑똑한 걸?")
                    else:
                        print(self.ox)
                        pibo = cm.tts(bhv="do_suggestion_S", string="같이 다시 한번 볼까?")
        
        pibo = cm.tts(bhv="do_explain_A", string="이 카드의 어린이는 친구를 도와주지 않고 있어.")
     
        # 2.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 친구를 잘 도와주니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 친구를 잘 도와주니?",
                                   pos_bhv="do_joy_A", pos="정말 대단한 걸!")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}도 도움이 필요한 적이 있었니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 도움이 필요한 적이 있었니?",
                                   pos_bhv="do_question_S", pos="언제였니?",
                                   neu_bhv="do_compliment_S", neu="기억이 안 날 수도 있지.")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="언제였니?",
                                       pos_bhv="do_compliment_S", pos="그 때 도움이 필요했구나!",
                                       neu_bhv="do_compliment_S", neu="기억이 안 날 수도 있어.")            
        
        # 2.3 문제 인식
        pibo = cm.tts(bhv="do_question_L", string="도움이 필요한 친구를 보면 어떻게 해야 할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="도움이 필요한 친구를 보면 어떻게 해야 할까?",
                                   pos_bhv="do_explain_B", pos="친구에게 어떻게 도와주면 좋을지 물어보면 좋을 것 같아.",
                                   neu_bhv="do_explain_B", neu="몰라도 괜찮아. 친구에게 어떻게 도와주면 좋을지 물어보면 좋을 것 같아.",
                                   act_bhv="do_explain_B", act="친구에게 어떻게 도와주면 좋을지 물어보면 좋을 것 같아.")
    
        # 3.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}에게 친구들이 도와 달라고 하면 도와주자. 할 수 없거나 위험한 일이라면 어른들께 도움을 구해 보는 것도 좋을 거야!")
    
        
        
        
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?")
              
        if answer[0][0] == "negative":
            cm.tts(bhv="do_joy_A", string=f"파이보는 {wm.word(self.user_name, 0)}랑 놀아서 재미있었어!")
            self.score = [0.0, -0.5, 0.0, 0.0]
        
        if answer[0][0] == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.5, 0.0, 0.0]
            
        if answer[0][0] != "negative" and answer[0][0] != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, -0.25, 0.0, 0.0]
        
        cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])

        # 종료 인사
        pibo = cm.tts(bhv="do_joy_A", string=f"나랑 놀아줘서 고마워~")

        # 4. Paradise framework 기록
        turns = sum((self.reject[i] + 1) * 2 for i in range(len(self.reject)))  
        reject = sum(self.reject) 
        
        cwc.writerow(['Turns', turns])
        cwc.writerow(['Rejections', reject])
        cwc.writerow(['Misrecognitions', ])

        cwc.writerow(['%Turns', ])
        cwc.writerow(['%Rejections', ])
        cwc.writerow(['%Misrecognitions', ])

        # 5. 활동 완료 기록
        gss.write_sheet(name=self.user_name, today=today, activities=filename)




if __name__ == "__main__":
    
    etq = Etiquette()
    etq.Friend3()