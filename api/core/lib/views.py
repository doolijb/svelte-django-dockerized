from rest_framework.viewsets import ViewSetMixin

class HasPermissionsHelperMixin(ViewSetMixin):
    """
    A mixin that overrides `get_serializer_class` method that returns a different
    serializer class depending on whether the user is staff or not.
    """
    admin_serializer_class = None
    request_user_is_admin: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ext_perms(self, permissions) -> None:
        """
        A helper method to extend permissions, reducing boilerplate.
        """
        self.permission_classes += permissions

    def set_perms(self, permissions) -> None:
        """
        A helper method to set permissions, reducing boilerplate.
        """
        self.permission_classes = permissions
