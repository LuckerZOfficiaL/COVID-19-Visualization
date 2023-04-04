import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from tkcalendar import*


root = Tk() # La finestra GUI
root.title('Covid-19 Stats')#Titolo della finestra
root.geometry('500x200')#Le dimensioni della finestra



#Prende i dati dall'url in formato csv
cov = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
cov['date'] = pd.to_datetime(cov['date'], dayfirst=True)#Concertire le date da stringa in formato date
nations = cov['location'].unique()#Lista delle nazioni senza ripetizioni


#Funzione per la scelta del colore
def color():
    global color
    color = colorchooser.askcolor()[1]
    plot_btn = Button(root,text='Show Graph',command=show)
    plot_btn.grid(row=5,column=2,columnspan=1,padx=2,pady=10,ipadx=70)
   
#Funzione per aggiornare la data d'inizio selezionata
def aggiorna_data_inizio():
        global inizio_lbl
        inizio_lbl = Label(root,text=cal1.get_date())
        inizio_lbl.grid(row=2,column=2)
        fine_btn = Button(root,text='To',command=fine)
        fine_btn.grid(row=3,column=1,ipadx=7.5)
        top.destroy()

#Funzione che fa apparire il calendario   
def inizio():
    global top
    top = Toplevel()
    top.title('Select initial date')
    
    global cal1 
    cal1 = Calendar(top,selectmode='day',year=2020,month=2, day=30)
    cal1.pack(pady=20)

    
    ok_btn = Button(top,text='OK',command=aggiorna_data_inizio).pack()
    
#Funzione per aggiornare la data di fine selezionata
def aggiorna_data_fine():
    
        
        if cal2.get_date()<=cal1.get_date():
            global response            
            response = messagebox.showwarning('Warning','The end date must be greater than the initial date!')
            Label(top,text=response).pack()
            
            
            
        else:
            global fine_lbl
            fine_lbl = Label(root,text=cal2.get_date())
            fine_lbl.grid(row=3,column=2)
            color_btn = Button(root,text='Pick color',command=color)
            color_btn.grid(row=5,column=1,columnspan=1,padx=2,pady=10,ipadx=10)
            top2.destroy()


#Funzione che fa apparire il calendario       
def fine():
    global top2
    top2 = Toplevel()
    top2.title('Select end date')
    
    global cal2 
    cal2 = Calendar(top2,selectmode='day',year=2020,month=5, day = 29)
    cal2.pack(pady=20)

    ok_btn = Button(top2,text='OK',command=aggiorna_data_fine).pack()

def restart():
    nation_box.delete(0,'end')
    inizio_lbl.destroy()
    fine_lbl.destroy()
    #fine_btn['state']=DISABLED
    #plot_btn['state']=DISABLED
    #color_btn['state']=DISABLED
    fine_btn = Button(root,text='To',command=fine,state=DISABLED)
    fine_btn.grid(row=3,column=1,ipadx=7.5)
    color_btn = Button(root,text='Pick color',command=color,state=DISABLED)
    color_btn.grid(row=5,column=1,columnspan=1,padx=2,pady=10,ipadx=10)
    plot_btn = Button(root,text='Show Graph',command=show,state=DISABLED)
    plot_btn.grid(row=5,column=2,columnspan=1,padx=2,pady=10,ipadx=70)

    

      
    
