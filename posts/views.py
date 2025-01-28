from .models import Post, Comment, Tag, Contact
from .form import CommentForm, ContactForm

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from rest_framework.parsers import JSONParser
from .serializers import PostSerializer


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
    ordering = ["-created_time"]

    def get_queryset(self):
        return Post.objects.filter(is_approved=True)


# class BlogHomeDetailView(DetailView):
#     model = Post
#     template_name = "posts/Post_detail.html"
#     context_object_name = "post"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.object
#         context["comments"] = Comment.objects.filter(blog=post)
#         context["form"] = CommentForm()
#         context["tags"] = Tag.objects.filter(postFore=post)
#         return context

#     def post(self, request, *args, **kwargs):
#         post = self.get_object()
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.blog = post
#             comment.user = request.user
#             comment.name = request.user.username
#             comment.email = request.user.email
#             comment.save()
#             messages.success(request, "نظر شما با موفقیت ثبت شد!")
#             return redirect("Post_detail", pk=post.pk)
#         else:
#             messages.error(
#                 request, "مشکلی در ثبت نظر وجود دارد. لطفاً دوباره تلاش کنید."
#             )
#             return self.render_to_response(self.get_context_data(form=form))


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


def Post_list(request):
    if request.method == "GET":
        snippets = Post.objects.all()
        serializer = PostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Post_Detail(request, pk):
    post = get_object_or_404(Post, id=pk, is_approved=True)  # فقط مقاله تایید شده
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
