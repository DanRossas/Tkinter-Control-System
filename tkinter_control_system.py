''' 
*******************************************************************************
 @archivo    tkinter_control_system.py
 @brief      Control system for a Goniophotometer with two motors and sends 
             the serial data to an Arduino.
 
 @autor  Daniel Rosas
 @fecha  11/24/2021
 *******************************************************************************
 '''
from tkinter import * 
from tkinter import ttk
#from typing_extensions import ParamSpecArgs 
import serial
import time
import serial.tools.list_ports

root = Tk()
root.geometry('700x680') # Geometría de la pantalla del programa
root.title("Control Goniometro") #Nombre de la ventana

# Comunicación Serial - Frame
comSerialFrame = LabelFrame(root, text="Comunicacion Serial", padx=5, pady=5)
comSerialFrame.grid(row=0, column=0, padx=5, pady=5)

# Parámetros de la Medición - Frame 
parMedFrame = LabelFrame(root, text="Parámetros de la Medición", padx=5, pady=5)
parMedFrame.grid(row=1, column=0, padx=5, pady=5)

# Proceso de Medición - Frame
procMedFrame = LabelFrame(root, text="Proceso de Medicion", padx=5, pady=5)
procMedFrame.grid(row=0, column=1, padx=5, pady=5)

# Cerrar Comunicación y Detener Programa - Frame
cerrarComFrame = LabelFrame(root)
cerrarComFrame.grid(row=2, column=0, padx=5, pady=5)

def connectCheck(args):
    if "-" in clickedCom.get() or "-" in clickedBd.get():
        connectButton["state"] = "disable"
    else: 
        connectButton["state"] = "active"        

def baudSelect(): 
    global clickedBd
    global dropBd
    clickedBd = StringVar()
    bds = ["-", 
        "300", 
        "600", 
        "1200", 
        "2400", 
        "4800", 
        "9600", 
        "14400", 
        "19200", 
        "28800", 
        "31250", 
        "38400", 
        "57600", 
        "115200"]
    clickedBd.set(bds[0])
    dropBd = OptionMenu(comSerialFrame, clickedBd, *bds, command = connectCheck)
    dropBd.config(width = 20)
    dropBd.grid(column = 2, row = 3, padx = 10)

def updateComms():
    global clickedCom 
    global dropCOM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        dropCOM.destroy()
    except:
        pass
    clickedCom = StringVar()
    clickedCom.set(coms[0])
    dropCOM = OptionMenu(comSerialFrame, clickedCom, *coms, command = connectCheck)
    dropCOM.config(width = 20)
    dropCOM.grid(column = 2, row = 2, padx = 10)
    connectCheck(0)

def connection():
    global ser
    if connectButton["text"] in "Desconectar":
        connectButton["text"] = "Conectar"
        refreshButton["state"] = "active"
        dropBd["state"] = "active"
        dropCOM["state"] = "active"
        try: 
            ser = 0 
        except: 
            pass
    else:  
        connectButton["text"] = "Desconectar"
        refreshButton["state"] = "disable"
        dropBd["state"] = "disable"
        dropCOM["state"] = "disable"
        port = clickedCom.get()
        baud = clickedBd.get()
        try: 
            ser = serial.Serial(port, baud)
        except: 
            pass

def mostrarEntryAzi(valor): 
    valorActual = int(posicionAziEntry.get())
    valorActual = valorActual + valor
    if valorActual < 0:
        valorActual = 360 + valorActual
    if valorActual >= 360:
        valorActual = valorActual - 360
    posicionAziEntry.delete(0, END)
    posicionAziEntry.insert(0, valorActual)


def mostrarEntryEle(valor):
    valorActual = int(posicionEleEntry.get())
    valorActual = valorActual + valor
    if valorActual < 0:
        valorActual = 360 + valorActual
    if valorActual >= 360:
        valorActual = valorActual - 360
    posicionEleEntry.delete(0, END)
    posicionEleEntry.insert(0, valorActual)

def resetAziEntry():
    posicionAziEntry.delete(0, END)
    posicionAziEntry.insert(0, 0)

def resetEleEntry():
    posicionEleEntry.delete(0, END)
    posicionEleEntry.insert(0, 0)

