# Conexión entre servidor y camara Yi Home 1080p

El programa realiza una conexión entre el servidor y la camara Yi Home 1080p mediante FTP.

### Pre-requisitos 📋

Servidor:
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.4 LTS
Release:	18.04
Codename:	bionic

Cámara IP Yi Home 1080p
Camara configurada para permitir el acceso mediante FTP.

### Instalación 🔧

Librería necesaria para poder realizar conexiones con la API de Telegram
apt-get install python-requests


## Ejecutando las pruebas ⚙️

Para la realización de las pruebas se deben de rellenar las siguientes variables aquí detalladas.
# Datos Conexion Camara
servidor="192.168.1.XXX"
user="root"
passwd="XXXXXXXX"
# Credenciales Telegram
id = "XXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Fichero registro de videos.
fname="listado_videos_mp4.txt"

## Construido con 🛠️

Python 2.7.17
Custom Firmware for Yi Camera based on MStart platform https://github.com/roleoroleo/yi-hack-MStar