from django.urls import path

from . import views
urlpatterns =[
# ex: /product/
path('', views.index, name='index'),
path('addcomment/<int:id>', views.addcomment, name='addcomment'),
#path('hakkimizda', home.views.detail, name='detail'),
# ex: /polls/5/
#path('<int:question_id>/', views.detail, name='detail'),
]
