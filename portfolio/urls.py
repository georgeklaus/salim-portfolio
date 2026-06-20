from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("profile/", views.profile_detail, name="profile-detail"),
    path("projects/", views.project_list, name="project-list"),
    path("skills/", views.skill_list, name="skill-list"),
    path("experience/", views.experience_list, name="experience-list"),
    path("education/", views.education_list, name="education-list"),
    path("contact/", views.contact_create, name="contact-create"),
]