''' función para enviar string de movimiento manual en sentido horario 
    en el eje azimutal: '''
def horarioAzimutal():
    global moverEjesCad
    if (gradAvanzar1.get() == "1 °"): 
        moverEjesCad = 'M,A'
        valorSumar = 1
    if (gradAvanzar1.get() == "2 °"):
        moverEjesCad = 'M,B'
        valorSumar = 2
    if (gradAvanzar1.get() == "5 °"):
        moverEjesCad = 'M,C'
        valorSumar = 5
    if (gradAvanzar1.get() == "10 °"):
        moverEjesCad = 'M,D'
        valorSumar = 10
    if (gradAvanzar1.get() == "15 °"):
        moverEjesCad = 'M,E'
        valorSumar = 15
    if (gradAvanzar1.get() == "20 °"):
        moverEjesCad = 'M,F'
        valorSumar = 20
    if (gradAvanzar1.get() == "30 °"):
        moverEjesCad = 'M,G'
        valorSumar = 30
    if (gradAvanzar1.get() == "45 °"):
        moverEjesCad = 'M,H'
        valorSumar = 45
    if (gradAvanzar1.get() == "90 °"):
        moverEjesCad = 'M,I'
        valorSumar = 90
    ser.write(moverEjesCad.encode('ascii'))
    mostrarEntryAzi(valorSumar)

''' función para enviar string de movimiento manual en sentido antihorario 
    en el eje azimutal: '''
def antihorarioAzimutal():
    global moverEjesCad
    if (gradAvanzar1.get() == "1 °"):
        moverEjesCad = 'M,a'
        valorSumar = -1
    if (gradAvanzar1.get() == "2 °"):
        moverEjesCad = 'M,b'
        valorSumar = -2
    if (gradAvanzar1.get() == "5 °"):
        moverEjesCad = 'M,c'
        valorSumar = -5
    if (gradAvanzar1.get() == "10 °"):
        moverEjesCad = 'M,d'
        valorSumar = -10
    if (gradAvanzar1.get() == "15 °"):
        moverEjesCad = 'M,e'
        valorSumar = -15
    if (gradAvanzar1.get() == "20 °"):
        moverEjesCad = 'M,f'
        valorSumar = -20
    if (gradAvanzar1.get() == "30 °"):
        moverEjesCad = 'M,g'
        valorSumar = -30
    if (gradAvanzar1.get() == "45 °"):
        moverEjesCad = 'M,h'
        valorSumar = -45
    if (gradAvanzar1.get() == "90 °"):
        moverEjesCad = 'M,i'
        valorSumar = -90
    ser.write(moverEjesCad.encode('ascii')) 
    mostrarEntryAzi(valorSumar)
              
''' función para enviar string de movimiento manual en sentido horario 
    en el eje de elevación: '''
def horarioElevacion():
    global moverEjesCad
    if (gradAvanzar2.get() == "1 °"):
        moverEjesCad = 'M,R'
        valorSumar = 1
    if (gradAvanzar2.get() == "2 °"):
        moverEjesCad = 'M,S'
        valorSumar = 2
    if (gradAvanzar2.get() == "5 °"):
        moverEjesCad = 'M,T'
        valorSumar = 5
    if (gradAvanzar2.get() == "10 °"):
        moverEjesCad = 'M,U'
        valorSumar = 10
    if (gradAvanzar2.get() == "15 °"):
        moverEjesCad = 'M,V'
        valorSumar = 15
    if (gradAvanzar2.get() == "20 °"):
        moverEjesCad = 'M,W'
        valorSumar = 20
    if (gradAvanzar2.get() == "30 °"):
        moverEjesCad = 'M,X'
        valorSumar = 30
    if (gradAvanzar2.get() == "45 °"):
        moverEjesCad = 'M,Y'
        valorSumar = 45
    if (gradAvanzar2.get() == "90 °"):
        moverEjesCad = 'M,Z'
        valorSumar = 90
    ser.write(moverEjesCad.encode('ascii'))
    mostrarEntryEle(valorSumar)

''' función para enviar string de movimiento manual en sentido antihorario 
    en el eje de elevación: '''
def antihorarioElevacion():
    global moverEjesCad
    if (gradAvanzar2.get() == "1 °"):
        moverEjesCad = 'M,r'
        valorSumar = -1
    if (gradAvanzar2.get() == "2 °"):
        moverEjesCad = 'M,s'
        valorSumar = -2
    if (gradAvanzar2.get() == "5 °"):
        moverEjesCad = 'M,t'
        valorSumar = -5
    if (gradAvanzar2.get() == "10 °"):
        moverEjesCad = 'M,u'
        valorSumar = -10
    if (gradAvanzar2.get() == "15 °"):
        moverEjesCad = 'M,v'
        valorSumar = -15
    if (gradAvanzar2.get() == "20 °"):
        moverEjesCad = 'M,w'
        valorSumar = -20
    if (gradAvanzar2.get() == "30 °"):
        moverEjesCad = 'M,x'
        valorSumar = -30
    if (gradAvanzar2.get() == "45 °"):
        moverEjesCad = 'M,y'
        valorSumar = -45
    if (gradAvanzar2.get() == "90 °"):
        moverEjesCad = 'M,z'
        valorSumar = -90
    ser.write(moverEjesCad.encode('ascii'))
    mostrarEntryEle(valorSumar)

# función para agregar a la string del modo automático el intervalo de espera
def intervaloEsperar():
    global moverEjesCad
    if (inter3.get() == "1 s"):
        moverEjesCad = moverEjesCad + ',1' 
    if (inter3.get() == "2 s"):
        moverEjesCad = moverEjesCad + ',2'
    if (inter3.get() == "3 s"):
        moverEjesCad = moverEjesCad + ',3'
    if (inter3.get() == "4 s"):
        moverEjesCad = moverEjesCad + ',4'
    if (inter3.get() == "5 s"):
        moverEjesCad = moverEjesCad + ',5'
    if (inter3.get() == "6 s"):
        moverEjesCad = moverEjesCad + ',6'
    if (inter3.get() == "7 s"):
        moverEjesCad = moverEjesCad + ',7'
    if (inter3.get() == "8 s"):
        moverEjesCad = moverEjesCad + ',8'
    if (inter3.get() == "9 s"):
        moverEjesCad = moverEjesCad + ',9'

# función para agregar a la string del modo automático el intervalo del eje de elevación
def moverElevacion():
    global moverEjesCad
    if (inter2.get() == "1 °"):
        moverEjesCad = moverEjesCad + ',r'
    if (inter2.get() == "2 °"):
        moverEjesCad = moverEjesCad + ',s'
    if (inter2.get() == "5 °"):
        moverEjesCad = moverEjesCad + ',t'
    if (inter2.get() == "10 °"):
        moverEjesCad = moverEjesCad + ',u'
    if (inter2.get() == "15 °"):
        moverEjesCad = moverEjesCad + ',v'
    if (inter2.get() == "20 °"):
        moverEjesCad = moverEjesCad + ',w'
    if (inter2.get() == "30 °"):
        moverEjesCad = moverEjesCad + ',x'
    if (inter2.get() == "45 °"):
        moverEjesCad = moverEjesCad + ',y'
    if (inter2.get() == "90 °"):
        moverEjesCad = moverEjesCad + ',z'
    intervaloEsperar()

# función para agregar a la string del modo automático el intervalo del eje azimutal
def moverAzimutal():
    global moverEjesCad 
    if (inter1.get() == "1 °"):
        moverEjesCad = moverEjesCad + ',a' 
    if (inter1.get() == "2 °"):
        moverEjesCad = moverEjesCad + ',b'
    if (inter1.get() == "5 °"):
        moverEjesCad = moverEjesCad + ',c' 
    if (inter1.get() == "10 °"):
        moverEjesCad = moverEjesCad + ',d' 
    if (inter1.get() == "15 °"):
        moverEjesCad = moverEjesCad + ',e' 
    if (inter1.get() == "20 °"):
        moverEjesCad = moverEjesCad + ',f' 
    if (inter1.get() == "30 °"):
        moverEjesCad = moverEjesCad + ',g' 
    if (inter1.get() == "45 °"):
        moverEjesCad = moverEjesCad + ',h' 
    if (inter1.get() == "90 °"): 
        moverEjesCad = moverEjesCad + ',i'
    moverElevacion() 

# función para enviar la string de movimiento automático al puerto serial 
def moverEjes():
    global moverEjesCad 
    moverEjesCad = 'A'
    moverAzimutal()
    ser.write(moverEjesCad.encode('ascii'))

# función para enviar dato para pausar o reanudar movimiento
def reanudarPausarMov():
    ser.write(bytes('K', 'UTF-8')) 

# función para encender laser
def laserTurn():
    laserString = 'L'
    ser.write(laserString.encode('ascii'))

# función para cancelar movimiento
def cancelarMov():
    ser.write(bytes('N', 'UTF-8'))

def popupOriginReminder():
   top= Toplevel(root)
   top.geometry("350x100")
   top.title("Colocar en Posición de Descanso")
   recordatorioLabel = Label(top, text= "Por favor, antes de terminar de medir, coloca el \n Goniómetro en su posición de descanso.")
   listoButton = Button(top, text="LISTO", command=root.destroy)
   regresarButton = Button(top, text="REGRESAR", command=top.destroy)

   recordatorioLabel.grid(row=0, column=0, columnspan=2)
   listoButton.grid(row=1, column=0)
   regresarButton.grid(row=1, column=1)
      
# inicio del programa
print("Reset Arduino")
time.sleep(2)

# Comunicación Serial - Buttons
portLabel = Label(comSerialFrame, text = "Puertos Disponibles:")
portLabel.grid(column = 1, row = 2, padx = 10, pady = 5)

portBd = Label(comSerialFrame, text = "Baude Rate:")
portBd.grid(column = 1, row = 3, padx = 10, pady = 5)

refreshButton = Button(comSerialFrame, text = "Refresh", height = 2, width = 10, command = updateComms)
refreshButton.grid(column = 3, row = 2)

connectButton = Button(comSerialFrame, text = "Conectar", height = 2, width = 10, state = "disabled", command = connection)
connectButton.grid(column = 3, row = 4)
baudSelect()
updateComms()

# Proceso de Medición - Buttons
# Reanudar - Button
pausarButton = Button(procMedFrame, text="Reanudar \n Pausar", command=reanudarPausarMov)
pausarButton.grid(row=0, column=0)

# Laser - Button
laserButton = Button(procMedFrame, text = "Encender/Apagar \n Laser", command=laserTurn)
laserButton.grid(row=0, column=1)

# Cancelar - Button
cancelarButton = Button(procMedFrame, text="Cancelar \n Movimiento", command=cancelarMov)
cancelarButton.grid(row=0,column=2)

# Tabs para Parametros de la Medición
parMedNotebook = ttk.Notebook(parMedFrame)
parMedNotebook.pack(pady=15)

modAuto = Frame(parMedNotebook)
modManual = Frame(parMedNotebook)

modAuto.pack(fill="both", expand=1)
modManual.pack(fill="both", expand=1)

parMedNotebook.add(modAuto, text="Modo Automático")
parMedNotebook.add(modManual, text="Modo Manual")

# Modo Automatico - Tab - Parámetros de la Medición
interOptions = [
    "1 °", 
    "2 °",
    "5 °", 
    "10 °", 
    "15 °", 
    "20 °", 
    "30 °", 
    "45 °", 
    "90 °",  
]

interTempOptions = [
    "1 s",
    "2 s",
    "3 s",
    "4 s",
    "5 s",
    "6 s",
    "7 s",
    "8 s",
    "9 s",
]

# Eje Azimutal - options
ejeAziLabel = Label(modAuto, text="Eje Azimutal")
ejeAziLabel.grid(row=0, column=0)
inter1Label = Label(modAuto, text="Intervalo 1")
inter1Label.grid(row=1, column=0)

inter1 = StringVar()
inter1.set(interOptions[0])

interMenu1 = OptionMenu(modAuto, inter1, *interOptions)
interMenu1.grid(row=2, column=0)

# Eje de Elevación - options
ejeEleLabel = Label(modAuto, text="Eje de Elevación")
ejeEleLabel.grid(row=3, column=0)
inter2Label = Label(modAuto, text="Intervalo 2")
inter2Label.grid(row=4, column=0)

inter2 = StringVar()
inter2.set(interOptions[0])

