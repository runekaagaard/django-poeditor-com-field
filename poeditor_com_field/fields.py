from django.db.models.fields import CharField
from django.db.models.signals import post_save, pre_save

from . import _post_save_signal, _pre_save_signal


class PoeditorComFieldMixin(object):
    pass


class PoeditorComCharField(CharField):
    def contribute_to_class(self, cls, name, *args, **kwargs):
        try:
            cls._poeditor_com_field_fields.append(name)
        except AttributeError:
            cls._poeditor_com_field_fields = [name]
            post_save.connect(_post_save_signal, sender=cls)
            pre_save.connect(_pre_save_signal, sender=cls)

        return super(PoeditorComCharField, self).contribute_to_class(cls, name,
            *args, **kwargs)
