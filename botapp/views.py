from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import User

def number_to_word(balance):
    if 1000 <= balance < 1000000:
        balance = str(balance // 1000) + "K"
    elif 1000000 <= balance < 100000000:
        balance = str(balance // 1000000) + "M"
    elif 100000000 <= balance < 1000000000:
        balance = str(balance // 100000000) + "B"
    elif 1000000000 <= balance < 1000000000000:
        balance = str(balance // 1000000000) + "T"
    elif 1000000000000 <= balance < 1000000000000000:
        balance = str(balance // 1000000000000) + "Q"

    return balance

def index(request, telegram_id):
    # Foydalanuvchini ID bo'yicha olish
    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Foydalanuvchi topilmadi")

    # Limitni avtomatik yangilash
    coins = user.coins
    coins = number_to_word(coins)

    return render(request, 'coin/index.html', {'user': user, 'coins': coins, 'limit': user.limit})

def update_coins(request, telegram_id):
    if request.method == "POST":
        # Foydalanuvchini ID bo'yicha olish
        try:
            user = User.objects.get(telegram_id=telegram_id)

        except User.DoesNotExist:
            return JsonResponse({'error': "Foydalanuvchi topilmadi"}, status=400)

        # Coinsni yangilash
        coins = int(request.POST.get('coins', 0))
        user.refill_limit()

        if 0 < user.tap <= user.limit:
            user.coins += coins
            user.limit -= user.tap
            user.save()

        return JsonResponse({'coins': user.coins, 'limit': user.limit})
    else:
        return JsonResponse({'error': "Noto'g'ri so'rov turi"}, status=400)


def boost(request, telegram_id):
    try:
        userData = User.objects.get(telegram_id=telegram_id)
        if request.method == 'POST':
            if 'tap' in request.POST:
                if 1 <= userData.tap < 10:
                    price = userData.tap * 1000 + 1000
                    if userData.coins >= price:
                        userData.tap += 1
                        userData.coins -= price
                        userData.save()

            if 'energy' in request.POST:
                if 1000 <= userData.energy < 10000:
                    price = (userData.energy // 1000) * 5000 + 5000
                    if userData.coins >= price:
                        userData.energy += 1000
                        userData.coins -= price
                        userData.save()

        tap_price = number_to_word(userData.tap * 1000 + 1000)
        energy_price = number_to_word( (userData.energy // 1000) * 5000 + 5000)
        balance = number_to_word(userData.coins)

        context = {
            'user_telegram_id': userData.telegram_id,
            'tap': userData.tap + 1,
            'tap_price': tap_price,
            'energy': (userData.energy // 1000) + 1,
            'energy_price': energy_price,
            'balance': balance,
        }
        return render(request, 'coin/boost.html', context)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Coin instance does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def guid(request, telegram_id):
    userData = User.objects.get(telegram_id=telegram_id)

    return render(request, 'coin/guid.html', {'user_telegram_id': userData.telegram_id})