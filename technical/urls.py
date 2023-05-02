"""
URL configuration for technical project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from TAScheduler.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('accounts/create/', CreateAccount.as_view(), name='createAccount'),
    path('accounts/edit/', EditAccount.as_view(), name='editAccount'),
    path('courses/create-course/', CreateCourse.as_view(), name='createCourse'),
    # path('courses/edit/', EditCourse.as_view())
    path('courses/create-lab/', CreateLab.as_view(), name='createLab'),
    path('accounts/', Accounts.as_view(), name='accounts'),
    path('courses/', Courses.as_view(), name='courses'),
    path('notifications/', Notifications.as_view(), name='notifications'),
    path('database/', Database.as_view(), name='database'),
    path('accounts/delete/<int:user_id>', deleteAccount, name='deleteAccount'),
    path('courses/delete/<int:course_id>', deleteCourse, name='deleteCourse'),
    path('courses/view/<int:course_id>', DisplayCourse.as_view(), name='displayCourse'),
]
