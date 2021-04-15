from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ["partial_update", "retrieve"]:
                return True
            else:
                return False
        return False

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class LoginSignupPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        else:
            return False


class FamilyRelativePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action in ["list", "destroy",
                               "partial_update",
                               "create", "relations"]:
                return True
            else:
                return False
        return False

class FamilyMemberPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action == "list":
                return True
            else:
                return False
        return False
