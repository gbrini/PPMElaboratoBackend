from rest_framework.throttling import SimpleRateThrottle

class RoleBasedThrottle(SimpleRateThrottle):
    scope = "standard"

    def configure(self, request):
        if not request.user.is_authenticated:
            self.scope = "anon"
            ident = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()

            if not ident:
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

        print(request.META.get("REMOTE_ADDR"))
        print(request.META.get("HTTP_X_FORWARDED_FOR"))

        print("scope:", self.scope)
        print("key:", self.key)
        print("before:", self.cache.get(self.key))

        if self.key is None:
            return True

        allowed = super().allow_request(request, view)

        print("after:", self.cache.get(self.key))
        print("allowed:", allowed)

        return allowed