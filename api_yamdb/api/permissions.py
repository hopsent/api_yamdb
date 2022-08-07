from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnly(BasePermission):
    """
    Предоставляет доступ только пользователям с ролью 'admin'
    и суперюзеру. В тестах роль суперюзера - 'user',
    поэтому суперюзер обозначен отдельно.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        ) or (request.user.is_superuser and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == 'admin'
        ) or (request.user.is_superuser and request.user.is_authenticated)


class SelfOnly(BasePermission):
    """
    Предоставляем доступ только пользователю
    к записи в базе о самом пользователе.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.username == request.user.username
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Редактирование объекта возможно только для Администратора.
    Для чтения доступно всем.
    """
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_authenticated
                and request.user.role == 'moderator'
                or obj.author == request.user)