#Funzione che mostra il grafico
def show():
    global data_inizio
    global data_fine
    global mode
    global country
    global mask
    global tab
    global x
    global y
    
    data_inizio = cal1.get_date()
    data_fine = cal2.get_date()
    mode = clicked.get()
    country = nation_box.get()
    
    if country in nations :
                if mode == 'Total cases':  
                    mask = (cov['date'] >= data_inizio) & (cov['date'] <= data_fine) & (cov['location']== country)
                    tab = cov.loc[mask]

                    x = tab['date']
                    y = tab['total_cases']

                    plt.plot(x,y,color,linewidth = scale.get())
                    plt.xlabel('Time')
                    plt.ylabel('Cases')
                    plt.title(mode + ' in ' + country)
                    plt.show()

                if mode == 'Total deaths':
                    mask = (cov['date'] >= data_inizio) & (cov['date'] <= data_fine) & (cov['location']== country)
                    tab = cov.loc[mask]
                    
                    x = tab['date']
                    y = tab['total_deaths']
               
                    fig = plt.figure(figsize=(12,4))
                    plt.plot(x,y,color,linewidth = scale.get())
                    plt.xlabel('Time')
                    plt.ylabel('Deaths')
                    plt.title(mode + ' in ' + country)
                    plt.show()
   
                if mode == 'Increasing cases':
                    fig = plt.figure(figsize=(12,4))
                    mask = (cov['date'] >= data_inizio) & (cov['date'] <= data_fine) & (cov['location']== country)
                    tab = cov.loc[mask]

                    x = tab['date']
                    y = tab['new_cases']

                    plt.plot(x,y,color,linewidth = scale.get())
                    plt.xlabel('Time')
                    plt.ylabel('New cases')
                    plt.title(mode + ' in ' + country)
                    plt.show()

                if mode == 'Increasing deaths':
                    mask = (cov['date'] >=data_inizio) & (cov['date'] <= data_fine) & (cov['location']== country)
                    tab = cov.loc[mask]

                    x = tab['date']
                    y = tab['new_deaths']

                    fig = plt.figure(figsize=(12,4))
                    plt.plot(x,y,color,linewidth = scale.get())
                    plt.xlabel('Time')
                    plt.ylabel('New deaths')
                    plt.title(mode + ' in ' + country)
                    plt.show()

                if mode == 'Cases/Deaths':
                    mask = (cov['location']== country)
                    tab = cov.loc[mask]

                    sns.jointplot(x='total_cases',y='total_deaths',data=tab,color=color)

                    plt.xlabel('Time')
                    plt.ylabel('New deaths')
                    plt.title(mode + ' in ' + country)
                    plt.show()
                                                 
                if mode == 'Cases vs Deaths':
                        mask = (cov['location']== country)
                        tab = cov.loc[mask]

                        x = tab['date']
                        y = tab['total_cases']
                        y1 = tab['total_deaths']
                    
                        plt.plot(x,y,color,linewidth = scale.get())
                        plt.plot(x,y1,'red',linewidth = scale.get())
                        plt.legend(['Cases', 'Deaths'])
                                         
                        plt.xlabel('Time')
                        plt.ylabel('Number')
                        plt.title(mode + ' in ' + country)
                        plt.show()
       
    else: 
        global response2
        response2 = messagebox.showwarning('Attenzione','La nazione inserita è errata!')
       

#Elementi grafici 
nation_lbl = Label(root,text='Location')
nation_lbl.grid(row=1,column=0)
nation_box = Entry(root,width=50,font=('Helvetica',10))
nation_box.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
data_lbl = Label(root,text='Select dates')
data_lbl.grid(row=2,column=0)
inizio_btn = Button(root,text='From',command=inizio)
inizio_btn.grid(row=2,column=1)
inizio_lbl = Label(root,text='')
inizio_lbl.grid(row=2,column=2)
fine_btn = Button(root,text='To',command=fine,state=DISABLED)
fine_btn.grid(row=3,column=1,ipadx=7.5)
fine_lbl = Label(root,text='')
fine_lbl.grid(row=3,column=2)

clicked = StringVar()
clicked.set('Total cases')

scegli_lbl = Label(root,text='Choose an option')
scegli_lbl.grid(row=4,column=0)
drop = OptionMenu(root,clicked,'Total cases','Total deaths','Increasing cases','Increasing deaths','Cases/Deaths','Cases vs Deaths')
drop.grid(row=4,column =1,columnspan=3,padx=10,pady=10,ipadx=50)

plot_btn = Button(root,text='Show Graph',command=show,state=DISABLED)
plot_btn.grid(row=5,column=2,columnspan=1,padx=2,pady=10,ipadx=70)

color_btn = Button(root,text='Pick color',command=color,state=DISABLED)
color_btn.grid(row=5,column=1,columnspan=1,padx=2,pady=10,ipadx=10)

scale = Scale(root,from_=1, to=15, orient=HORIZONTAL)
scale.grid(row=5, column=0)


my_menu = Menu(root)
root.config(menu=my_menu)

#Creare un oggetto del menù
action_menu = Menu(my_menu)
my_menu.add_cascade(label='Action',menu=action_menu)
action_menu.add_command(label='Restart',comman=restart)
action_menu.add_command(label='Exit',comman=root.destroy)

#Esecuzione di una GUI
root.mainloop()