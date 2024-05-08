import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import random
import wolframalpha
import calc
from keras.models import load_model
from PIL import Image, ImageOps 
import numpy as np
import cv2
import requests 
from bs4 import BeautifulSoup
face_cap = cv2.CascadeClassifier("C:/Users/sunil/OneDrive/Desktop/python/MY PYTHON/haarcascade_frontalface_default.xml")
video_cap = cv2.VideoCapture(0)
while True:
    ret, video_data = video_cap.read()
    col= cv2.cvtColor(video_data,cv2.COLOR_BGR2GRAY)
    faces = face_cap.detectMultiScale(
        col,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
     cv2.rectangle(video_data,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('Video_live', video_data)
    model = load_model('keras_Model.h5', compile=False)
    class_names = open('labels.txt', 'r').readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.fromarray(video_data).convert('RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    for i in prediction:
     if i[0] > 0.7:
        text ="Sir"
     if i[1] > 0.7:
        text = "Varin"
     if i[2] > 0.7:
        text = "Someone else"
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    


    if cv2.waitKey(10) == ord("a") :
        break
    video_cap.release()
    cv2.destroyAllWindows()
        #Video code 
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[1].id)
    engine.setProperty('voice', voices[2].id)
    print(voices)
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()


    def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            speak("Good Morning Sir!")

        elif hour>=12 and hour<18:
            speak("Good Afternoon Sir!")   

        else:
            speak("Good Evening Sir!")  

        speak("I am Friday . Please tell me how may I help you")       

    def takeCommand():
        #It takes microphone input from the user and returns string output

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            # print(e)    
            print("Say that again please...")  
            return "None"
        return query

    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('neekunj.singhipad@gmail.com', 'PaSS!@#$%')
        server.sendmail('varin.singhipad@gmail.com', to, content)
        server.close()
    def op():
         while True:
                query = takeCommand().lower()
                if 'wikipedia' in query:
                    
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open youtube' in query:
                    speak("Opening Youtube")
                    webbrowser.open("https://youtube.com")

                elif 'open google' in query:
                    speak("Opening Google")
                    webbrowser.open("https://google.com")

                elif 'open stack overflow' in query:
                    speak("Opening Stack Overflow")
                    webbrowser.open("https://stackoverflow.com")   

                elif 'open white hat junior' in query:
                    speak("Opening White Hat Junior")
                    webbrowser.open("https://code.whitehatjr.com/s/dashboard")

                elif 'open code.org' in query:
                    speak("Opening Code.org")
                    webbrowser.open("https://studio.code.org/home")

                elif 'open ti launcher' in query:
                    speak("Opening Tlauncher")
                    Path="C:\\Users\\sunil\\AppData\\Roaming\\.minecraft\\TLauncher.exe"
                    os.startfile(Path)
                elif 'play music' in query:
                    speak("Playing Music")
                    n = random.randint(0,16)
                    print(n)
                    music_dir = 'D:\Music\FAvourite songs'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[n]))
                    
                elif 'what is the time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                    speak(f"Sir, the time is {strTime}")
                    print(strTime)

                elif 'open code' in query:
                    speak("Opening Code")
                    codePath = "C:\\Users\\sunil\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(codePath)

                elif 'email to worry' in query:
                    try:
                        speak("What should I say?")
                        content = takeCommand()
                        to = "varin.singhipad@gmail.com"    
                        sendEmail(to, content)
                        speak("Email has been sent!")
                    except Exception as e:
                        print(e)
                        speak("Sorry Sir. I am not able to send this email")
                        
                elif "calculate" in query:
                    from calculator import WolfRamAlpha
                    from calculator import Calc
                    query = query.replace("calculate","")
                    query = query.replace("friday","")
                    Calc(query)       
                elif "very good friday" in query:
                    speak("Thank You Sir")
                elif "how is the weather today" in query:
                     speak("Which City")
                     city=takeCommand()
                     speak("Telling  Weather report")
                     url = f"https://www.google.com/search?q=weather+{city}"
                     res = requests.get(url)
                     data = BeautifulSoup(res.text,"html.parser")
                     temp = data.find("div",class_="BNeawe").text
                     print(f"current {city} is{temp} ")
                     speak(f"current {city} is{temp} ")
                elif 'quit' in query:
                    exit()

    if __name__ == "__main__":
     while True:
        
        if 'Sir' in class_name:
         wishMe()  
         print( class_name, end='')
         op()
        if 'Varin' in class_name:
         wishMe()  
         print( class_name, end='')
         op() 
        if 'Someone else' in class_name:
         wishMe()  
         print( class_name, end='')
         op()
        