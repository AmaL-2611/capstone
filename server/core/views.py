import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer, Review


def dealer_list(request):
    state = request.GET.get('state')
    queryset = Dealer.objects.all()
    if state:
        queryset = queryset.filter(state__iexact=state)
    data = [
        {
            'id': dealer.id,
            'name': dealer.name,
            'state': dealer.state,
            'city': dealer.city,
            'address': dealer.address,
            'phone': dealer.phone,
        }
        for dealer in queryset
    ]
    return JsonResponse(data, safe=False)


def dealer_detail(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({'error': 'Dealer not found'}, status=404)
    return JsonResponse(
        {
            'id': dealer.id,
            'name': dealer.name,
            'state': dealer.state,
            'city': dealer.city,
            'address': dealer.address,
            'phone': dealer.phone,
        }
    )


def review_list(request):
    dealer_id = request.GET.get('dealer_id')
    queryset = Review.objects.all()
    if dealer_id:
        queryset = queryset.filter(dealer_id=dealer_id)
    data = [
        {
            'id': review.id,
            'dealer_id': review.dealer_id,
            'reviewer': review.reviewer,
            'rating': review.rating,
            'comment': review.comment,
            'sentiment': review.sentiment,
        }
        for review in queryset
    ]
    return JsonResponse(data, safe=False)


def car_makes(request):
    return JsonResponse(
        [
            {'make': 'Toyota', 'models': ['Camry', 'Corolla', 'RAV4']},
            {'make': 'Ford', 'models': ['Mustang', 'F-150', 'Explorer']},
        ],
        safe=False,
    )


def analyze_review(request):
    text = request.GET.get('text', '')
    sentiment = 'positive' if 'fantastic' in text.lower() or 'excellent' in text.lower() else 'neutral'
    return JsonResponse({'text': text, 'sentiment': sentiment, 'confidence': 0.92})


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    payload = json.loads(request.body.decode('utf-8'))
    username = payload.get('username')
    password = payload.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'success': True, 'message': 'Login successful', 'username': username})
    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})


@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    payload = json.loads(request.body.decode('utf-8'))
    username = payload.get('username')
    first_name = payload.get('first_name', '')
    last_name = payload.get('last_name', '')
    email = payload.get('email', '')
    password = payload.get('password')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'message': 'Username already exists'}, status=409)
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return JsonResponse({'success': True, 'message': 'Registration successful', 'username': username})
