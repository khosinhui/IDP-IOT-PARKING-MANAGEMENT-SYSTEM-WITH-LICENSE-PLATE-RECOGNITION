from tkinter import*
import tkinter as tk
from firebase import firebase

firebase = firebase.FirebaseApplication('https://lpr-g2.firebaseio.com/',None)


prev = "" 
firebase.put('https://lpr-g2.firebaseio.com/',"Current_Plate","None")

while(1):
    plate_status = firebase.get('https://lpr-g2.firebaseio.com/',"Current_Plate")
    if(plate_status!="None"):
        if(prev != plate_status):
            root = tk.Tk()
            
            w = tk.Label(root, text=plate_status, font = "Verdana 50 bold")
            w.grid(row=1,column=0)
            root.after(5000,root.destroy)
            prev = plate_status
            root.mainloop()
    else:
        prev=""

    