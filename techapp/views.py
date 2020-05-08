from django.shortcuts import render, redirect

from django.views.generic import CreateView, DeleteView, UpdateView, ListView, TemplateView

from .models import Category, Pref
from .forms import SearchForm, SignUpForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
import json
import requests


def get_key_id():
    key_id = "e45a551c836ba0e0bfc85d72d5ca03b2"
    return key_id


def search(request):
    if request.method == "GET":
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            category_l = request.GET['category_l']
            pref = request.GET['pref']
            freeword = request.GET['freeword']
            query = get_gnavi_data("", category_l, pref, freeword)
            res_list = rest_search(query)
            hit_count = len(res_list)
            restaurants_info = extract_restaurant_info(res_list)

    params = {
        'total_hit_count': hit_count,
        'restaurants_info': restaurants_info
    }

    return render(request, 'techapp/search.html', params)

def get_gnavi_data(id, category_l, pref, freeword, hit_per_page = 10):
    area = "AREA110" #関東圏にしたいのでハードコーディング
    query = {
        "keyid": get_key_id(),
        "id": id,
        "hit_per_page": hit_per_page,
        "category_l": category_l,
        "pref":pref,
        "freeword": freeword,
        "area": area,
        }
    return query

def rest_search(query):
    rest_list = []
    res = json.loads(requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
    if "error" not in res:
        rest_list.extend(res['rest'])
    return rest_list


def extract_restaurant_info(restaurants: 'restaurant response') -> 'restaurant list':
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant["id"]
        name = restaurant["name"]
        name_kana = restaurant["name_kana"]
        url = restaurant["url"]
        url_mobile = restaurant["url_mobile"]
        shop_image1 = restaurant["image_url"]["shop_image1"]
        shop_image2 = restaurant["image_url"]["shop_image2"]
        address = restaurant["address"]
        tel = restaurant["tel"]
        station_line = restaurant["access"]["line"]
        station = restaurant["access"]["station"]
        latitude = restaurant["latitude"]
        longitude = restaurant["longitude"]
        pr_long = restaurant["pr"]["pr_long"]

        restaurant_list.append([id, name, name_kana, url, url_mobile, shop_image1, shop_image2, address, tel, station_line, station, latitude, longitude, pr_long ])
    return restaurant_list



def shopinfo(request, restid):
    keyid = get_key_id()
    id = restid
    query = get_gnavi_data(id, "", "", "", 1)
    res_list = rest_search(query)
    restaurants_info = extract_restaurant_info(res_list)

    params = {
        'title': '店舗詳細',
        'restaurants_info': restaurants_info
    }

    return render(request, 'techapp/shop_info.html', params)


class IndexView(TemplateView):
    template_name = "techapp/index.html"

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        category_list = Category.objects.all().order_by('category_l')
        pref_list = Pref.objects.all().order_by('pref')
        params = {
            'searchform': searchform
        }
        return params

class Signup(CreateView):
    form_class = SignUpForm
    template_name = 'techapp/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('techapp:index')
        return render(request, 'techapp/signup.html', {'form': form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'techapp/login.html'

class Logout(LogoutView):
    template_name = 'techapp/logout.html'