import datetime
from calendar import monthrange
import calendar

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import ast

global calendarFrame
global statWindow

day_widgets = []

savedMonths = []
savedDays = []

f_savedDays = []

currentFilePath = None
statWindow = None

import os

minres = (720, 360)

streak = 0

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def clear_frame(frame, header=None):
   for widgets in frame.winfo_children():
      widgets.destroy()

def SendMsgBoxCustom(message):
   messagebox.showinfo(title=None, message=message)

def SendMsgBox():
   msg_box = messagebox.askquestion('Confirmation', 'Are you sure you want to clear all data?',
                                        icon='warning')
   if msg_box == 'yes':
         ClearData()

def AskForSave():
   t = root.title()
   if f_savedDays != savedDays:
      print(str(f_savedDays == savedDays))
      filename = os.path.basename(currentFilePath)
      if filename != '' and filename != None:
         text = 'Save changes to ' + filename + '?'
      else:
         text = 'Do you want to save the file?'
      msg_box = messagebox.askyesnocancel(message=text, icon='question', title='Save file')
      if msg_box == True:
         save()
         root.destroy()
      if msg_box == False:
         root.destroy()
   else:
      root.destroy()
         

def ClearData():
   open(currentFilePath, 'w').close()
   open(currentFilePath, 'w').close()
   savedMonths.clear()
   savedDays.clear()
   f_savedDays.clear()
   streakText.set('')
   for widg in day_widgets:
      widg.var.set(0)

def DestroyWindow(window):
   global statWindow
   statWindow = None
   window.destroy()


def get_stats():
   #count how many days are checked
   totalDayCount = 0
   for monthDays in savedDays:
      totalDayCount += monthDays.count(1)

   firstCheckedMo = savedMonths[0]
   firstCheckedDay = savedDays[0].index(1)+1 #index returns first occurrence of element
   firstCheckedDate = datetime.datetime(firstCheckedMo[1], firstCheckedMo[0], firstCheckedDay)

   #days passed since first check
   firstCheckedId = savedDays[0].index(1)
   firstMoDaysPassed = len(savedDays[0][firstCheckedId:])
   if savedMonths[0][0] == tMonth:
      firstMoDaysPassed = tDay - firstCheckedId
   print('first mo days passed: ' + str(firstMoDaysPassed))
   counter = 0
   tempMo = savedMonths[0][0]+1
   tempYear = savedMonths[0][1]
   print('temp vars: ' + str(tempMo) + ' ' + str(tempYear))
   print('today vars: ' + str(tMonth) + ' ' + str(tYear))
   if tempMo >= 12:
      tempMo = 1
      tempYear += 1
   while tempYear == tYear and tempMo <= tMonth or tempYear < tYear:
      if tempMo != tMonth or tempYear != tYear:
         counter+=number_of_days_in_month(tempMo, tempYear)
      else:
         counter+=tDay
      tempMo+=1
      if tempMo == 13:
         tempMo = 1
         tempYear+=1
   print(str(tempMo), str(tempYear))
   print('counter: ' + str(counter))
   daysPassed = counter + firstMoDaysPassed - 1

      
   return [totalDayCount, firstCheckedDate, daysPassed]

def OpenStatsWindow():
   global statWindow
   #statWindow is the global var for the stats window and statsWindow is just referring to it in the update function
   if statWindow == None:
      statWindow = Toplevel(root)
      statWindow['background'] = 'black'
      statWindow.minsize(180, 360)
      statWindow.resizable(False, False)
      statWindow.protocol("WM_DELETE_WINDOW", lambda: DestroyWindow(statWindow))
      UpdateStatsWindow(statWindow)
      
   else:
      statWindow.focus_set()

