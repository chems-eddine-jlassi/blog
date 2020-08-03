from blog import views
from django.urls import path,include

urlpatterns = [
    path('', views.PostList, name='home'),
    path('create', views.PostCreateView, name='article-create'),
    path('<slug:slug>', views.PostDetail, name='post_detail'),
    path('<slug>/edit', views.PostUpdateView, name='edit'),
    path('<slug>/delete', views.PostDeleteView, name='delete'),
    path('contact/', views.contact_form, name="contact"),
    path('signup/', views.signup, name='signup')
]