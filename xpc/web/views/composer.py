import random
import string
import json
from hashlib import md5
from datetime import datetime
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
from django.conf import settings
from web.models import Composer, Code


def oneuser(request, cid):
    composer = Composer.objects.filter(cid=cid).all()
    composer.two_posts = composer.posts[0:2]
    return render(request, 'oneuser.html', {'composer': composer})


def homepage(request, cid):
    composer = Composer.objects.get(cid=cid)
    composer.rest_posts = composer.posts[1:]
    return render(request, 'homepage.html', {'composer': composer})


def signup(request):
    """显示注册页面"""
    return render(request, 'signup.html')


def send_signup_captcha(request):
    """发送注册验证码"""
    body = request.body.decode('utf-8')
    data = json.loads(body)
    code = Code()
    code.phone = data['phone']
    code.code = ''.join(random.choices(string.digits, k=6))
    code.created_at = datetime.now()
    code.ip = request.META['REMOTE_ADDR']
    code.save()
    print('send code %s to %s' % (code.code, code.phone))
    return JsonResponse({
        "code": "SUCCESS",
        "success": True,
        "message": "成功"})


def register(request):
    """注册逻辑"""
    # {"phone": "13601058935", "password": "123456", "smsCaptcha": "415781", "nickname": "小申", "regionCode": "+86",
    #  "quickMode": False}
    body = request.body.decode('utf-8')
    data = json.loads(body)
    code = Code.objects.filter(phone=data['phone'], code=data['smsCaptcha']).first()
    if not code:
        return JsonResponse({
            "code": "PHONE_CHECK_ERROR",
            "message": "手机号错误或验证码已过期",
            "success": False,
            "date": "20190617-09:50:18"})
    composer = Composer()
    composer.phone = data['phone']
    composer.password = Composer.make_password(data['password'])
    composer.cid = composer.phone
    composer.name = data['nickname']
    composer.banner = ''
    composer.avatar = ''
    composer.like_counts = 0
    composer.follow_counts = 0
    composer.fans_counts = 0
    composer.save()
    return JsonResponse({
        "code": "SUCCESS",
        "success": True,
        "message": "成功"})


def login(request):
    return render(request, 'login.html')


def do_login(request):
    body = request.body.decode('utf-8')
    data = json.loads(body)

    composer = Composer.objects.filter(phone=data['phone']).first()
    if not composer or composer.password != Composer.make_password(data['password']):
        return JsonResponse({
            "code": "PHONE_USER_NOT_EXIST",
            "message": "手机号或者密码错误",
            "success": False,
            "date": "20190617-10:48:03"})

    response = JsonResponse({
        "code": "SUCCESS",
        "success": True,
        "message": "成功",
        "redirect_uri": "/",
    })
    # response = HttpResponse('test')
    response.set_cookie('cid', composer.cid)
    return response


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cid')
    return response


