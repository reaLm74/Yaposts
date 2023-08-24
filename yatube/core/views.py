from django.shortcuts import render


def page_403(request, exception):
    return render(request, 'core/403.html', {'path': request.path}, status=403)


def page_403_csrf(request, reason=''):
    return render(request, 'core/CSRF403.html')


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def page_500(request):
    return render(request, 'core/500.html', {'path': request.path}, status=500)
