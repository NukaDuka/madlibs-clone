from django.shortcuts import render
from django.http import HttpResponse, Http404
import redis

# Create your views here.

def index(request):
    return render(request, 'index.html')

def results(request):
    if request.method != 'POST':
        raise Http404('Does not exist')
    r = redis.Redis(host='test-redis.vaxrbu.0001.aps1.cache.amazonaws.com', port=6379, db=0)
    try:
        response = r.incr('hits')
        ip = get_client_ip(request)
        key = 'client:' + str(ip)
        response = r.incr(key)
    except:
        print('Was not able to connect to redis instance')

    post = request.POST
    pr = post['pr'].lower()
    gp = post['gp']
    exc = post['exc'].lower().capitalize()
    adv = post['adv'].lower()
    verb = post['verb'].lower()
    adj = post['adj'].lower()
    noun = post['noun']
    if pr == "he":
        pr2 = 'his'
    elif pr == "she":
        pr2 = 'her'
    else:
        pr2 = 'their'
    context = {'pr':pr, 'pr2':pr2,'gp':gp, 'exc':exc, 'adv':adv, 'verb':verb, 'adj':adj, 'noun':noun}
    return render(request, 'results.html', context=context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def stats(request):
    ip = get_client_ip(request)
    r = redis.Redis('test-redis.vaxrbu.0001.aps1.cache.amazonaws.com', port=6379, db=0)
    try:
        hits = int(r.get('hits'))
        key = 'client:' + str(ip)
        clhits = r.get(key)
        print(clhits)
        context = {'hits':hits}
        if int(hits) == 1:
            context['plural'] = 'time'
        else:
            context['plural'] = 'times'
        if clhits != None:
            context['clhits'] = int(clhits)
            if int(clhits) == 1:
                context['pluralcl'] = 'time'
            else:
                context['pluralcl'] = 'times'
        return render(request, 'stats.html', context=context)
    except:
        raise
        raise Http404('Temporarily not found')

