from django.shortcuts import render

def frontend(request):
    response = render(request, "index.html")
    response['Permissions-Policy'] = 'camera=(self)'
    return response
