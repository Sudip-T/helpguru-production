from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsObjectOwner(BasePermission):
    msg = 'not associated with this object'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        user_type = request.user.user_type
        owner_attrs = {
            'customer':('profile','appointment','customer','user'),
            'vendor':('vendor','appointment','user')
        }

        for attr in owner_attrs.get(user_type,[]):
            if hasattr(obj,attr):
                owner = getattr(obj,attr)
                if owner == request.user:
                    return True
                raise PermissionDenied({'detail':f'{user_type} {self.msg}'})
        
        return False


class IsVerified(BasePermission):
    message = 'You need to verify your account first to perform this action'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        elif request.user.user_type == 'customer':
            try:
                customer = request.user.customer
                if not customer.user_status == 'Verified':
                    raise PermissionDenied(self.message)
                return True
            except AttributeError:
                raise PermissionDenied('No customer associated with this user')
        elif request.user.user_type == 'vendor':
            try:
                vendor = request.user.vendor
                print(vendor.vendor_status)
                if not vendor.vendor_status == 'Verified':
                    raise PermissionDenied(self.message)
                return True
            except AttributeError:
                raise PermissionDenied('No vendor associated with this user')
        return False


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        raise PermissionDenied('only admin users can perform this action')



def apply_permissions(*permission_classes):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()

                if (
                    hasattr(permission, 'has_object_permission') and
                    self.action in ['retrieve', 'update', 'partial_update']
                ):
                    # Check for object-level permission
                    obj = self.get_object()
                    if not permission.has_object_permission(request, self, obj):
                        return Response(
                            {'error': 'Permission denied'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                elif not permission.has_permission(request, self):
                    # Check for general permission
                    return Response(
                        {'error': 'Permission denied'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator