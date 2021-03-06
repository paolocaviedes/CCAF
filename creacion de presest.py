#import RPi.GPIO as GPIO
import time
#from telnetlib import Telnet
import random

ids={1:'0000000',2:'1000000',3:'0100000',4:'0010000',5:'0001000',6:'0000100',7:'0000010',8:'0000001',9:'1100000',10:'0110000',11:'0011000',12:'0001100',13:'0000110',14:'0000011',15:'1110000',16:'0111000',17:'0011100',18:'0001110',19:'0000111',20:'1111000',21:'0111100',22:'0011110',23:'0001111',24:'1111100',25:'0111110',26:'0011111',27:'1111110',28:'0111111',29:'1111111'}

def invertir(entero):
	if entero==0:
		return 1
	else:
		return 0

def armarCadena():
    #para formar una cadena aleatoria
    cadena=""
    for i in range(7):
        elemento=str(random.randint(0,1))
        cadena += elemento
    return cadena

def contarZeros(cadena):
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

def contarZerosReverse(cadena):
	cadena=cadena[::-1]
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

def contarOnes(cadena):
	if contarZeros(cadena)==7:
		return 0
	return 7 - (contarZeros(cadena)+contarZerosReverse(cadena))

def transformarCadena(cadena):
	cadenaDefinitiva=''
	if contarZeros(cadena)==7:
		return '0000000'
	elif contarZeros(cadena)==0 and contarZerosReverse==0:
		return '1111111'
	else:
		cadenaDefinitiva='0'*contarZeros(cadena)+'1'*contarOnes(cadena)+'0'*contarZerosReverse(cadena)
		return cadenaDefinitiva

def determinarZoom(cadena,minZoom,maxZoom):
    factorDiff= (abs(maxZoom)-abs(minZoom))/6
    Zoom= minZoom+(factorDiff*(7-int(contarOnes(cadena))))
    return Zoom
#Determina la configuracion necesaria del pan para la camara, al ingresar la cadena ingresada
def determinarPan(cadena,minPan,maxPan):
    factorDiff=float(abs(maxPan)+abs(minPan))/6.0
    ajusteCentro= (float(contarOnes(cadena)))* factorDiff/2.0
    ajusteIzquierda=factorDiff*float(contarZeros(cadena))
    Pan= minPan+ajusteIzquierda+ajusteCentro
    return int(round(Pan,0))

def generarDiccionario(zoom, pan, tilt):
	dicc={}
	for id1,cadena in ids.items():
		zoom1=determinarZoom(cadena,zoom[0],zoom[1])
		pan1=determinarPan(cadena,pan[0],pan[1])
		dicc[id1]=(cadena,zoom1,pan1,tilt)
	return dicc

#crea las configuraciones que se insertan en el diccionario
def crearConfiguraciones(zoom,pan,tilt):
	arch=open('configuraciones.txt','w')
	dicc=generarDiccionario(zoom,pan,tilt)
	for id1 in sorted(ids):
		arch.write('Comando correspondiente al preset: '+str(id1)+', cadena: '+str(dicc[id1][0])+'\n')
		arch.write('xCommand Camera PositionSet CameraId:1 Zoom:'+str(dicc[id1][1])+' Pan:'+str(dicc[id1][2])+' Tilt: '+str(dicc[id1][3])+'\nxCommand Camera PositionSet CameraId:2 Zoom:6000 Pan:50 Tilt:-620\n\n')

#relaciona la cadena ingresada con el id del preset correspondiente
def determinarID(cadena):
	for id1,cadena1 in ids.items():
		if cadena1 == cadena:
			return id1

def mezclarCadena(cadena1,cadena2):
	if cadena1=="0000000" or cadena2 =="0000000":
		return "0000000"
	elif cadena1=="1111111" or cadena2 =="1111111":
		return "1111111"
	else:
		cz1=contarZeros(cadena1)
		cz2=contarZeros(cadena2)
		czr1=contarZerosReverse(cadena1)
		czr2=contarZerosReverse(cadena2)
		ones=7-(min(cz1,cz2)+min(czr1,czr2))
		cadenaDefinitiva= "0"*min(cz1,cz2)+"1"*ones+"0"*min(czr1,czr2)
		return cadenaDefinitiva


