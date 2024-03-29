from django.urls import path
from .views import TodoDetail, TodoList, TodoCreate, TodoUpdate, TodoDelete
# , Contact, TodoTwenty
from . import views

urlpatterns = [
    path("", TodoList.as_view(), name="list"),
    path("detail/<int:pk>", TodoDetail.as_view(), name="detail"),
    path("create/", TodoCreate.as_view(), name="create"),
    path("update/<int:pk>", TodoUpdate.as_view(), name="update"),
    path("delete/<int:pk>", TodoDelete.as_view(), name="delete"),

    # path("td_tw/", TodoTwenty.as_view(), name="tw"),

    # path('', views.index, name='index'),
    path('sns', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('goods', views.goods, name='goods'),
    path('good/<int:good_id>', views.good, name='good'),
    path('edit/<int:message_id>', views.edit, name='edit'),
    path('delete/<int:message_id>', views.delete, name='delete'),
    path('find/<int:num>', views.find, name='find'),
    # path('contact', views.contact, name='contact'),

    path('g20', views.index20, name='g20'),

]

# <int:page>

# from django.urls import path
# from . import views

# urlpatterns = [
#   path('', views.index, name='index'),
#   path('<int:page>', views.index, name='index'),
#   path('post', views.post, name='post'),
#   path('goods', views.goods, name='goods'),
#   path('good/<int:good_id>', views.good, name='good'),
#   path('edit/<int:message_id>', views.edit, name='edit'),
#   path('delete/<int:message_id>', views.delete, name='delete'),
#   path('find/<int:num>', views.find, name='find'),
# ]
