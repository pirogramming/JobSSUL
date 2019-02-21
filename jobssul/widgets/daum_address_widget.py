# from urllib import request
# from main import Forms
from django import forms
# from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
# from main.Forms import PostForm
# from main.models import Post



class DaumAddressWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = render_to_string('address_widget.html', {
        }) #context
        return html



#
# class DaumAddressWidget(forms.TextInput):
#     def render(self, name, value, attrs=None, renderer=None):
#         post = get_object_or_404(Post, id=request.POST.get('post_id'))
#         if request.method == 'POST':
#             form = PostForm(request.POST, request.FILES, instance=post)
#             if form.is_valid():
#                 print('ok')
#                 post = form.save()
#
#                 return redirect(f'/main/post/{post.pk}')
#         else:
#             form = PostForm(instance=post)
#             html = render_to_string('address_widget.html', {
#             })  # context
#             return html
#             return render_to_string(request, 'address_widget.html', {
#                 'form': form,
#             })
#
#
