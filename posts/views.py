from .models import Post, Comment, Contact
from .form import CommentForm

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from .serializers import (
    PostSerializer,
    CommentSerializer,
    ContactSerializer,
    UserSerializer,
)
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from drf_spectacular.utils import extend_schema

User = get_user_model()


def approve_article(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.is_approved = True
        post.save()
        return redirect("Post_list")
    except Post.DoesNotExist:
        messages.error(request, "مقاله پیدا نشد.")
        return redirect("Post_list")


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


class PostListViewSetApiView(viewsets.ModelViewSet):
    
    queryset = Post.objects.order_by("-created_time").all()
    serializer_class = PostSerializer
    permission_classes=[IsAuthenticated]


class CommentListViewSetApiView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes=[IsAuthenticated]
    


class ContentListViewSetApiView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes=[IsAuthenticated]
    


def Post_Detail(request, pk):
    try:
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
    except Exception as e:
        messages.error(request, f"خطا در بارگذاری پست: {str(e)}")
        return redirect("Post_list")


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
    try:
        query = request.GET.get("q", "").strip()

        if not query:
            return render(
                request,
                "posts/search_results.html",
                {"error": "لطفاً یک کلمه جستجو وارد کنید."},
            )

        articles = Post.objects.filter(title__icontains=query, is_approved=True)
        if articles.exists():
            return render(request, "posts/search_results.html", {"articles": articles})

        articles = Post.objects.filter(title__icontains=query)
        if articles.exists():
            return render(request, "posts/search_results.html", {"articles": articles})

        return render(
            request,
            "posts/search_results.html",
            {"error": "هیچ مقاله‌ای با این عنوان پیدا نشد."},
        )

    except Exception as e:
        return render(
            request,
            "posts/search_results.html",
            {"error": f"خطا در انجام جستجو: {str(e)}. لطفاً دوباره تلاش کنید."},
        )


@login_required
def profile(request):
    try:
        articles = Post.objects.filter(author=request.user)

        approved_count = articles.filter(is_approved=True).count()
        rejected_count = articles.filter(is_approved=False).count()

        context = {
            "user": request.user,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "articles": articles,
        }
        return render(request, "posts/profile.html", context)

    except Exception as e:
        messages.error(request, f"خطا در بارگذاری پروفایل: {str(e)}")
        return redirect("Post_list")


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class UserListViewSetsApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]
    
