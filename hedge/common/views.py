from django.http import Http404
from django.http import JsonResponse
from registration.users import UserModel
User = UserModel()

def check_username(request):
	u = request.GET.get("username", '')
	if u:
		try:
			ue = User.objects.get(username=u)
			return JsonResponse({"valid":False})
		except User.DoesNotExist:
			return JsonResponse({"valid":True})
	else:
		raise Http404('')
