from django.conf.urls import url
from Projects import views
from django.urls import path

urlpatterns = [


            url('projects', views.ProjectList.as_view(), name='Projects-list'),
            path('<int:pk>/Update/', views.ProjectUpdateView.as_view(),

         name='project-update'),

            path('<int:pk>/Details/', views.ProjectDetailView.as_view(),
         name='project-detail'),
]
