from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from member.forms import UserEditForm

User = get_user_model()

__all__ = (
    'my_profile',
    'my_profile_edit',
)

def my_profile(request, user_pk=None):
    if not request.user.is_authenticated and not user_pk:
        login_url = reverse('accounts:login')
        redirect_url = login_url + '?next=' + request.get_full_path()
        return redirect(redirect_url)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user
    context = {
        'cur_user': user
    }

    return render(request, 'member/my_profile.html', context)


@login_required
def my_profile_edit(request):
    if request.method == "POST":
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('member:my_profile_edit')

    else:
        form = UserEditForm(instance=request.user)
        print(form)
    context = {
        'user': request.user,
        'form': form,
    }
    return render(request, 'member/my_profile_edit.html', context)
