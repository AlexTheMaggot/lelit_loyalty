import random
import os
import django
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lelit_loyalty')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lelit_loyalty.settings')
django.setup()


from api.models import User


async def user_get_or_create(user_id):
    try:
        user = await User.objects.aget(user_id=user_id)
    except User.DoesNotExist:
        user = User(user_id=user_id, balance=0)
        await user.asave()
    return user


async def user_barcode_generate(user_id):
    user = await User.objects.aget(user_id=user_id)
    if not user.barcode:
        barcode = ''
        for i in range(9):
            num = random.randint(0, 9)
            barcode += str(num)
        try:
            users = await User.objects.aget(barcode=barcode)
            await user_barcode_generate(user_id)
        except User.DoesNotExist:
            user.barcode = barcode
            await user.asave()
