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
        dirty = False
        for attr, value in request.session.get('attributes', {}).items():
            try:
                local_attr = attr_map[attr]
            except KeyError:
                pass
            else:
                if getattr(user, local_attr, None) != value:
                    setattr(user, local_attr, value)
                    dirty = True
        if dirty:
            user.save()
        return user

