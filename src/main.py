from tkinter import *
import time
import datetime
import pyttsx3
import speech_recognition as sr
from PIL import ImageTk, Image
from threading import Thread
import sounddevice
import json


def shut_down():
    p1=Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()

def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
            if flag == False:
                #canvas.create_image(0, 0, image=img1, anchor=NW)
                #canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)

def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False


def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir. I am Albus. How can I Serve you?"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir. I am Albus. How can I Serve you?"
    else:
        text = "Good Evening sir. I am Albus. How can I Serve you?"

    canvas2.create_text(10, 10, anchor=NW, text=text, font=('Candara Light', -25, 'bold italic'), fill="white",
                        width=350)
    p1 = Thread(target=speak, args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    speak("I am listening.")
    flag = True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,timeout=10,phrase_time_limit=6)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")
        query = query.lower()
        #print(query)
        search(query)
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('fixedsys', -30),fill="white", width=350)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)

    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"

def search(query):
    global answer
    p = query.split()
    print(p[0])
    # for test in p:
       # print(test)
    myfile = open('Data.json','r')
    data = json.load(myfile)
    for i in data['Trains']:
       if i["train_name"] == p[0]:
           speak(i["departure"])
           answer = i["departure"]
           break

    canvas2.create_text(10, 225, anchor=NW, text= answer, font=('Candara Light', -25, 'bold italic'), fill="white",
                           width=350)

    myfile.close()



def main_window():
    global query
    wishme()
    while True:
        if query != None:
          if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
            shut_down()
            break
          else:
              search(query)






if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 10)

    root = Tk()
    root.title('Railway Chatbot')
    root.geometry('1360x690+-5+0')
    root.configure(background='white')


    #img1 = ImageTk.PhotoImage(Image.open("train.jpg"))
    img2 = ImageTk.PhotoImage(Image.open("button.png"))
    img3 = ImageTk.PhotoImage(Image.open("icon.png"))
    img4 = ImageTk.PhotoImage(Image.open("terminal.png"))
    background_image = ImageTk.PhotoImage(Image.open("last.png"))


    f = Frame(root, width=1360, height=690)
    f.place(x=0, y=0)
    f.tkraise()
    front_image = ImageTk.PhotoImage(Image.open("indianrailway.gif"))
    #front_image = PhotoImage(file="indian-railways.jpg")
    okVar = IntVar()
    btnOK = Button(f, image=front_image, command=lambda: okVar.set(1))
    btnOK.place(x=0, y=0)
    f.wait_variable(okVar)
    f.destroy()

    #trying to load json


    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=1)

    frames = [PhotoImage(file='chatgif.gif', format='gif -index %i' % (i)) for i in range(20)]
    canvas = Canvas(root, width=800, height=596)
    canvas.place(x=0, y=0)
    #canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root, image=img2, bd=0, command=takecommand)
    question_button.place(x=200, y=625)

    frame = Frame(root, width=500, height=596)
    frame.place(x=825, y=10)
    canvas2 = Canvas(frame, bg='#FFFFFF', width=500, height=596, scrollregion=(0, 0, 500, 900))
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500, height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT, expand=True, fill=BOTH)
    canvas2.create_image(0, 0, image=img4, anchor="nw")

    task = Thread(target=main_window)
    task.start()
    root.mainloop()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
