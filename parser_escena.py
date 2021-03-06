import os
from xml.dom import minidom
import pygame

def parse(fullname):
    xmldoc = minidom.parse(fullname)
    return xmldoc

def coordenadasPersonaje(tag, xmldoc):
    res =  xmldoc.getElementsByTagName(tag)
    if res == []:
        return None
    else:
        return (int(res[0].attributes['x'].value),int(res[0].attributes['y'].value))

def decorado(xmldoc):
    res =  xmldoc.getElementsByTagName("decorado")
    return res[0].attributes['name'].value

def texturas(xmldoc):
    res =  xmldoc.getElementsByTagName("texturas")
    return res[0].attributes['name'].value

def limites(xmldoc):
    res = xmldoc.getElementsByTagName("limitesMapa")
    return (int(res[0].attributes['x'].value),int(res[0].attributes['y'].value))

def escala_jefe(xmldoc):
    res = xmldoc.getElementsByTagName("Jefe")
    if res == []:
        return None
    else:
        return int(res[0].attributes['escala'].value)

def listaCoordenadasPlataforma(xmldoc):
    res = xmldoc.getElementsByTagName('plataforma')
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        z = int(res[i].attributes['z'].value)
        lista.append([pygame.Rect(x, y, z-5, 5),z,5])
    return lista

def listaCoordenadasSuelo(xmldoc):
    res = xmldoc.getElementsByTagName('suelo')
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        z = int(res[i].attributes['z'].value)
        lista.append([pygame.Rect(x, y, z-5, 5),z,5])
    return lista

def listaCoordenadasPared(xmldoc):
    res = xmldoc.getElementsByTagName('pared')
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        z = int(res[i].attributes['z'].value)
        lista.append([pygame.Rect(x, y, 5, z-y-5),5,z-y+5])
    return lista

def listaCoordenadasPersonaje(tag, xmldoc):
    res = xmldoc.getElementsByTagName(tag)
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        lista.append((x,y))
    return lista

def listaCoordenadasRelleno(xmldoc):
    res = xmldoc.getElementsByTagName('relleno')
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        z = int(res[i].attributes['z'].value)
        k = int(res[i].attributes['k'].value)
        lista.append([pygame.Rect(x, y, k, z),z,k])
    return lista

def coordenadasUpgrades(tag, xmldoc):
    res =  xmldoc.getElementsByTagName(tag)
    lista = []
    for i in range(0,len(res)):
        x = int(res[i].attributes['x'].value)
        y = int(res[i].attributes['y'].value)
        lista.append((x,y))
    return lista