def UpdateStatsWindow(statsWindow, strk=None, maxStrk=None):
   stats = get_stats()

   clear_frame(statsWindow)
   
   stwHeadframe = ttk.Frame(statsWindow)
   stwHeadframe.grid(column=0,row=0)
   stwHeadframe.columnconfigure(0,weight=1)
   stwHeadframe.rowconfigure(0,weight=1)
   
   stwFrame1 = ttk.Frame(statsWindow, borderwidth=5, relief='ridge')
   stwFrame1.grid(column=0,row=1)
   stwFrame1.columnconfigure(0,weight=1)
   for row in range(1):
      stwFrame1.rowconfigure(row,weight=1)

   stwFrame2 = ttk.Frame(statsWindow, borderwidth=5, relief='ridge')
   stwFrame2.grid(column=0,row=2, sticky=(W, E))
   stwFrame2.columnconfigure(0,weight=1)
   for row in range(1):
      stwFrame2.rowconfigure(row,weight=1)
   
   ttk.Label(stwHeadframe, text="Stats").grid(column=0,row=0)
   
   ttk.Label(stwFrame1, text=str(stats[0]) + ' Days Checked').grid(column=0, row=0, sticky=(W))

   ttk.Label(stwFrame1, text='First checked day: ' + stats[1].strftime("%d %b %Y")).grid(column=0,row=1, sticky=(W))

   ttk.Label(stwFrame1, text='Days passed since first check: ' + str(stats[2])).grid(column=0,row=2,sticky=(W))

   if strk == None:
      strk, maxStrk = calculate_streak()
   ttk.Label(stwFrame2, text='Current Streak: ' + str(strk) + ' days').grid(column=0, row=0, sticky=(W))
   ttk.Label(stwFrame2, text='Maximum Streak: ' + str(maxStrk) + ' days').grid(column=0, row=1, sticky=(W))

   for child in statsWindow.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

def calculate_streak():
   if len(savedMonths) == 0:
         return 0, 0
   
   currentDate = datetime.datetime.now()
   streak = 0
   streaks = []
   todayMo = currentDate.month
   todayYear = currentDate.year
   todayDay = currentDate.day

   minStreak = 3
   
   if [todayMo, todayYear] in savedMonths:
      currentMo = todayMo
      currentYear = todayYear
      init = savedMonths.index([todayMo, todayYear])
      ind = savedMonths.index([currentMo, currentYear])
      j = todayDay-1
   else:
      if todayDay == 1:
         if todayMo == 1:
            currentMo = 12
            currentYear = todayYear-1
         else:
            currentMo = todayMo-1
            currentYear = todayYear
         if [currentMo, currentYear] not in savedMonths:
            streaks.append(streak)
   
         init = None
         ind = savedMonths.index([currentMo, currentYear])
         j = number_of_days_in_month(currentMo, currentYear)-1
      else:
         streaks.append(streak)
         temp = len(savedMonths)-1
         while savedMonths[temp][0] > todayMo and savedMonths[temp][1] > todayYear:
            temp-=1
         if temp >= 0:
            ind = temp
            currentMo = savedMonths[ind][0]
            currentYear = savedMonths[ind][1]
            j = number_of_days_in_month(currentMo, currentYear)-1
            init = None
         else:
            return 0, 0

   
   print(str(savedDays[ind][j]))
   print('Streak parameters: ')
   print(str(currentMo), str(currentYear), str(ind), str(j))
   while j >= 0:
      if savedDays[ind][j] == 1:
         streak+=1
      elif j != todayDay-1 or ind != init: # Allow streak to continue even if the current day is still not checked
         print('Broke out of streak')
         if len(streaks) == 2:
            if streak >= streaks[1]:
               streaks[1] = streak
         else:
            streaks.append(streak)
         streak = 0
         #return streak
      if j == 0 and ind > 0:
         if currentMo > 1:
            if [currentMo-1, currentYear] in savedMonths:
               currentMo-=1
               ind = savedMonths.index([currentMo, currentYear])
               print(str(currentMo), str(currentYear))
               j = number_of_days_in_month(savedMonths[ind][0], savedMonths[ind][1])
            else:
               if len(streaks) == 2:
                  if streak >= streaks[1]:
                     streaks[1] = streak
               else:
                  streaks.append(streak)
               streak = 0
               ind-=1
               currentMo, currentYear = savedMonths[ind][0], savedMonths[ind][1]
               j = number_of_days_in_month(savedMonths[ind][0], savedMonths[ind][1])
               #return streak
         if currentMo == 1 and j == 0:
            if [12, currentYear-1] in savedMonths:
               currentMo, currentYear = 12, currentYear-1
               ind = savedMonths.index([currentMo, currentYear])
               print(str(currentMo), str(currentYear))
               j = number_of_days_in_month(savedMonths[ind][0], savedMonths[ind][1])
            else:
               if len(streaks) == 2:
                  if streak >= streaks[1]:
                     streaks[1] = streak
               else:
                  streaks.append(streak)
               streak = 0
               ind-=1
               j = number_of_days_in_month(savedMonths[ind][0], savedMonths[ind][1])
               currentMo, currentYear = savedMonths[ind][0], savedMonths[ind][1]
               #return streak
      j-=1
      if ind == 0 and j == 0:
         if savedDays[ind][j] == 1:
            streak+=1
         #^ new line so it doesnt skip the first day of month when there's no previous month saved
         if streak > 0:
            if len(streaks) < 2:
               streaks.append(streak)
            else:
               if streak > streaks[1]:
                  streaks[1] = streak
         print(streaks)
         if streaks == [] or len(streaks) == 1:
            return streak, streak
         currentStreak = streaks[0]
         if streaks[1] > streaks[0]:
            maxStreak = streaks[1]
         else:
            maxStreak = currentStreak
         return currentStreak, maxStreak

