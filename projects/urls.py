from django.conf.urls import url

from projects import views


urlpatterns = [


            url('projects', views.ProjectList.as_view(), name='Projects-list'),
            url('new_project',views.ProjectCreateView.as_view(), name='new_project'),
            url('projects/<int:pk>/update', views.ProjectUpdateView.as_view(),
         name='project-update'),
            url('projects/<int:pk>', views.ProjectDetailView.as_view(),
         name='project-detail'),
]
