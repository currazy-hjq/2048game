import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from .models import ScoreList

def initview(request):
    return render(request, 'scorelist/scorelist.html')


def scorelistview(request):
    cur_page = request.GET.get('page',1)
    scorelist = ScoreList.objects.all().order_by('-score')
    paginator = Paginator(scorelist, 5)
    try:
        page = paginator.page(cur_page)
        info = []
        for item in page:
            item_info = {}
            item_info["player"] = item.player
            item_info["score"] = item.score
            item_info["created_time"] = item.created_time
            info.append(item_info)
    except:
        result = {'code': 10003, 'error': '页数有误，小于0或者大于总页数'}
        return JsonResponse(result)
    result = {"code": 200, "listinfo": info,'paginator': {'pagesize': 5, 'total': len(scorelist)}}
    return JsonResponse(result)


def addlistview(request):
    data = json.loads(request.body)
    player = data.get('player','佚名')
    score = int(data.get('score'))
    try:
        item = ScoreList.objects.create(player=player, score=score)
    except Exception as e:
        print(e)
        result = {'code': 10003, 'error': '服务器忙,请再试一次'}
        return JsonResponse(result)
    result = {'code': 200, 'state': 'ok'}
    return JsonResponse(result)
