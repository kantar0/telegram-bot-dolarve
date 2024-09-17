# importing the libraries
import os
import re
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel
from localDataTime import utc_to_local, aslocaltimestr  # localDataTime.py
from log_func import (
    log_info,
    log_error,
    log_debug,
    log_warning,
    start_logging,
)  # log_func.py
import settings  # settings.py

# Load environment variables
settings.start_env()  # Cargar las variables de entorno
start_logging()  # Inicia el log
print(os.getenv("API_ID"))
print(os.getenv("API_HASH"))

# Verifica que STRING_SESSION no sea None
string_session = os.getenv("STRING_SESSION") if os.getenv("STRING_SESSION") else None

# Define la función asincrónica principal
async def main():
    # Inicializa el cliente de Telegram
    async with TelegramClient(
        StringSession(string_session),
        int(os.getenv("API_ID")),
        os.getenv("API_HASH"),
    ) as client:
        print(StringSession.save(client.session))
        await client.start()
        await client.send_message("me", "Telegram bot : I'm alive, Master Pedro")
        log_info("telethon bot started")

        # Lista de IDs de canales o grupos de origen (donde se obtendrán los mensajes)
        source_channel_ids = [-2172964101, -1488430381]

        # ID del grupo al que se enviarán los mensajes
        target_group_id = -2478364422

        # Obtener las entidades de los canales o grupos de origen
        source_channels = []
        for channel_id in source_channel_ids:
            channel_entity = await client.get_entity(PeerChannel(channel_id))
            source_channels.append(channel_entity)

        # Obtener la entidad del grupo de destino
        target_group = await client.get_entity(PeerChannel(target_group_id))

        # Opcional: Mostrar los diálogos (puedes comentar esto si no es necesario)
        async for d in client.iter_dialogs():
            channelId = d.entity.id
            channelName = d.name
            print(f"channel id: {channelId}, channel name: {channelName}")

        # Manejador de nuevos mensajes en los canales o grupos de origen
        @client.on(events.NewMessage(chats=source_channels))
        async def forward_message(event):
            msg = event.message
            print
            # Impresión en consola mostrando el mensaje procesado
            print(
                f"Nuevo mensaje detectado. ID: {msg.id}, Texto: {msg.message}, Contiene medios: {'Sí' if msg.media else 'No'}"
            )

            # Caso 1: Si el mensaje tiene medios adjuntos (fotos, videos, etc.)
            if msg.media:
                try:
                    # Descargar el archivo multimedia y obtener el nombre real del archivo
                    filename = await msg.download_media()
                    if filename:
                        print(f"Archivo {filename} descargado.")

                        # Obtener el tamaño del archivo para verificar si es demasiado grande (opcional)
                        file_size = os.path.getsize(filename) / (1024 * 1024)  # Convertir a MB
                        print(f"Tamaño del archivo: {file_size:.2f} MB")

                        # Enviar el archivo multimedia junto con el texto (si existe) al grupo de destino
                        try:
                            if msg.message:
                                await client.send_file(
                                    target_group, filename, caption=msg.message
                                )
                                print(
                                    f"Archivo {filename} enviado al grupo {target_group.id} con el texto: {msg.message}"
                                )
                            else:
                                await client.send_file(target_group, filename)
                                print(
                                    f"Archivo {filename} enviado al grupo {target_group.id} sin texto."
                                )
                        except Exception as e:
                            print(
                                f"Error al enviar el archivo {filename} al grupo {target_group.id}: {e}"
                            )

                        # Eliminar el archivo después de enviarlo
                        if os.path.exists(filename):
                            os.remove(filename)
                            print(
                                f"Archivo {filename} eliminado correctamente después de enviarlo."
                            )
                        else:
                            print(f"El archivo {filename} no existe o ya fue eliminado.")
                    else:
                        print("Error: No se pudo descargar el archivo.")

                except Exception as e:
                    print(f"Ocurrió un error al procesar el archivo: {e}")

            # Caso 2: Si el mensaje solo tiene texto (y no tiene medios)
            elif msg.message:
                try:
                    await client.send_message(target_group, msg.message)
                    print(
                        f"Mensaje de solo texto enviado al grupo {target_group.id}: {msg.message}"
                    )
                except Exception as e:
                    print(
                        f"Error al enviar el mensaje al grupo {target_group.id}: {e}"
                    )

        # Ejecutar hasta desconectar
        await client.run_until_disconnected()


# Ejecutar el bucle de eventos asincrónico
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