interMenu2 = OptionMenu(modAuto, inter2, *interOptions)
interMenu2.grid(row=5, column=0)

# Tiempo de Muestreo
tiempoMuestreoLabel = Label(modAuto, text="Tiempo de Muestreo")
tiempoMuestreoLabel.grid(row=6, column=0)
inter3Label = Label(modAuto, text="Intervalo 3")
inter3Label.grid(row=7, column=0)

inter3 = StringVar()
inter3.set(interTempOptions[0])

interMenu3 = OptionMenu(modAuto, inter3, *interTempOptions)
interMenu3.grid(row=8, column=0)

# Definir Parametros - Button 
defParButton = Button(modAuto, text="Definir Parametros", command=moverEjes)
defParButton.grid(row=9,column=0)

# Modo Manual - Tab - Parametros de la medición

    # Eje Azimutal - Button - modo manual
ejeAziLabel = Label(modManual, text="Eje Azimutal")
ejeAziLabel.grid(row=0, column=0)

atrasButton1 = Button(modManual, text= "Horario", command=horarioAzimutal)
atrasButton1.grid(row=1, column=0)

adelanteButton1 = Button(modManual, text= "Antihorario", command=antihorarioAzimutal)
adelanteButton1.grid(row=2, column=0, pady=(0, 20))

gradAvanzarLabel1 = Label(modManual, text="Grados a \n Avanzar")
gradAvanzarLabel1.grid(row=1, column=1, padx=20)

gradAvanzar1 = StringVar()
gradAvanzar1.set(interOptions[0])

gradAvanzarMenu1 = OptionMenu(modManual, gradAvanzar1, *interOptions)
gradAvanzarMenu1.grid(row=2, column=1, padx=20)

# Eje Elevación - Button - modo manual
ejeEleLabel = Label(modManual, text="Eje de Elevación")
ejeEleLabel.grid(row=3, column=0)

atrasButton2 = Button(modManual, text= "Horario", command=horarioElevacion)
atrasButton2.grid(row=4, column=0)

adelanteButton2 = Button(modManual, text= "Antihorario",  command=antihorarioElevacion)
adelanteButton2.grid(row=5, column=0, pady=(0, 20))

gradAvanzarLabel2 = Label(modManual, text="Grados a \n Avanzar")
gradAvanzarLabel2.grid(row=4, column=1, padx=20)

gradAvanzar2 = StringVar()
gradAvanzar2.set(interOptions[0])

gradAvanzarMenu2 = OptionMenu(modManual, gradAvanzar2, *interOptions)
gradAvanzarMenu2.grid(row=5, column=1, padx=20)

# Posicion Azimutal y Elevación - Entries
posicionAziEleFrame = Frame(parMedFrame)
posicionAziEleFrame.pack()

posicionAziLabel = Label(posicionAziEleFrame, text="Posición \n Azimutal")
posicionAziLabel.grid(row=0, column=0)
posicionAziEntry = Entry(posicionAziEleFrame, width=10)
posicionAziEntry.grid(row=1, column=0, padx=8)
posicionAziEntry.insert(0, 0)

# Resetear valores en el Entry del eje de elevación- Button 
resetAziButton = Button(posicionAziEleFrame, text="Resetear a 0°", command = resetAziEntry)
resetAziButton.grid(row=2, column=0)

posicionEleLabel = Label(posicionAziEleFrame, text="Posición \n Elevación")
posicionEleLabel.grid(row=0, column=1)
posicionEleEntry = Entry(posicionAziEleFrame, width=10)
posicionEleEntry.grid(row=1, column=1, padx=8)
posicionEleEntry.insert(0, 0)

# Resetear valores en el Entry del eje de elevación- Button 
resetEleButton = Button(posicionAziEleFrame, text="Resetear a 0°", command = resetEleEntry)
resetEleButton.grid(row=2, column=1)

# Cerrar Comunicación y Detener Programa - Button
cerrarComLabel = Label(cerrarComFrame, text="Cerrar Comunicación \n y Detener Programa")
cerrarComButton = Button(cerrarComFrame, text="CERRAR", command=popupOriginReminder)

cerrarComLabel.grid(row=0, column=0)
cerrarComButton.grid(row=1, column=0, pady=10)

root.mainloop()