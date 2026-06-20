import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import ContactMessage, Education, Experience, Profile, Project, Skill


def bad_request(errors):
    return JsonResponse({"errors": errors}, status=400)


def absolute_media_url(request, field):
    if not field:
        return ""
    return request.build_absolute_uri(field.url)


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return None


@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})


@require_GET
def profile_detail(request):
    profile = Profile.objects.filter(is_active=True).first()
    if profile is None:
        return JsonResponse({}, status=404)

    return JsonResponse(
        {
            "full_name": profile.full_name,
            "title": profile.title,
            "bio": profile.bio,
            "location": profile.location,
            "email": profile.email,
            "phone": profile.phone,
            "resume_url": profile.resume_url,
            "github_url": profile.github_url,
            "linkedin_url": profile.linkedin_url,
            "website_url": profile.website_url,
        }
    )


@require_GET
def project_list(request):
    projects = Project.objects.filter(published=True)
    return JsonResponse(
        {
            "results": [
                {
                    "title": project.title,
                    "slug": project.slug,
                    "summary": project.summary,
                    "description": project.description,
                    "tech_stack": [
                        item.strip()
                        for item in project.tech_stack.split(",")
                        if item.strip()
                    ],
                    "image_url": project.image_url,
                    "live_url": project.live_url,
                    "source_url": project.source_url,
                    "is_featured": project.is_featured,
                }
                for project in projects
            ]
        }
    )


@require_GET
def skill_list(request):
    skills = Skill.objects.filter(is_featured=True)
    return JsonResponse(
        {
            "results": [
                {
                    "name": skill.name,
                    "category": skill.category,
                    "proficiency": skill.proficiency,
                }
                for skill in skills
            ]
        }
    )


@require_GET
def experience_list(request):
    experiences = Experience.objects.all()
    return JsonResponse(
        {
            "results": [
                {
                    "role": experience.role,
                    "company": experience.company,
                    "location": experience.location,
                    "start_date": experience.start_date.isoformat(),
                    "end_date": experience.end_date.isoformat()
                    if experience.end_date
                    else None,
                    "currently_working": experience.currently_working,
                    "description": experience.description,
                }
                for experience in experiences
            ]
        }
    )


@require_GET
def education_list(request):
    education_items = Education.objects.all()
    return JsonResponse(
        {
            "results": [
                {
                    "school": item.school,
                    "qualification": item.qualification,
                    "start_date": item.start_date.isoformat()
                    if item.start_date
                    else None,
                    "end_date": item.end_date.isoformat() if item.end_date else None,
                    "description": item.description,
                }
                for item in education_items
            ]
        }
    )


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def contact_create(request):
    if request.method == "OPTIONS":
        return JsonResponse({})

    payload = parse_json_body(request)
    if payload is None:
        return bad_request({"body": "Send valid JSON."})

    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    subject = str(payload.get("subject", "")).strip()
    message = str(payload.get("message", "")).strip()

    errors = {}
    if not name:
        errors["name"] = "Name is required."
    if not email:
        errors["email"] = "Email is required."
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Enter a valid email address."
    if not message:
        errors["message"] = "Message is required."

    if errors:
        return bad_request(errors)

    contact = ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )
    return JsonResponse({"id": contact.id, "status": "received"}, status=201)