Sen_1=26
Sen_2=19
Sen_3=13
Sen_4=21
Sen_5=20
Sen_6=16
Sen_7=12

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(Sen_1,GPIO.IN)
#GPIO.setup(Sen_2,GPIO.IN)
#GPIO.setup(Sen_3,GPIO.IN)
#GPIO.setup(Sen_4,GPIO.IN)
#GPIO.setup(Sen_5,GPIO.IN)
#GPIO.setup(Sen_6,GPIO.IN)
#GPIO.setup(Sen_7,GPIO.IN)
#GPIO.setup(23,GPIO.OUT)

'''
#conexion
telnet = Telnet('192.168.29.111', 23)
telnet.read_until('login:')
telnet.write('admin\n')
telnet.read_until('Password:')
telnet.write('\n')
telnet.read_until('OK')
#wake up camara
telnet.write('xCommand Standby Deactivate\n')
telnet.read_until('OK')
time.sleep(1)

'''


#main
planoGeneral=(5900,-50,-600)

zoom=(5900,8000)
pan=(-720,630)
tilt=-450

crearConfiguraciones(zoom,pan,tilt)
diccionario=generarDiccionario(zoom,pan,tilt)

cadena_inicial="0000000"

cadena_auxiliar="0000000"

cadena_auxiliar2="0000000"

cadenaMezclada="0000000"

id_inicial=1
'''
while (True):


    GPIO.output(23,1)
    S1=GPIO.input(Sen_1)
    S2=GPIO.input(Sen_2)
    S3=GPIO.input(Sen_3)
    S4=GPIO.input(Sen_4)
    S5=GPIO.input(Sen_5)
    S6=GPIO.input(Sen_6)
    S7=GPIO.input(Sen_7)

	#caso1
    if cadena_inicial=="0000000" and cadena_auxiliar== "0000000":
        #print "caso 1"
        id1=determinarID("0000000")
        #print cadena_inicial
        #print 'el id del preset es', id1
        #print 'la configuracion es', diccionario[id1]

	#caso2
    elif cadena_inicial=="0000000" and cadena_auxiliar!= "0000000":
        #print "caso 2"
        id1=determinarID(transformarCadena(cadena_auxiliar))
        #print cadena_inicial
        #print 'el id del preset es', id1
        #print 'la configuracion es', diccionario[id1]
        #cadena_auxiliar=cadena_inicial

	#caso3
    elif cadena_inicial!="0000000" and cadena_auxiliar== "0000000":
        #print "caso 3"
        id1=determinarID(transformarCadena(cadena_inicial))
        #print cadena_inicial
        #print 'el id del preset es', id1
        #print 'la configuracion es', diccionario[id1]
        cadena_auxiliar=cadena_inicial

	#caso4
    elif cadena_inicial!="0000000" and cadena_auxiliar!= "0000000":
        #print "caso 4"
        cadenaMezclada=mezclarCadena(cadena_auxiliar,cadena_inicial)
        cadena_auxiliar=cadenaMezclada
        id1=determinarID(transformarCadena(cadena_auxiliar))
        #print cadena_inicial
        #print 'el id del preset es', id1
        #print 'la configuracion es', diccionario[id1]
        cadena_auxiliar=cadena_auxiliar2
        cadena_auxiliar2=cadena_inicial

    #Envio del comando a la sx80
    id_preset=id1
    if id_inicial!=id_preset:

        telnet.write('xCommand Camera Preset Activate PresetId:'+str(id1)+'\n')
        telnet.read_until('OK')

    id_inicial=id_preset

    time.sleep(0.3)
   # GPIO.output(23,0)
    time.sleep(0.2)

    #cadena_inicial=str(S1)+str(S2)+str(S3)+str(S4)+str(S5)+str(S6)+str(S7)

    #cadena_inicial=transformarCadena(armarCadena())
    #print "-------------------------------------------"
    #print cadena_inicial," cadena que sigue"
    #print cadena_auxiliar," cadena auxiliar"
    #print cadena_auxiliar2," cadena auxiliar 2"
    #print cadenaMezclada, " cadena mezclada"
    #print "-------------------------------------------"

    #a=str(raw_input())

'''