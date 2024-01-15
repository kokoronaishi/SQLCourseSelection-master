import json
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from Model.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(f"username:{username}")
        print(f"password:{password}")
        try:
            user = User.objects.get(user_id=username)  
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        if check_password(password, user.password):  
            return JsonResponse({'role': user.user_type})  
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)