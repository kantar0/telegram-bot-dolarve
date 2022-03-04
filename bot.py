# importing the libraries
import os
import re
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime
from localDataTime import utc_to_local, aslocaltimestr # localDataTime.py
from log_func import log_info, log_error, log_debug, log_warning, start_logging # log_func.py
import settings # settings.py
import database # database. 

# defining the variables
settings.start_env() #carga las variables de entorno
start_logging() # inicia el log
client_mongodb = database.start_connection() # conecta a la base de datos
database.check_connection(client_mongodb) # verifica la conexion a la base de datos
pattern = re.compile(r'[💵]\ [Bs\.]+\ [0-9]+[,][0-9]+') ##patrón de busqueda  para localizar el mensaje con la información del dolar
percentagePattern = re.compile(r'[🔺]\ [0-9]+[,][0-9]+[%]|[🔻]\ [0-9]+[,][0-9]+[%]|[=]\ [0-9]+[,][0-9]+[%]') #patrón de busqueda para localizar el mensaje con el porcentaje del dolar
floatPattern = re.compile(r'[0-9]+[,][0-9]+') #Patrón flotante

with TelegramClient(StringSession(os.getenv('STRING_SESSION')), os.getenv('API_ID'), os.getenv('API_HASH')) as client:
    #si pierdes la sesión, desactiva el comentario de la siguiente linea y quita el parametro os.getenv('STRING_SESSION') del constructor, posteriormente  guarda el token de la sesión en el archivo .env
    #print(StringSession.save(client.session))
    client.start()
    client.send_message('me', 'Telegram bot : I\'m alive, Master')
    log_info('telethon bot started')
    myChannelIDList = ['me','@EnParaleloVzla', '@enparalelovzlatelegram', 'botkantar0']
    @client.on(events.NewMessage(chats=myChannelIDList))
    async def handler(event):
        
        if event.message.photo:
            if(pattern.search(event.message.message)):
                savedPattern = pattern.search(event.message.message).group(0)
                ratePrice = round(float(floatPattern.search(savedPattern).group(0).replace(',','.')),2)
                ratePorcentage = round(float(floatPattern.search(percentagePattern.search(event.message.message).group(0)).group(0).replace(',','.')),2)
                rateSymbolPorcentage = percentagePattern.search(event.message.message).group(0)[0]
                if (rateSymbolPorcentage == '🔺'):
                    rateSymbolPorcentageToRecord = '🔺'
                elif (rateSymbolPorcentage == '🔻'):
                    rateSymbolPorcentageToRecord = '🔻'
                else:
                    rateSymbolPorcentageToRecord = '='
                rawPath = await event.message.download_media(file="media/"+str(event.message.id))
                src_media_path = rawPath.replace("\\","/").replace("./","/")
                recordToDB = {
                    'price': ratePrice ,
                    'social_network_source': 'telegram',
                    'social_network_nickname': 'enparalelovzlatelegram',
                    'captured_date': aslocaltimestr(event.date),
                    'media_path': src_media_path,
                    'rate_porcentage': ratePorcentage,
                    'rate_porcentage_symbol': rateSymbolPorcentageToRecord
                }
                database.insert_record(recordToDB, client_mongodb)
                ##await client.send_message('me', 'telethon: '+ "record inserted. || " + str(datetime.now()))
                log_info("record from channel_id " + str(event.message.peer_id.channel_id) + " has been inserted.")
                
            else:
                log_info("pattern not found in channel_id " + str(event.message.peer_id.channel_id))
        if (event.message.message == '/disconnect' ):
            await client.send_message('me', 'Telegram bot: '+ " Bye!")
            log_info("Telegram bot has been disconnected from command ")
            await client.disconnect()
        if (event.message.message == '/ping' ):
            await client.send_message('me', 'Telegram bot: '+ " pong!")
            log_info("Telegram bot has been pinged from command ")
    @client.on(events.MessageEdited(chats=myChannelIDList))
    async def handler(event):
        if event.message.photo:
            if(pattern.search(event.message.message)):
                savedPattern = pattern.search(event.message.message).group(0)
                ratePrice = round(float(floatPattern.search(savedPattern).group(0).replace(',','.')),2)
                ratePorcentage = round(float(floatPattern.search(percentagePattern.search(event.message.message).group(0)).group(0).replace(',','.')),2)
                rateSymbolPorcentage = percentagePattern.search(event.message.message).group(0)[0]
                if (rateSymbolPorcentage == '🔺'):
                    rateSymbolPorcentageToRecord = '🔺'
                elif (rateSymbolPorcentage == '🔻'):
                    rateSymbolPorcentageToRecord = '🔻'
                else:
                    rateSymbolPorcentageToRecord = '='
                rawPath = await event.message.download_media(file="media/"+str(event.message.id))
                src_media_path = rawPath.replace("\\","/").replace("./","/")
                recordToDB = {
                    'price': ratePrice ,
                    'social_network_source': 'telegram',
                    'social_network_nickname': 'enparalelovzlatelegram',
                    'captured_date': aslocaltimestr(event.date),
                    'media_path': src_media_path,
                    'rate_porcentage': ratePorcentage,
                    'rate_porcentage_symbol': rateSymbolPorcentageToRecord
                }
                database.insert_record(recordToDB)
                ##await client.send_message('me', 'telethon: ' + "record inserted from edited post || " + str(datetime.now()))
                log_info("record  from edited post in channel_id " + str(event.message.peer_id.channel_id) + " has been inserted.")
                
            else:
                log_info("pattern not found from a edited post in channel_id " + str(event.message.peer_id.channel_id))
    client.run_until_disconnected()
    