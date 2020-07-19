#!/usr/bin/python
# -*- coding: utf-8 -*-

from ftplib import FTP
from datetime import datetime
import os.path, time
from os  import remove
import requests
import sys

# Datos Conexion Camara
servidor="192.168.1.X"
user="root"
passwd="XXXXXX"
# Credenciales Telegram
id = "XXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"
# Fichero registro de videos.
fname="listado_videos_mp4.txt"

# Una vez enviado el video se elimina del servidor.
# Si no se desea eliminar los videos del servidor comentar esta funcion.
def delete_videos_server(listado):
    for item in listado:
        remove(item)

def enviar_mensaje(listado):    
    # Mensaje de texto plano
    #url = "https://api.telegram.org/bot" + token + "/sendMessage" 
    #params = {
    #    'chat_id': id,
    #    'text' : "Vamos a enviar un mensaje"
    #    }
    #requests.post(url, params=params)
    url = "https://api.telegram.org/bot" + token + "/sendVideoNote"    
    for video in listado:        
        data = {
            'chat_id': id,
            'text': video,
            }
        files = {
            'video_note': (video,open(str(video), 'rb'))
            }
        try:
            requests.post(url, files=files, data=data)
        except Exception, e:
            print "[-] Error al intentar enviar video mediante API telegram "+str(e)
        

def almacenar_listado_videos(listado_Videos):
    with open(fname, 'w') as f: # guardamos listado en archivo.
            for i in listado_videos:
                f.write(i+'\n')
            f.close()

def comparacion_listados(listado_new, listado_old):
    listado_comparativa = []        
    final=set(listado_new) & set(listado_old)    
    if len(final)>0:
        print "Existen {} videos identicos".format(len(final))
        if len(final) != len(listado_new):
            remove(fname) # eliminamos fichero de registro de videos
            almacenar_listado_videos(listado_new) # creamos de nuevo fichero con el listado nuevo
            for l1 in listado_new: # Comparamos los listados para obtener los nuevos videos.
                if l1 not in listado_old:
                    listado_comparativa.append(l1)            
            return listado_comparativa
        else:
            print "No hemos tenido variacion alguna." # no realizamos ninguna accion ya que no se ha generado ningun video nuevo.
    else:
        print "El listado es totalmente distinto"
        remove(fname) # eliminamos fichero
        almacenar_listado_videos(listado_new) # creamos de nuevo fichero con el listado nuevo        
        return listado_new
    return False

def recuperar_listado(fname):
    listado_video=[]
    file = open(fname, "r")
    print "[+] Contenido del fichero: "+fname
    for linea in file:
        listado_video.append(linea[:-1]) # recuperamos el listado de videos anterior.   
    file.close()    
    return listado_video

# Inicio
try:
    conexion = FTP(servidor)
    conexion.login(user,passwd)
    print "[+] Conexion establecida a camara 1"
    conexion.cwd("/tmp/sd/record/")
    archivos = conexion.dir()

    listado_archivos = conexion.nlst() # listamos los directorios existentes en FTP
    nombre_directorio=''
    listado_videos=[]
    listado_video_old=[]
    for archivo in reversed(listado_archivos): # Ordenacion inversa.
        if archivo.find('tmp.mp4.tmp')>=0: # Puede que en ese momento nos encontremos con un video tmp que se esta almacenando.
            continue
        else:        
            nombre_directorio=archivo
            break
    try:    
        conexion.cwd("/tmp/sd/record/"+str(nombre_directorio)+"/") # Accedemos al ultimo directorio
        print "[+] Acceso al directorio: "+str(nombre_directorio)
        listado_videos = conexion.nlst()    
        if os.path.isfile(fname):
            listado_video_old = recuperar_listado(fname)
            listado_a_descargar = comparacion_listados(listado_videos, listado_video_old)
            if listado_a_descargar: 
                for filename in listado_a_descargar: # descarga de ficheros del FTP a server
                    with open(filename, 'wb') as f:
                        conexion.retrbinary('RETR ' + filename, f.write)            
                enviar_mensaje(listado_a_descargar) # Enviar notificacion con los videos nuevos.
                delete_videos_server(listado_a_descargar) # elimina videos del server
        else:
            print "[+] Creamos fichero y almacenamos el listado de .mp4"        
            almacenar_listado_videos(listado_videos) # creamos de nuevo fichero con el listado nuevo        
            for filename in listado_videos: # descarga de ficheros del FTP a server
                    with open(filename, 'wb') as f:
                        conexion.retrbinary('RETR ' + filename, f.write)        
            enviar_mensaje(listado_videos) # Enviar notificacion con los videos nuevos.
            delete_videos_server(listado_videos) # elimina videos del server
    except Exception, e:
        print "[-] No se pudo acceder al directorio. Error: "+str(e)
except Exception, e:
    print "[-] No se pudo establer la conexion con el servidor"+str(e)
finally:
    conexion.quit()
