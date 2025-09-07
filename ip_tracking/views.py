from django.http import JsonResponse
from ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=True)
def anonymous_view(request):
    return JsonResponse({"message": "Hello, anonymous user!"})

@csrf_exempt
@ratelimit(key='user', rate='10/m', block=True)
def login_view(request):
    return JsonResponse({"message": "Login attempt"})