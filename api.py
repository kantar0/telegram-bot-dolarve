import os
import requests
import settings

settings.start_env()  # carga las variables de entorno

newHeaders = {'auth-token': os.getenv('API_TOKEN1')}
recordToState = {
    'price': 4.43,
    'rate_porcentage': 0.57,
    'rate_porcentage_symbol': "🔺"
}
response = requests.post(os.getenv('API_URL_BOT_DISCORD'),
                         headers=newHeaders, json=recordToState)

if (response.status_code == 200): 
    log_info("New statu has been sent  to Bot Discord.")
else:
    log_info("Error sending new statu to Bot Discord.")
