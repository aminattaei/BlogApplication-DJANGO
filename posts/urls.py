from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("posts", views.PostListViewSetApiView)
router.register("comments", views.CommentListViewSetApiView)
router.register("contents", views.ContentListViewSetApiView)
router.register("users", views.UserListViewSetsApiView)


from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("", views.BlogHomeListView.as_view(), name="Post_list"),
    path("<int:pk>/", views.Post_Detail, name="Post_detail"),
    path("<int:pk>/delete/", views.BlogHomeDeleteView.as_view(), name="Post_delete"),
    path("<int:pk>/update/", views.BlogHomeUpdateView.as_view(), name="Post_update"),
    path("add/", views.BlogHomeCreateView.as_view(), name="Post_create"),
    path(
        "all_users_posts/",
        views.AllUsersPostsView.as_view(),
        name="Post_all_users_posts",
    ),
    path("contact/", views.ContactFormView.as_view(), name="contact_view"),
    path(
        "contact_done/", views.ContactDoneTemplateView.as_view(), name="success_content"
    ),
    path(
        "approve_article/<int:post_id>/", views.approve_article, name="approve_article"
    ),
    path("search/", views.Search, name="search_results"),
    path("profile/", views.profile, name="profile"),
    path("api/posts/<int:pk>/", views.PostDetail.as_view(), name="post-detail"),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
