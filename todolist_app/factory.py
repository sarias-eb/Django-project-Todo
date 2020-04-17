import factory
from models import ToDo, Priority
from django.contrib.auth.models import User


class PriorityFactory(factory.Factory):
    class Meta:
        model = Priority

    orders = 1
    name = 'ALTA'


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    email = 'admin@admin.com'
    username = 'testuser'
    password = '12345'

    is_superuser = True
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class TodoFactory(factory.Factory):
    class Meta:
        model = ToDo

    title = 'Tarea 1'
    description = 'tarea 1'
    done = False
    priority = PriorityFactory().id
    created_by = UserFactory().id
    updated_by = UserFactory().id
    asigned_user = UserFactory().id
