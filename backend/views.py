from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


FRONTEND_DIR = settings.BASE_DIR / "frontend"
ALLOWED_FRONTEND_FILES = {
    "CEO.jpeg",
    "favicon.png",
    "index.html",
    "support.html",
    "twitter-card.png",
}


def serve_frontend_page(request, filename="index.html"):
    return serve_frontend_file(request, filename)


def serve_frontend_file(request, filename):
    if filename not in ALLOWED_FRONTEND_FILES:
        raise Http404("Frontend file not found.")

    path = (FRONTEND_DIR / filename).resolve()
    if FRONTEND_DIR.resolve() not in path.parents and path != FRONTEND_DIR.resolve():
        raise Http404("Frontend file not found.")
    if not path.exists() or not path.is_file():
        raise Http404("Frontend file not found.")

    return FileResponse(path.open("rb"))
