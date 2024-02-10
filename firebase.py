import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# Путь к файлу сертификата Firebase Admin SDK
cred = credentials.Certificate('private_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://literallylitter-968b9-default-rtdb.firebaseio.com/'
})
# Получите ссылку на корневой узел базы данных Firebase
ref = db.reference('/')