def apply_streak(strk=None, maxStrk=None):
   if showStreak.get() == False:
      streakText.set('')
      return None
   if strk == None:
      strk, maxStrk = calculate_streak()
   if strk == None:
      streakText.set('')
      return False
   if strk >= 3:
      streakText.set(str(strk) + ' Day Streak!')
   else:
      streakText.set('')
   if strk >= 3 and maxStrk > strk:
      streakText.set(str(strk) + ' Day Streak!\nMaximum Day Streak: ' + str(maxStrk))
   if strk < 3 and maxStrk > strk and maxStrk >= 3:
      streakText.set('Maximum Streak: ' + str(maxStrk) + ' Days')

      
   print(str(maxStrk))


def upon_select(widget):
    print('---------------------------')
    save_internal(monthVar, yearVar, day_widgets)

def number_of_days_in_month(m, y):
    return monthrange(y, m)[1]

def sort_months():
   global savedMonths
   global savedDays
   if len(savedMonths) >= 2:
      savedMonths, savedDays = (list(t) for t in zip(*sorted(zip(savedMonths, savedDays),key=lambda x:(x[0][1],x[0][0]))))
      print('Sorted months:')
      print(savedMonths)

def draw_calendar(m, y):
    day_widgets.clear()
    clear_frame(calendarFrame)
    currentColumn = 0
    currentRow = 0
    for i in range(number_of_days_in_month(m,y)):
        if currentColumn >= 11:
            if currentRow < 4:
                currentRow+=1
            currentColumn = 0
        w = ttk.Checkbutton(calendarFrame, text=str(i+1))
        w.var = IntVar()
        if ([m,y] in savedMonths):
            t = savedMonths.index([m,y])
            w.var.set(savedDays[t][i])
        w['variable'] = w.var
        w['command'] = lambda widg=w: \
                                                                    upon_select(widg)
        disableWidget = disableFutureDays.get()
        if m == tMonth and y == tYear and i > tDay-1 and disableWidget == True or m > tMonth and y >= tYear and disableWidget == True:
           w['state'] = 'disabled'
        w.grid(column=currentColumn, row=currentRow)
        day_widgets.append(w)
        currentColumn += 1
        for child in calendarFrame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

def change_month(operationType, mName, m, yVar, yearChanging=False):
   y = yVar.get()
   v = m.get()

   if yearChanging==False:
      #save_internal(m, yVar, day_widgets)
      pass
   
   if operationType == '+':
      v+=1
      if v > 12:
         v = 1
         y+=1
   if operationType == '-':
      v-=1
      if v < 1:
         v = 12
         y-=1
   m.set(v)
   yVar.set(y)
   
   mName.set(calendar.month_name[v])
   draw_calendar(v, y)
   
   print(v)

def change_year(operationType, var, mName, m):
    v = var.get()
    save_internal(m, var, day_widgets)
    if operationType == '+':
        v+=1
        var.set(v)
    if operationType == '-':
        v-=1
        var.set(v)
    day_widgets.clear()
    change_month('', mName, m, var, yearChanging=True)

def save_internal(mo, yVar, daylist):
   m = mo.get()
   print(m)
   y = yVar.get()

   days = []
   for i in daylist:
      days.append(i.var.get())
   print(days)
   
   if ([m,y] in savedMonths):
      t = savedMonths.index([m,y])
      #Remove from data if there are no days saved anymore
      if 1 not in days:


         
         del savedMonths[t]
         del savedDays[t]
         sort_months()
         st, maxSt = calculate_streak()
         apply_streak(strk=st, maxStrk = maxSt)

         menu_show.entryconfigure('Show statistics', state=DISABLED)
         return False
      lineToEdit = savedMonths.index([m,y])
      savedDays[t] = days

   #Do not allow save for no days
   if 1 not in days:
      sort_months()
      apply_streak()
      return False

   if ([m,y] not in savedMonths):
      savedMonths.append([m,y])
      savedDays.append(days)

   sort_months()
   st, maxSt = calculate_streak()
   apply_streak(strk=st, maxStrk = maxSt)
   if statWindow != None:
      UpdateStatsWindow(statWindow, strk=st, maxStrk=maxSt)
   
   if currentFilePath != '' and currentFilePath != None: #Show in title that file has unsaved changes
      oldtitle = root.title()
      print(str(f_savedDays == savedDays))
      print(f_savedDays)
      if f_savedDays != savedDays and '*' not in oldtitle:
         
         oldtitle += '*'
         root.title(oldtitle)
      if f_savedDays  == savedDays and '*' in oldtitle:
         oldtitle = oldtitle.replace('*','')
         print(oldtitle)
         root.title(oldtitle)

   if len(savedMonths) > 0:
      menu_show.entryconfigure('Show statistics', state=NORMAL)
      
   
   print('Saved internally.')
   print(savedMonths)
   print(savedDays)

