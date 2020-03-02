#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lizz Morales
#
# Created:     28/02/2020
# Copyright:   (c) Lizz Morales 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import random
import threading

N = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    semaforo = threading.Lock()
    estado = []
    tenedores = []
    count=0

    def _init_(self):
        super()._init_()
        self.id=filosofo.count #DESIGNA EL ID AL FILOSOFO
        filosofo.count+=1 #AGREGA UNO A LA CANT DE FILOSOFOS
        filosofo.estado.append('PENSANDO') #EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        filosofo.tenedores.append(threading.Semaphore(0)) #AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        print("FILOSOFO {0} - PENSANDO".format(self.id))

    def _del_(self):
        print("FILOSOFO {0} - Se para de la mesa".format(self.id))

    def pensar(self):
        time.sleep(random.randint(0,5))

    def derecha(self,i):
        return (i-1)%N #BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N #BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()

    def tomar(self):
        filosofo.semaforo.acquire()
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id)
        filosofo.semaforo.release() #SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.tenedores[self.id].acquire()
    def soltar(self):
        filosofo.semaforo.acquire()
        filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release()

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(self.id))
        time.sleep(2) #TIEMPO ARBITRARIO PARA COMER
        print("FILOSOFO {} TERMINO DE COMER".format(self.id))

    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar()
            self.tomar()
            self.comer()
            self.soltar()

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) #AGREGA UN FILOSOFO A LA LISTA

    for f in lista:
        f.start()
    for f in lista:
        f.join()

    if _name=="main_":
        main()