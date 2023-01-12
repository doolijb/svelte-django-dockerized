from rest_framework import serializers


class GETAccountSerializer(serializers.Serializer):
    """
    GET serializer that gets authenticated user's account information,
    else returns default unauthenticated values.
    """

    def __init__(self, request):
        # Default anonymous account

        self.body = {
            "userName": None,
            "isAuth": False,
            "passwordSet": False,
            "email": None,
            "emails": [],
            "isStaff": False,
            "status": {"value": 0, "label": "Unauthorized"},
            "social": {},
            "favorites": [],
        }

        # Get authenticated account
        if request.user.is_authenticated:
            self.body["userName"] = request.user.username
            self.body["isAuth"] = request.user.is_authenticated
            self.body["passwordSet"] = bool(
                request.user.password and request.user.has_usable_password()
            )
            self.body["email"] = request.user.emailaddress_set.get(primary=True).email
            self.body["emails"] = request.user.emailaddress_set.all().values(
                "email", "primary", "verified"
            )
            self.body["isStaff"] = request.user.is_staff
