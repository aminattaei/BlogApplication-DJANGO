from django.urls import path
from .views import (
    BlogHomeListView,
    # BlogHomeDetailView,
    BlogHomeDeleteView,
    BlogHomeUpdateView,
    BlogHomeCreateView,
    AllUsersPostsView,
    ContactFormView,
    ContactDoneTemplateView,
    Post_list,
    Comment_list,
    Contact_list,
    Post_Detail,
    approve_article,
    Search,
    profile,
    PostDetail,
)


urlpatterns = [
    path("", BlogHomeListView.as_view(), name="Post_list"),
    path("<int:pk>/", Post_Detail, name="Post_detail"),
    path("<int:pk>/delete/", BlogHomeDeleteView.as_view(), name="Post_delete"),
    path("<int:pk>/update/", BlogHomeUpdateView.as_view(), name="Post_update"),
    path("add/", BlogHomeCreateView.as_view(), name="Post_create"),
    path("all_users_posts/", AllUsersPostsView.as_view(), name="Post_all_users_posts"),
    path("api/posts/", Post_list, name="posts_api"),
    path("contact/", ContactFormView.as_view(), name="contact_view"),
    path("contact_done/", ContactDoneTemplateView.as_view(), name="success_content"),
    path("approve_article/<int:post_id>/", approve_article, name="approve_article"),
    path("search/", Search, name="search_results"),
    path("api/comments", Comment_list, name="Comment_list"),
    path("api/contacts", Contact_list, name="Contact_list"),
    path("profile/", profile, name="profile"),
    path("api/posts/<int:pk>/", PostDetail.as_view(), name="post-detail"),
]
