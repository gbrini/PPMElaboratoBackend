from rest_framework.throttling import UserRateThrottle

class RoleBasedThrottle(UserRateThrottle):
    scope = 'user'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)

            if user_role == 'admin':
                return None

            self.scope = role if role in [ 'standard', 'premium' ] else 'standard'
        
        return super().get_cache_key(request, view)