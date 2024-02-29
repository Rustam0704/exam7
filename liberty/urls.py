from django.urls import path

from liberty.views import (HomePageView, ExploreView, UserLoginView, UserLogoutView, register_view, CategoryDetailView, \
                           ItemsListView, SearchExploreView, user_profile, post_detail, post_create, item_update,
                           item_delete, LikeItemView)

app_name = 'liberty'
urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('register/', register_view, name='register-page'),
    path('login/', UserLoginView.as_view(), name='login-page'),
    path('logout/', UserLogoutView.as_view(), name='logout-page'),
    path('user/<str:username>', user_profile, name="author"),
    path('explore/', ExploreView.as_view(), name="explore"),
    path('search', SearchExploreView.as_view(), name='search'),
    path('item-list/', ItemsListView.as_view(), name="item_list"),
    path('new-item/', post_create, name="create"),
    path('item-detail/<pk>', post_detail, name="detail"),
    path('category/<pk>', CategoryDetailView.as_view(), name='category_list'),
    path('update/<int:pk>', item_update, name="update"),
    path('delete/<int:pk>', item_delete, name="delete"),
    path('like/<pk>', LikeItemView.as_view(), name='item-like'),

]
