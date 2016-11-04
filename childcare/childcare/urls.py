
from django.conf.urls import url, include

from django.contrib import admin
from timer.views import IndexView, UserCreateView, ProfileView, ChildDetailView, StayCreateView, \
                        GARBAGEView, NEWView, StayUpdateView, FacultyView, ChildCreateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^GARBAGE/$', GARBAGEView.as_view(), name="garbage_view"),
    url(r'^new/(?P<pk>\d+)/$', NEWView.as_view(), name='new_view'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name="profile_view"),
    url(r'^create/user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^create/child/$', ChildCreateView.as_view(), name="child_create_view"),
    url(r'^child/(?P<pk>\d+)/stay/$', StayCreateView.as_view(), name="stay_create_view"),
    url(r'^child/(?P<pk>\d+)/stay/update/$', StayUpdateView.as_view(), name="stay_update_view"),
    url(r'^child/(?P<pk>\d+)/$', ChildDetailView.as_view(), name="child_detail_view"),
    url(r'^faculty/$', FacultyView.as_view(), name="faculty_view"),
]
