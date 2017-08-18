

#supposed to be a gui for this fucking awful app, sort of works but only if youre cool like me.
#gui made by W. R. R. Frey on 7/20/2017


from tkinter import Tk, Label, Button
import asyncio
from time import sleep

from fisher.connectors import TwilioConnector

from fisher.csapi import get_crn_status
from fisher.monitor import check_course
from fisher.monitor import target
from fisher.monitor import courses
from fisher.monitor import event_loop
from fisher.monitor import message_service
from fisher.monitor import run_coursefisher_service



class MyFirstGUI:

    #start_fishing_service = start_fishing()

    def __init__(self, master):
        master.title("A simple GUI")
        master.geometry(450,250)








root = Tk()
my_gui = MyFirstGUI(root)
#MyFirstGUI.start_fishing()
root.mainloop()

