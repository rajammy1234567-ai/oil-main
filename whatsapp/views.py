from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

VERIFY_TOKEN = "my_verify_token_123"

@csrf_exempt
def webhook(request):
    # Verification (GET)
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Invalid token", status=403)

    # Receiving messages (POST)
    if request.method == "POST":
        data = json.loads(request.body)
        print("Webhook data:", data)
        return JsonResponse({"status": "ok"})
