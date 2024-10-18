import os


if 'backup.zip' in os.listdir('./'):
    os.system('rm ./backup.zip')


os.system('mkdir backup')
os.system('cp -r ./bot/barcodes ./backup/barcodes')
os.system('cp ./lelit_loyalty/db.sqlite3 ./backup/db.sqlite3')
os.system('zip -r backup.zip ./backup')
os.system('rm -r ./backup')
