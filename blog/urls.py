from django.urls import path
from .views import PoatListView

app_name = 'blog'

urlpatterns = [
    path('', PoatListView.as_view(), name='home'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail')
]
