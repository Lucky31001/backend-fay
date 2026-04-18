from FAY.models.model_profile import Profile
from rest_framework_simplejwt.tokens import RefreshToken


def build_tokens_for_user(user):
    """Build refresh and access tokens embedding the user's role claim."""
    role = (
        Profile.objects.filter(user=user).values_list("role", flat=True).first()
        or "USER"
    )

    refresh = RefreshToken.for_user(user)
    refresh["role"] = role

    access = refresh.access_token
    access["role"] = role

    return {
        "refresh_token": str(refresh),
        "access_token": str(access),
    }
