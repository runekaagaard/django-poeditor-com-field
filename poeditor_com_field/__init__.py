from hashlib import sha1

from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .models import Term
from celery.task.base import task
from poeditor import POEditorAPI

__version__ = '0.1.0'


def _terms(instance):
    return [{'value': getattr(instance, x),
             'field_name': x} for x in instance._poeditor_com_field_fields]


def _pre_save_signal(sender, instance=None, **kwargs):
    if instance.pk is not None:
        instance.__poeditor_com_field_cached_instance = sender.objects.get(
            pk=instance.pk)


def _post_save_signal(sender, created=None, instance=None, **kwargs):
    if created:
        add_terms(_terms(instance), instance)
    else:
        print "UPDATE STUFF"


def _content_type(instance):
    return ContentType.objects.get_for_model(instance)


def _shipped_hash_exists(hash):
    return Term.objects.filter(hash=hash, shipped=True).exists()

def client():
    return POEditorAPI(api_token=settings.POEDITOR_API_TOKEN)


@task
def add_term(term, instance):
    hash = sha1(term['value']).hexdigest()
    shipped_hash_exists = _shipped_hash_exists(hash)
    obj = Term.objects.create(
        hash=hash,
        content_type_id=_content_type(instance).pk,
        object_id=instance.pk,
        field_name=term['field_name'],
    )
    client().add_terms(settings.POEDITOR_PROJECT_ID, [
        {
            "term": term['value'],
            "context": settings.POEDITOR_CONTEXT,
            "reference": u"{}-{}-{}".format(instance.__class__.__name__,
                                            instance.pk, term['field_name']),
            "plural": ""
        },
    ])
    print shipped_hash_exists
    

    
def add_terms(terms, instance):
    return [add_term(x, instance) for x in terms]
