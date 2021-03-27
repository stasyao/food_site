from django.shortcuts import render


def page_not_found(request, exception):
    return render(
        request,
        '404.html',
        {'path': request.path},
        status=404
    )


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def server_error(request):
    return render(request, '500.html', status=500)
