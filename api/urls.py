from django.urls import path
from .views import (
    CourseListView, get_profile, update_profile,
    add_to_cart, get_cart, remove_from_cart, checkout, get_my_courses,
    BlogListView, BlogDetailView
)
from .auth_views import register, login, refresh_token

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/token/refresh/', refresh_token, name='token-refresh'),
    path('profile/', get_profile, name='get-profile'),
    path('profile/update/', update_profile, name='update-profile'),
    
    # Cart endpoints
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/', get_cart, name='get-cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout, name='checkout'),
    
    # My Courses endpoints
    path('my-courses/', get_my_courses, name='get-my-courses'),
    
    # Blog endpoints
    path('blog/', BlogListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
]