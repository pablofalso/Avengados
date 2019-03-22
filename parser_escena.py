import os
from xml.dom import minidom
import pygame

def parse(fullname):
    xmldoc = minidom.parse(fullname)
    return xmldoc


def devolver(tag,xmldoc):
    itemlist = xmldoc.getElementsByTagName(tag)
    return itemlist

def coordenadasPersonaje(tag,xmldoc):
    res = devolver(tag,xmldoc)
    return (int(res[0].attributes['name'].value),int(res[1].attributes['name'].value))

def coordenadasPlataforma(tag,xmldoc):
    res = devolver(tag,xmldoc)
    x = int(res[0].attributes['name'].value)
    y = int(res[1].attributes['name'].value)
    z = int(res[2].attributes['name'].value)
    return (pygame.Rect(x, y, z-x-5, 5),z-x,5)

def coordenadasPared(tag,xmldoc):
    res = devolver(tag,xmldoc)
    x = int(res[0].attributes['name'].value)
    y = int(res[1].attributes['name'].value)
    z = int(res[3].attributes['name'].value)
    return (pygame.Rect(x, y, 5, z-y-10),5,z-y+5)
