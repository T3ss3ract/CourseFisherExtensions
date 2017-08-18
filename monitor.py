#!/usr/bin/env python


import asyncio
from time import sleep

from fisher.connectors import TwilioConnector

from fisher.csapi import get_crn_status

from  tkinter import *

import threading
import uiucapi

from PIL import Image

from tkinter import ttk
target = "+17205327798"

#drew_target = ""
courses = [
    "ECE 391 FA17 CRN47765",
    "CS 411 FA17 CRN30109",
    "ECON 302 FA17 CRN59661"
]




courses_2 = []
event_loop = asyncio.get_event_loop()
message_service = TwilioConnector()


def loadbar_update():
    step = 1/60
    loadbar.step(step)


async def check_course(course_string: str) -> None:
    global target
    course_status = await get_crn_status(course_string)
    #message_service.send(target = target, message ="this is a test message from the coursefisher service to see whether the check_course function is working.")
    if "open" in course_status.lower():
        message_service.send(target=target, message="Course {course} is open!".format(course=course_string))
    print(course_string + ": " + course_status + "\n")

halt_flag = 0
#TODO make pretty colors
#TODO long term: autoenroll feature??? would be fucking broken lmao
#global variable halt needs to actually work

def run_coursefisher_service():
    global halt_flag
    #message_service.send(target=target, message="Starting CourseFisher service!")   removed cause twilio number is running low niBBa
    while halt_flag == 0:
        for course in courses:
            event_loop.run_until_complete(check_course(course))
        sleep(180)
        if halt_flag == 1:
            break


start_button_text = "start service"
start_button_color = "green"
#TODO implement color change on button press


def run_coursefisher_thread():
    t = threading.Thread(target=run_coursefisher_service)
    loadbar_update()
    t.start()
    #return
    #TODO make loadbar work


def full_halt():
    global halt_flag
    halt_flag = 1
    f.destroy()

##w e w this code needs to be cleaned up before push



#gui code below
f = Tk()
#photo = PhotoImage(file = "loading.gif")
f.geometry("450x250")
b = Button(f, text = "start service", command = run_coursefisher_thread, fg = start_button_color)
b.pack()
c = Button(f, text = "close service" , command = full_halt)
c.pack()



class_title = Label(text = "course list")
class_title.pack()

#for i in courses:
 #   lab = Label(text = courses[i] + " ... ", fg = "blue")
  #  lab.pack()




lab1 = Label(text = courses[0] + " ... ", fg = "yellow")
lab1.pack()
lab2 = Label(text = courses[1] + " ... ", fg = "yellow")
lab2.pack()



loadbar = ttk.Progressbar(f, length = 60)
loadbar.pack()

#photo = PhotoImage(file = "loading.gif")
#photo = photo.zoom(40)
#photo = photo.subsample(90)
#load = Label(image = photo)
#load.pack()


f.mainloop()



