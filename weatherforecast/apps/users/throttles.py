from rest_framework.throttling import SimpleRateThrottle

from django.core.cache import cache
from django.conf import settings

print(caches["default"].__class__)
cache.set("test_key", "hello", 60)
print(cache.get("test_key"))

class RoleBasedThrottle(SimpleRateThrottle):
    scope = "standard"

    def configure(self, request):
        if not request.user.is_authenticated:
            self.scope = "anon"
            ident = self.get_ident(request)
        else:
            role = getattr(request.user, "role", "standard")

            if role == "admin":
                self.scope = None
                self.rate = None
                self.key = None
                return

            self.scope = role if role in ("standard", "premium") else "standard"
            ident = request.user.pk

        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        self.key = self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }

    def get_cache_key(self, request, view):
        if not hasattr(self, "key") or self.key is None:
            self.configure(request)
        return self.key

    def allow_request(self, request, view):
        self.configure(request)

        if self.key is None:
            return True

        return super().allow_request(request, view)