def newFile():
   global currentFilePath
   savedMonths.clear()
   savedDays.clear()
   f_savedDays.clear()
   draw_calendar(month,year)
   save_internal(monthVar, yearVar, day_widgets)
   

   with open('recentfile.txt', 'w') as filehandle:
      filehandle.write('')
      filehandle.close()
   currentFilePath = ''
   root.title('Habit Tracker')
   menu_show.entryconfigure('Show statistics', state=DISABLED)

def openFile():
   fileToOpen = filedialog.askopenfilename()
   if fileToOpen != '' and fileToOpen != None:
      load(fileToOpen)
      menu_show.entryconfigure('Show statistics', state=NORMAL)

def save(saveAs=False):
   global currentFilePath

   if len(savedDays) <= 0:
      SendMsgBoxCustom('Cannot save empty file')
      return False
   
   print('Current path: ', currentFilePath)
   save_internal(monthVar, yearVar, day_widgets)
   if currentFilePath == '' or currentFilePath == None or saveAs == True:
      currentFilePath = filedialog.asksaveasfilename(filetypes=[('Habit Tracker File', '*.hbt'), ('All Files', '*.*')], defaultextension=[('Habit Tracker File', '*.hbt'), ('All Files', '*.*')])

   if currentFilePath == '' or currentFilePath == None:
      return False
   
   with open(currentFilePath, 'w') as filehandle:
      print('Opened ', currentFilePath)
      print(len(savedMonths)-1)
      for listitem in range(len(savedMonths)):
         filehandle.write('%s - %s\n' % (savedMonths[listitem], savedDays[listitem]))
         print(str(listitem))
         print('%s - %s\n' % (savedMonths[listitem], savedDays[listitem]))
      f_savedDays.clear()
      for element in savedDays:
         f_savedDays.append(element)
      oldtitle = root.title()
      if '*' in oldtitle:
         oldtitle.replace('*','')
         root.title(oldtitle)
      
      filename = os.path.basename(currentFilePath)
      root.title('Habit Tracker - ' + filename)
      set_recent_file()



def load(filepath):
   global currentFilePath
   global f_savedDays

   savedDays.clear()
   savedMonths.clear()
   
   month = tMonth
   year = tYear

   monthVar.set(month)
   yearVar.set(year)
   monthName.set(calendar.month_name[month])
   
   with open(filepath, 'r') as filehandle:
      stringMonths = []
      stringDays = []
      for line in filehandle:

      
         # remove linebreak which is the last character of the string
         currentLine = line[:-1].split(' - ')

         currentMonth = currentLine[0]
         currentDayArray = currentLine[1]
         # add item to the list
         currentMonth = ast.literal_eval(currentMonth)
         currentDayArray = ast.literal_eval(currentDayArray)
         savedMonths.append(currentMonth)
         savedDays.append(currentDayArray)
   print(savedMonths, savedDays)
   f_savedDays.clear()
   for element in savedDays:
      f_savedDays.append(element)
   currentFilePath = filepath
   filename = os.path.basename(currentFilePath)
   root.title('Habit Tracker - ' + filename)


   if filepath != '' and filepath != None:
      menu_show.entryconfigure('Show statistics', state=NORMAL)
   
   sort_months()
   draw_calendar(month,year)
   apply_streak()
    
def initialize():
   global currentFilePath
   if os.path.exists('recentfile.txt'):
      with open('recentfile.txt', 'r') as filehandle:
         currentFilePath = filehandle.read()
         print('Loaded ' + currentFilePath + ' on start')
      if currentFilePath != '' and currentFilePath != None:
         load(currentFilePath)
      else:
         menu_show.entryconfigure('Show statistics', state=DISABLED)

def set_recent_file():
   global currentFilePath
   with open('recentfile.txt', 'w') as filehandle:
      filehandle.write(currentFilePath)
   print(currentFilePath)
   filehandle.close()
   

