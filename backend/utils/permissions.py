from rest_framework import permissions

class IsHospitalAdmin(permissions.BasePermission):
    """
    Custom permission to only allow hospital admins to access certain views.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'hospital_admin')
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner
        return obj.user == request.user or obj.patient == request.user or obj.donor == request.user