from .models import Post, Comment, Contact
from .form import CommentForm, UserRegisterForm

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from .serializers import PostSerializer, CommentSerializer, ContactSerializer


def approve_article(request, post_id):
    post = Post.objects.get(id=post_id)
    post.is_approved = True
    post.save()
    return redirect("post_list")


class BlogHomeListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/Post_index.html"
    paginate_by = 3
    ordering = ["-published_time"]

    def get_queryset(self):
        return Post.objects.filter(is_approved=True)


class BlogHomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/Post_delete.html"
    success_url = reverse_lazy("Post_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)


class BlogHomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/Post_update.html"
    context_object_name = "post"
    fields = ["title", "content", "image"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)


class BlogHomeCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/Post_create.html"
    fields = ["title", "content", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "پست شما با موفقیت ایجاد شد!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "خطا در ارسال فرم. لطفاً دوباره تلاش کنید.")
        return super().form_invalid(form)


class AllUsersPostsView(TemplateView):
    template_name = "posts/Post_author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = get_user_model().objects.all()
        users_with_posts = [
            {
                "user": user,
                "posts": Post.objects.filter(author=user).order_by("-created_time"),
            }
            for user in users
        ]
        context["users_with_posts"] = users_with_posts
        return context


def Post_list(request: Request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Comment_list(request: Request):
    if request.method == "GET":
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Contact_list(request: Request):
    if request.method == "GET":
        contacts = Comment.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Post_Detail(request, pk):
    post = get_object_or_404(Post, id=pk, is_approved=True)
    comments = Comment.objects.filter(blog=post)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                messages.error(
                    request, "اول باید وارد حساب کاربری‌ات بشی، بعد کامنت بذاری!"
                )
                return HttpResponseRedirect(request.path_info)

            obj = form.save(commit=False)
            obj.user = request.user
            obj.name = request.user.username
            obj.email = request.user.email
            obj.blog = post
            obj.save()

            messages.success(request, "کامنتت با موفقیت ثبت شد، مرسی رفیق! 😊")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "یه مشکلی پیش اومده، دوباره امتحان کن!")

    context = {"form": form, "post": post, "comments": comments}
    return render(request, "posts/Post_detail.html", context)


# class ContactFormView(LoginRequiredMixin, FormView):
#     template_name = "posts/contact_form.html"
#     form_class = ContactForm
#     success_url = "/contact_done/"


class ContactFormView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = "posts/contact_form.html"
    fields = ["message"]
    success_url = reverse_lazy("success_content")

    def form_valid(self, form):
        form.instance.name = self.request.user.username
        return super().form_valid(form)


class ContactDoneTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "posts/contact_done.html"


def Search(request):
    result = []
    if request.method == "GET":
        search_query = request.GET.get("q", "")
        if search_query:
            result = Post.objects.filter(title__icontains=search_query)
        context = {"result": result}
    return render(request, "posts/search_results.html", context)


@login_required
def profile(request):
    articles = Post.objects.filter(author=request.user)
    
    approved_count = articles.filter(is_approved=True).count()
    rejected_count = articles.filter(is_approved=False).count()
    pending_count = articles.filter(is_approved=None).count()

    context = {
        'user': request.user,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'articles': articles
    }

    return render(request, 'posts/profile.html', context)