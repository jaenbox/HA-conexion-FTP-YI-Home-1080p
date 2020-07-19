# Conexión entre servidor y camara Yi Home 1080p

El programa realiza una conexión entre el servidor y la camara Yi Home 1080p mediante FTP, descarga los vídeos al servidor, envío de los videos a la aplicación de mensajería de Telegram mediante su API y elimina el fichero del servidor.

La cámara realiza videos cuando detecta un ruido, cambio de luces o presencias de personas. El programa realizado en python se debe de configurar con el crontab para que cada X minutos se recorran estos directorios en busca de nuevos videos y si encuentra uno nuevo se transfiere al servidor y se envía mediante Telegram. 
Como es un programa inicial para comprobar la funcionalidad del sistema el almacenado de los datos para poder comparar los ficheros del directorio de video se almacenan en un fichero de .txt el cual se consulta para verificar el listado de vídeos ya disponibles anteriormente.
La contra de este programa es que la cámara no almacena un timestamp de cada fichero lo cual no se puede saber cuando se ha creado cada vídeo. Por ello se ha optado por recorrer cada minuto para comprobar si existen nuevos vídeos. Otra de las problemáticas que nos encontramos es que se generan mucho falsos positivos los cuales la aplicación de Yi Home no los muestra ya que deducimos que se pasan los vídeos por algún tipo de detector de movimientos antes de mostrarse sobre la misma.

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
** Es necesario disponer de los credenciales para poder conectarse con la api de Telegram desde el servidor.

Configuración crontab. Se ejecuta cada minuto.
crontab -e
* * * * * /usr/bin/python /control_videos_yi_home.py

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