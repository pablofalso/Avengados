import os
from xml.dom import minidom

def parse(fullname):
    xmldoc = minidom.parse(fullname)
    return xmldoc


def devolver(tag,xmldoc):
    itemlist = xmldoc.getElementsByTagName(tag)
    return itemlist

def coordenadasPersonaje(tag,xmldoc):
    res = devolver(tag,xmldoc)
    return (int(res[0].attributes['name'].value),int(res[1].attributes['name'].value))
