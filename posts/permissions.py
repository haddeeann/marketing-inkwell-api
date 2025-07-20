from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostPermissions(BasePermission):
    """
    * Everyone (auth or not) can GET a published post.
    * Only authenticated users can do unsafe requests (POST, PUT, DELETE …).
    * Admin / Editor can touch any post.
    * Writer can only change/delete their *own* posts.
    """

    def has_permission(self, request, view):
        # read-only actions are fine for everyone
        if request.method in SAFE_METHODS:
            return True

        # otherwise must be authenticated AND in one of the groups
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Everybody may view a *published* post
        if request.method in SAFE_METHODS:
            return obj.published or self._can_edit(request.user, obj)

        # For unsafe methods we enforce edit rules
        return self._can_edit(request.user, obj)

    # ---------- helpers ----------
    def _can_edit(self, user, obj):
        if not user.is_authenticated:
            return False

        # Admin or Editor ➜ unrestricted
        if user.groups.filter(name__in=["Admin", "Editor"]).exists():
            return True

        # Writer ➜ only own posts
        if user.groups.filter(name="Writer").exists():
            return obj.author_id == user.id

        return False