def check_all(uncheck):
   for widg in day_widgets:
      st = str(widg['state'])
      if st!='disabled':
         v = widg.var.get()
         if uncheck == False:
            if v == 0:
               widg.var.set(1)
         if uncheck == True:
            if v == 1:
               widg.var.set(0)
   save_internal(monthVar, yearVar, day_widgets)

root = Tk()
root.title("Habit Tracker")
#root['background'] = '#5A5A5A'

root.tk.call('lappend', 'auto_path', 'C:\\awthemes')
root.tk.call('package', 'require', 'awdark') #DOES NOT WORK FOR SOME FUCKING REASON

#s = ttk.Style()
#print(s.theme_use('awdark'))

root.minsize(720, 360)
root.resizable(False, False)
root.option_add('*tearOff', FALSE)

streakText = StringVar()

menubar = Menu(root)
root['menu'] = menubar
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menu_preferences = Menu(menubar)
menu_show = Menu(menubar)

menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')
menubar.add_cascade(menu=menu_preferences, label='Preferences')
menubar.add_cascade(menu=menu_show, label='Show')

menu_file.add_command(label='New File', command=newFile)
menu_file.add_command(label='Open File', command=openFile)
menu_file.add_command(label='Save File', command=save)
menu_file.add_command(label='Save As', command=lambda: save(saveAs=True))
menu_file.add_command(label='Wipe File', command=ClearData)

menu_edit.add_command(label='Check all for this month', command=lambda:check_all(False))
menu_edit.add_command(label='Uncheck all for this month', command=lambda:check_all(True))

showStreak = BooleanVar()
showStreak.set(True)
disableFutureDays = BooleanVar()
disableFutureDays.set(True)
menu_preferences.add_checkbutton(label='Show streaks', variable=showStreak, onvalue=True, offvalue=False, command=apply_streak)

menu_show.add_command(label='Show statistics', command=OpenStatsWindow)
menu_show.entryconfigure('Show statistics', state=DISABLED)


mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)

calendarFrame = ttk.Frame(root, borderwidth=5, relief="ridge")
calendarFrame.grid(column=0, row=1, padx=80, sticky =(N,S,E,W))
for column in range(11):
   calendarFrame.columnconfigure(column, weight=1)
for row in range(4):
   calendarFrame.rowconfigure(row, weight=1)


ttk.Label(mainframe, text="habtrack by surik").grid(column=5, row=1, sticky=(E))

currentDate = datetime.datetime.now()


month = currentDate.month
year = currentDate.year
tMonth = month #today month
tYear = year
tDay = currentDate.day

monthName = StringVar()
monthName.set(calendar.month_name[month])

monthVar = IntVar()
monthVar.set(month)

yearVar = IntVar()
yearVar.set(year)

menu_preferences.add_checkbutton(label='Disable Future Days', variable=disableFutureDays, onvalue=True, offvalue=False, command=lambda: draw_calendar(month, year))

initialize() #

ttk.Button(mainframe, text="<", command= lambda: change_month('-', monthName, monthVar, yearVar)).grid(column=2, row=2)
mSelect = ttk.Label(mainframe, textvariable=monthName)
mSelect.grid(column=3, row=2)
ttk.Button(mainframe, text=">", command= lambda: change_month('+', monthName, monthVar, yearVar)).grid(column=4, row=2)

ttk.Button(mainframe, text="<", command= lambda: change_year('-', yearVar, monthName, monthVar)).grid(column=5, row=2)
ttk.Label(mainframe, textvariable=yearVar).grid(column=6, row=2)
ttk.Button(mainframe, text=">", command= lambda: change_year('+', yearVar, monthName, monthVar)).grid(column=7, row=2)


#calendarframe define


draw_calendar(month, year)

bottomFrame = ttk.Frame(root)
bottomFrame.grid(column=0,row=2)




streakLabel = ttk.Label(bottomFrame,textvariable=streakText)
uncheckBtn = ttk.Button(bottomFrame, text="Uncheck All", command= lambda: check_all(True))
button = ttk.Button(bottomFrame, text="Save", command=save)
clearBtn = ttk.Button(mainframe, text="Clear All Data", command=SendMsgBox)
checkBtn = ttk.Button(bottomFrame, text="Check All", command= lambda: check_all(False))
streakLabel.grid(column=1,row=0)
uncheckBtn.grid(column=0, row=1)
clearBtn.grid(column=0,row=1)
button.grid(column=1, row=1)
checkBtn.grid(column=2, row=1)


root.columnconfigure(0, weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=3)
root.rowconfigure(2,weight=1)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)


root.protocol("WM_DELETE_WINDOW", AskForSave)
root.mainloop()


