from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import FormView, View
from django.core.mail import send_mail

from .models import Post
from .forms import EmailForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    temlate_name = "blog/list.html"


class ShareFormView(FormView):
    form_class = EmailForm
    template_name = "blog/share.html"
    success_url = "/blog/"


    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST or None)
        self.post = get_object_or_404(Post, id= self.kwargs['post_id'], status='published')
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(self.post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], self.post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(self.post.title, post_url, cd['name'], cd['comments'])

            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
        else:
            form = EmailForm()



        return super(ShareFormView, self).post(self, request, *args, **kwargs)





def post_list_view(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    template = "blog/list.html"

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'page' : page,
        'posts' : posts,
    }
    return render(request, template, context)

def post_detail_view(request, year, month, day, post):
    template = "blog/detail.html"
    posts = get_object_or_404(
        Post,
        slug = post,
        status = 'published',
        publish__year = year,
        publish__month = month,
        publish__day = day,
    )

    context = {
        'posts' : posts
    }

    return render(request, template, context)
