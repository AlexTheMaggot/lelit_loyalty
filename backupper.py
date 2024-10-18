import os


if 'backup.zip' in os.listdir('/home/lelit_loyalty/'):
    os.system('rm /home/lelit_loyalty/backup.zip')


os.system('mkdir /home/lelit_loyalty/backup')
os.system('cp -r /home/lelit_loyalty/bot/barcodes /home/lelit_loyalty/backup/barcodes')
os.system('cp /home/lelit_loyalty/lelit_loyalty/db.sqlite3 /home/lelit_loyalty/backup/db.sqlite3')
os.system('zip -r /home/lelit_loyalty/backup.zip /home/lelit_loyalty/backup')
os.system('rm -r /home/lelit_loyalty/backup')
print('Done!')
