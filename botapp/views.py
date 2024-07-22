from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import User, RefFriendModel
from encoder import encoder, decoder
from django_user_agents.utils import get_user_agent

def number_to_word(balance):
    if 1000 <= balance < 1000000:
        balance = str(balance // 1000) + "K"

    elif 1000000 <= balance < 100000000:
        balance = str(balance // 1000000) + "M"

    elif balance >= 100000000:
        balance = str(balance // 100000000) + "B"

    return balance


def index(request, telegram_id):
    # Get user from DataBase with user's telegram id
    user_agent = get_user_agent(request)

    if user_agent.is_mobile or user_agent.is_bot or user_agent.is_touch_capable:
        try:
            telegram_id = decoder(telegram_id)
            user = User.objects.get(telegram_id=telegram_id)

        except User.DoesNotExist:
            return render(request, 'errors/user_agent.html', {})

        telegram_id = encoder(telegram_id)

        context = {
            'user': user,
            'coins': user.coins,
            'tap': user.tap,
            'telegram_id': telegram_id,
        }

        return render(request, 'coin/index.html', context)

    else:
        return render(request, 'errors/user_agent.html', {})


def update_coins(request, telegram_id):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile or user_agent.is_bot or user_agent.is_touch_capable:
        if request.method == "POST":
            # Get user from DataBase with user's telegram id
            try:
                user = User.objects.get(telegram_id=telegram_id)

            except User.DoesNotExist:
                return JsonResponse({'error': "Foydalanuvchi topilmadi"}, status=400)

            # Update COin
            coins = int(request.POST.get('coins', 0))
            user.refill_limit()

            if 0 < user.tap <= user.limit:
                user.coins += coins
                user.limit -= user.tap
                user.save()

            return JsonResponse({'coins': user.coins, 'limit': user.limit})

        else:
            return JsonResponse({'error': "Noto'g'ri so'rov turi"}, status=400)

    else:
        return render(request, 'errors/user_agent.html', {})

def boost(request, telegram_id):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile or user_agent.is_bot or user_agent.is_touch_capable:
        try:
            telegram_id = decoder(telegram_id)
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
            energy_price = number_to_word((userData.energy // 1000) * 5000 + 5000)

            user_telegram_id = encoder(userData.telegram_id)

            context = {
                'user_telegram_id': user_telegram_id,
                'tap': userData.tap + 1,
                'tap_price': tap_price,
                'energy': (userData.energy // 1000) + 1,
                'energy_price': energy_price,
                'balance': userData.coins,
            }
            return render(request, 'coin/boost.html', context)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Coin instance does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return render(request, 'errors/user_agent.html', {})

def guid(request, telegram_id):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile or user_agent.is_bot or user_agent.is_touch_capable:
        telegram_id = decoder(telegram_id)

        userData = User.objects.get(telegram_id=telegram_id)
        user_telegram_id = encoder(telegram_id)

        return render(request, 'coin/guid.html', {'user_telegram_id': user_telegram_id})

    else:
        return render(request, 'errors/user_agent.html', {})

def friends(request, telegram_id):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile or user_agent.is_bot or user_agent.is_touch_capable:
        telegram_id = decoder(telegram_id)
        ref_friends = RefFriendModel.objects.filter(telegram_id=telegram_id)
        user_refs = []

        for ref_friend in ref_friends:
            try:
                # ref_friend - this is model in `User`
                user_ref = User.objects.get(telegram_id=ref_friend.ref_friend)
                user_refs.append({
                    'ref_friend': ref_friend.ref_friend,
                    'coins': user_ref.coins
                })
            except User.DoesNotExist:
                # Unless find `User` in database, continue
                continue

        copy = telegram_id
        telegram_id = encoder(telegram_id)
        context = {
            'telegram_id': telegram_id,
            'user_refs': user_refs,
            'copy': copy
        }

        return render(request, 'coin/friends.html', context)

    else:
        return render(request, 'errors/user_agent.html', {})