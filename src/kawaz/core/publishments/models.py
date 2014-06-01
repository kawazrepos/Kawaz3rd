from django.db import modelsfrom django.utils.translation import ugettext as _from .lookups import published_lookup, draft_lookupPUB_STATES = (    ('public',      _("Public")),    ('protected',   _("Internal")),    ('draft',       _("Draft")),)class PublishmentManagerMixin(object):    """    A model manager mixin for ``AbstractPublishmentModel`` model.    """    author_field_name = 'author'    def related(self, user):        """        Return a queryset which include the objects related to the specified        user, namely an union of the ``published`` and ``draft`` queryset.        """        q = published_lookup(user)        q |= draft_lookup(user,                          author_field_name=self.author_field_name)        return self.filter(q).distinct()    def published(self, user):        """        Return a queryset which include the objects published to the specified        user.        A queryset which include public/protected objects would be returend if        the specified user is the member of Kawaz, otherwise it only include        the public objects.        """        return self.filter(published_lookup(user))    def draft(self, user):        """        Return a queryset which include the draft objects of the specified user.        """        return self.filter(draft_lookup(user,                                        author_field_name=self.author_field_name))