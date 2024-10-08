import json
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from home.models import Setting,ContactFormu,ContactFormMessage,UserProfile
from home.forms import SearchForm,SignUpForm
from product.models import Product,Category,Images,Comment



from order.models import ShopCart





# Create your views here.
def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()

    dayproducts= Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    context = {'setting': setting,
               'category': category,
                'page': 'home',
               'sliderdata': sliderdata,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts':randomproducts
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting':setting,'category':category}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting':setting,'category':category}
    return render(request, 'referanslarimiz.html', context)



def iletisim(request):

    if request.method == 'POST': # check post
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #veritabanına kaydeder
            messages.success(request,"Measjınız başarı ile gönderilmiştir.Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')


    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context={'setting':setting,'form':form,'category':category}
    return render(request,'iletisim.html',context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products=Product.objects.filter(category_id=id)
    context = {'products':products,
               'category': category,
               'slug':slug,
               'categorydata':categorydata}
    return render(request,'products.html',context)


def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images=Images.objects.filter(product_id=id)
    comments= Comment.objects.filter(product_id=id,status='True')
    context = {'product': product,
               'category': category,
               'images':images,
               'comments':comments
               }
    return render(request,'product_detail.html',context)


def content_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.filter(category_id=id)
    link = '/product/'+str(product[0].id)+'/'+product[0].slug

    return HttpResponseRedirect(link)

def product_search(request):
    if request.method == 'POST': # Chect form post
       form =SearchForm(request.POST)
       if form.is_valid():
           category = Category.objects.all()

           query =form.cleaned_data['query'] #Get form data
           catid= form.cleaned_data['catid'] # Get form data
           # return HttpResponse(catid)
           if catid == 0:
               products= Product.objects.filter(title__icontains=query)  # Select * from product where title like %query%
           else:
               products= Product.objects.filter(title__icontains=query, category_id=catid)

           #return HttpResponse(products)

           context = {'products': products,
                      'category': category,
                      }
           return render(request, 'products_search.html', context)
    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı veya şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
               'category': category,
               }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, "Tebrikler.Üye oldunuz")

            return HttpResponseRedirect("/")
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
              }
    return render(request, 'signup.html', context)


#def menu(request,id):
#    content= Content.objects.get(menu_id=id)
#    if content:
#        link='/content/' + str(content.id)+'/menu'
#        return HttpResponseRedirect(link)
#    else:
#        messages.warning (request, "Hata! İlgili içerik bulunamadı")
#        link='/'
#        return HttpResponseRedirect(link)

#def contentdetail(request, id, slug):
#    category =Category.objects.all()
#    menu=Menu.objects.all()
#    content=Content.objects.get(pk=id)
#    images=CImages.objects.filter(content_id=id)
#    #comments =Comment.objects.filter(product_id=id, status='True')
#    context= {'content': content,
#                'category': category,
#                 'menu':menu,
#                 'images': images,
#                }
#return render(request,'content_detail.html',context)