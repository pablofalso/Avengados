import os
from xml.dom import minidom
import pygame

def parse(fullname):
    xmldoc = minidom.parse(fullname)
    return xmldoc

def coordenadasPersonaje(tag, xmldoc):
    res =  xmldoc.getElementsByTagName(tag)
    return (int(res[0].attributes['x'].value),int(res[0].attributes['y'].value))

def listaCoordenadasPlataforma(xmldoc):
    res = xmldoc.getElementsByTagName('plataforma')
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
