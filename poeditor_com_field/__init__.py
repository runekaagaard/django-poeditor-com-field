from itertools import izip

from celery.task.base import task
from poeditor import POEditorAPI

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import F

from .models import Link

__version__ = '0.1.0'


def _terms(instance):
    return [{
        'value': getattr(instance, x),
        'field_name': x,
        'reference': u"{}-{}-{}".format(instance.__class__.__name__,
            instance.pk, x),
    } for x in instance._poeditor_com_field_fields]


def _post_save_signal(sender, created=None, instance=None, **kwargs):
    update_terms(_terms(instance), instance)


def _content_type(instance):
    return ContentType.objects.get_for_model(instance)


def _posted_hash_exists(hash):
    return Link.objects.filter(hash=hash, posted=True).exists()


@task
def _post_terms(terms, link_pks):
    if len(terms) == 0:
        return
    
    _client().add_terms(settings.POEDITOR_PROJECT_ID, [
        {
            "term": x['value'],
            "context": settings.POEDITOR_CONTEXT,
            "reference": x['reference'],
            "plural": ""
        } for x in terms
    ])
    Link.objects.filter(pk__in=link_pks, posted=False).update(
        posted=True)


def _save_link(term, instance):
    try:
        link = Link.objects.get(
            term=term['value'],
        )
        link.count = F('count') + 1
        link.save()
    except Link.DoesNotExist:
        link = Link.objects.create(
            term=term['value'],
            count=1,
        )

    return link


def _client():
    return POEditorAPI(api_token=settings.POEDITOR_API_TOKEN)


def update_terms(terms, instance):
    links = [_save_link(x, instance) for x in terms]
    unposted_terms = [term for link, term in izip(links, terms)
                      if link.posted is False]
    _post_terms(unposted_terms, [x.id for x in links])
