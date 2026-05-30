from rest_framework import permissions

class IsPremiumUser(permissions.BasePermission):
    def has_permission(slef, request, view):
        return bool(request.user 
            and request.user.is_authenticated
            and request.user.role == 'premium'
        )

class IsStandardUser(permissions.BasePermission):
    message = 'Premium membership is required to perform this action'
    def has_permission(slef, request, view):
        return bool(request.user 
            and request.user.is_authenticated
        )