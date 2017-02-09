from django.db.models.base import Model
from poeditor_com_field.fields import PoeditorComCharField


class TestModel(Model):
    title = PoeditorComCharField(max_length=80)
