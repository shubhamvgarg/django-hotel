from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.

def home(request):
    emenities = Emenities.objects.all()
    context = {'emenities':emenities}
    return render(request, 'home.html', context)

def getEmenities(request):
    payload = []
    count = 1
    emenities = Emenities.objects.all()
    for emenitiy in  (emenities):
        result = {}
        result['id'] = count
        result['name'] = emenitiy.name
        payload.append(result)
        count += 1
    print(payload)
    return JsonResponse(payload, safe=False)
    

def api_hotels(request):
    hotels_objs = Hotels.objects.all()
    payload = []

    Min_price = request.GET.get('minprice')
    Max_price = request.GET.get('price')
    if Min_price is not None and Max_price is not None:
        hotels_objs = hotels_objs.filter(price__range=(Min_price, Max_price))
    elif Min_price is not None:
        hotels_objs = hotels_objs.filter(price__gte=Min_price)
    elif Max_price is not None:
        hotels_objs = hotels_objs.filter(price__lte=Max_price)

    emenities = request.GET.get('emenities')
    if emenities is not None:
        emenities = emenities.split(',')
        em = []
        for e in emenities:
            try:
                em.append(int(e))
            except Exception as e:
                pass
        
        hotels_objs = hotels_objs.filter(emenities__in =em).distinct()


    for hotel_obj in hotels_objs:
        result = {}
        result['hotel_name'] = hotel_obj.hotel_name
        result['hotel_description'] = hotel_obj.hotel_description
        result['hotel_image'] = hotel_obj.image
        result['hotel_price'] = hotel_obj.price
        payload.append(result)

    return JsonResponse(payload, safe=False)
         