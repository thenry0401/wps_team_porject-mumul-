from django.shortcuts import render, redirect


def index(request):
    return render(request, 'base/base.html')

def callback(request):
    return render(request, 'member/callback.html')