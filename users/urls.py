from django.urls import path
from . import views
from . import api
from rest_framework import routers

app_name = "users"

router = routers.DefaultRouter()
router.register('api/customers', api.customers_api)
# router.register('api/customers2',api.customers_api2)
# router.register('api/users_router',api.UsersViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("add", views.add, name="add"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path(r'^delete/(?P<row_id>\d+)/$', views.delete, name="delete"),
    path(r'^update_user/(?P<row_id>\d+)/$',
         views.update_user, name="update_user"),



    # api
    #to upload files
    path("upload-file/", api.FileUploadView.as_view(), name='upload-file'),
    #to get max id
    path("api/get_max_id/", api.get_max_id,name="get_max_id"),
    #to remove file
    path("api/remove_file/", api.remove_file,name="remove_file"),


    # path("api/users",api.get_users_api,name="get_users_api"),
    # path("api/users/<int:id>",api.get_user_api,name="get_user_api"),
    # path("api/users/add",api.save_user_api,name="save_user_api"),
    # path("api/get_users_class",api.get_users_class.as_view(),name="get_users_class"),
    # path("api/users_class2/<int:id>",api.users_class2.as_view(),name="users_class2"),
    path("api/customer_delete/<int:id>", api.customers_api.destroy, name="customer-delete"),



]
urlpatterns += router.urls
