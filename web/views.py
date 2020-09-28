from django.shortcuts import render
from shots.models import Shot, ShotsFile


def index(request):
    shots = Shot.objects.filter(is_published=True).order_by('-published')
    shots_files = ShotsFile.objects.all()
    context = {
        'shots': shots,
    }
    return render(request, 'web/index.html', context)
