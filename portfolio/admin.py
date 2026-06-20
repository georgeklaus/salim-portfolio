from django.contrib import admin

from .models import ContactMessage, Education, Experience, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "email", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("full_name", "title", "email")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("name", "category")
    ordering = ("order", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_featured", "published", "order")
    list_filter = ("is_featured", "published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "tech_stack")
    ordering = ("order", "-created_at")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "currently_working", "order")
    list_filter = ("currently_working", "company")
    search_fields = ("role", "company", "description")
    ordering = ("order", "-start_date")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("qualification", "school", "start_date", "end_date", "order")
    search_fields = ("qualification", "school", "description")
    ordering = ("order", "-end_date")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "read", "created_at")
    list_filter = ("read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at", "updated_at")