def phone_codes(request):
    return JsonResponse({
        "currentCode": "CN",
        "codes": [
            {
                "code": "CN",
                "phonePrefix": "86",
                "description": "中国大陆"
            },
            {
                "code": "HK",
                "phonePrefix": "852",
                "description": "香港"
            },
            {
                "code": "MO",
                "phonePrefix": "853",
                "description": "澳门"
            },
            {
                "code": "TW",
                "phonePrefix": "886",
                "description": "台湾"
            },
            {
                "code": "US",
                "phonePrefix": "1",
                "description": "美国"
            },
            {
                "code": "AR",
                "phonePrefix": "54",
                "description": "阿根廷"
            },
            {
                "code": "AU",
                "phonePrefix": "61",
                "description": "澳大利亚"
            },
            {
                "code": "AT",
                "phonePrefix": "43",
                "description": "奥地利"
            },
            {
                "code": "BS",
                "phonePrefix": "1242",
                "description": "巴哈马"
            },
            {
                "code": "BY",
                "phonePrefix": "375",
                "description": "白俄罗斯"
            },
            {
                "code": "BE",
                "phonePrefix": "32",
                "description": "比利时"
            },
            {
                "code": "BZ",
                "phonePrefix": "501",
                "description": "伯利兹"
            },
            {
                "code": "BR",
                "phonePrefix": "55",
                "description": "巴西"
            },
            {
                "code": "BG",
                "phonePrefix": "359",
                "description": "保加利亚"
            },
            {
                "code": "KH",
                "phonePrefix": "855",
                "description": "柬埔寨"
            },
            {
                "code": "CA",
                "phonePrefix": "1",
                "description": "加拿大"
            },
            {
                "code": "CL",
                "phonePrefix": "56",
                "description": "智利"
            },
            {
                "code": "CO",
                "phonePrefix": "57",
                "description": "哥伦比亚"
            },
            {
                "code": "DK",
                "phonePrefix": "45",
                "description": "丹麦"
            },
            {
                "code": "EG",
                "phonePrefix": "20",
                "description": "埃及"
            },
            {
                "code": "EE",
                "phonePrefix": "372",
                "description": "爱沙尼亚"
            },
            {
                "code": "FI",
                "phonePrefix": "358",
                "description": "芬兰"
            },
            {
                "code": "FR",
                "phonePrefix": "33",
                "description": "法国"
            },
            {
                "code": "DE",
                "phonePrefix": "49",
                "description": "德国"
            },
            {
                "code": "GR",
                "phonePrefix": "30",
                "description": "希腊"
            },
            {
                "code": "HU",
                "phonePrefix": "36",
                "description": "匈牙利"
            },
            {
                "code": "IN",
                "phonePrefix": "91",
                "description": "印度"
            },
            {
                "code": "ID",
                "phonePrefix": "62",
                "description": "印度尼西亚"
            },
            {
                "code": "IE",
                "phonePrefix": "353",
                "description": "爱尔兰"
            },
            {
                "code": "IL",
                "phonePrefix": "972",
                "description": "以色列"
            },
            {
                "code": "IT",
                "phonePrefix": "39",
                "description": "意大利"
            },
            {
                "code": "JP",
                "phonePrefix": "81",
                "description": "日本"
            },
            {
                "code": "JO",
                "phonePrefix": "962",
                "description": "约旦"
            },
            {
                "code": "KG",
                "phonePrefix": "996",
                "description": "吉尔吉斯斯坦"
            },
            {
                "code": "LT",
                "phonePrefix": "370",
                "description": "立陶宛"
            },
            {
                "code": "LU",
                "phonePrefix": "352",
                "description": "卢森堡"
            },
            {
                "code": "MY",
                "phonePrefix": "60",
                "description": "马来西亚"
            },
            {
                "code": "MV",
                "phonePrefix": "960",
                "description": "马尔代夫"
            },
            {
                "code": "MX",
                "phonePrefix": "52",
                "description": "墨西哥"
            },
            {
                "code": "MN",
                "phonePrefix": "976",
                "description": "蒙古"
            },
            {
                "code": "MA",
                "phonePrefix": "212",
                "description": "摩洛哥"
            },
            {
                "code": "NL",
                "phonePrefix": "31",
                "description": "荷兰"
            },
            {
                "code": "NZ",
                "phonePrefix": "64",
                "description": "新西兰"
            },
            {
                "code": "NG",
                "phonePrefix": "234",
                "description": "尼日利亚"
            },
            {
                "code": "NO",
                "phonePrefix": "47",
                "description": "挪威"
            },
            {
                "code": "PA",
                "phonePrefix": "507",
                "description": "巴拿马"
            },
            {
                "code": "PE",
                "phonePrefix": "51",
                "description": "秘鲁"
            },
            {
                "code": "PH",
                "phonePrefix": "63",
                "description": "菲律宾"
            },
            {
                "code": "PL",
                "phonePrefix": "48",
                "description": "波兰"
            },
            {
                "code": "PT",
                "phonePrefix": "351",
                "description": "葡萄牙"
            },
            {
                "code": "QA",
                "phonePrefix": "974",
                "description": "卡塔尔"
            },
            {
                "code": "RO",
                "phonePrefix": "40",
                "description": "罗马尼亚"
            },
            {
                "code": "RU",
                "phonePrefix": "7",
                "description": "俄罗斯"
            },
            {
                "code": "SA",
                "phonePrefix": "966",
                "description": "沙特阿拉伯"
            },
            {
                "code": "RS",
                "phonePrefix": "381",
                "description": "塞尔维亚"
            },
            {
                "code": "SC",
                "phonePrefix": "248",
                "description": "塞舌尔"
            },
            {
                "code": "SG",
                "phonePrefix": "65",
                "description": "新加坡"
            },
            {
                "code": "ZA",
                "phonePrefix": "27",
                "description": "南非"
            },
            {
                "code": "KR",
                "phonePrefix": "82",
                "description": "韩国"
            },
            {
                "code": "ES",
                "phonePrefix": "34",
                "description": "西班牙"
            },
            {
                "code": "LK",
                "phonePrefix": "94",
                "description": "斯里兰卡"
            },
            {
                "code": "SE",
                "phonePrefix": "46",
                "description": "瑞典"
            },
            {
                "code": "CH",
                "phonePrefix": "41",
                "description": "瑞士"
            },
            {
                "code": "TH",
                "phonePrefix": "66",
                "description": "泰国"
            },
            {
                "code": "TN",
                "phonePrefix": "216",
                "description": "突尼斯"
            },
            {
                "code": "TR",
                "phonePrefix": "90",
                "description": "土耳其"
            },
            {
                "code": "UA",
                "phonePrefix": "380",
                "description": "乌克兰"
            },
            {
                "code": "AE",
                "phonePrefix": "971",
                "description": "阿联酋"
            },
            {
                "code": "GB",
                "phonePrefix": "44",
                "description": "英国"
            },
            {
                "code": "VE",
                "phonePrefix": "58",
                "description": "委内瑞拉"
            },
            {
                "code": "VN",
                "phonePrefix": "84",
                "description": "越南"
            },
            {
                "code": "VG",
                "phonePrefix": "1284",
                "description": "英属维尔京群岛"
            }
        ]
    })
