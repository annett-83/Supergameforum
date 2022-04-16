from .views import CategoryList, post_edit_view,answer_edit_view,user_content_view
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',CategoryList.as_view()),
#    path('create/', post_create, name='post_create'),
    path('post/<int:pk>/<str:action>', post_edit_view.as_view(), name='edit_post'),
 #   path('new_answer/<int:pk>/', AnswerNewView.as_view(), name='new_answer'),
    path('answer/<int:pk>/<str:action>', answer_edit_view.as_view(), name='edit_answer'),
    path('user/content', user_content_view.as_view(), name='user_content')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)