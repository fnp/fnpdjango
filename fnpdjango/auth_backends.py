from django.conf import settings
from django_cas.backends import CASBackend

attr_map = getattr(settings, 'CAS_USER_ATTRS_MAP', {
    'email': 'email',
    'firstname': 'first_name',
    'lastname': 'last_name',
})

class AttrCASBackend(CASBackend):
    def authenticate(self, ticket, service, request):
        user = super(AttrCASBackend, self).authenticate(ticket, service, request)
        for attr, value in request.session.get('attributes', {}).items():
            try:
                local_attr = attr_map[attr]
            except KeyError:
                pass
            else:
                setattr(user, local_attr, value)
        user.save()
        return user

