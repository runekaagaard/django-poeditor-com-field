from collections import namedtuple
from copy import deepcopy
import json

from celery.task.base import task
import requests


from django.conf import settings
from django.db.transaction import atomic
from django.core.validators import EMPTY_VALUES
from django.db.models.loading import get_models

from .models import Link

__version__ = '0.1.0'

Term = namedtuple('Term', 'field_name,value,reference')


def _post_init_signal(sender, instance=None, **kwargs):
    instance._poeditor_com_field_cache = deepcopy(instance)
    

def _post_save_signal(sender, created=None, instance=None, **kwargs):
    update_terms(instance, created)
    

def _pre_delete_signal(sender, instance=None, **kwargs):
    remove_terms(instance)


def _link_add(term):
    Link.objects.select_for_update().filter(term=term)
    try:
        link = Link.objects.get(
            term=term.value,
        )
        link.count += 1
        link.references.replace(term.reference, '')
        link.references += term.reference
        link.save()
    except Link.DoesNotExist:
        link = Link.objects.create(
            term=term.value,
            count=1,
            references=term.reference,
        )

    return link


def _link_subtract(term):
    Link.objects.select_for_update().filter(term=term)
    try:
        link = Link.objects.get(
            term=term.value,
        )
        link.count -= 1
        link.references.replace(term.reference, '')
        link.save()
        return link
    except Link.DoesNotExist:
        return None


def _changed_terms(instance, created):
    deleted, added = [], []
    for field_name in instance._poeditor_com_field_fields:
        
        if not created:
            before = make_term(instance._poeditor_com_field_cache, field_name)
        after = make_term(instance, field_name)
        
        if not created and before.value == after.value:
            continue

        if not created and before.value not in EMPTY_VALUES:
            deleted.append(before)

        if after.value not in EMPTY_VALUES:
            added.append(after)

    return deleted, added


def make_term(instance, field_name):
        return Term(
            field_name,
            getattr(instance, field_name),
            u'<{}.{} id={} field={} />'.format(
                instance._meta.app_label,
                instance.__class__.__name__, instance.pk, field_name
            ),
        )


@atomic
def update_terms(instance, created):
    deleted, added = _changed_terms(instance, created)
    modified_link_pks = set()
    if added:
        modified_link_pks |= set(_link_add(x).pk for x in added)
    if deleted:
        modified_link_pks |= set(_link_subtract(x).pk for x in deleted
                                 if x is not None)

    sync_links(modified_link_pks)


@atomic
def remove_terms(instance):
    terms = [make_term(instance, x) for x in instance._poeditor_com_field_fields]
    modified_link_pks = set(_link_subtract(x).pk for x in terms
                            if x is not None)
    sync_links(modified_link_pks)


def post(path, data):
    r = requests.post(
        'https://api.poeditor.com/v2/' + path,
        data={
            'id': settings.POEDITOR_PROJECT_ID,
            'api_token': settings.POEDITOR_API_TOKEN,
            'data': json.dumps(data),
        },
    )
    print "\nPOSTING STUFF TO POEDITOR.COM"
    print "#############################"
    print "path:", path
    print "data:", data
    print "response:", r.json()
    
    return r.json()
        

@task
def sync_links(link_pks=None):
    links = Link.objects.all()
    if link_pks is not None:
        links = links.filter(pk__in=link_pks)

    if not links:
        return

    add = links.filter(count__gt=0, posted=False)
    len(add) # Force evaluation.
    update = links.filter(count__gt=0, posted=True)
    len(update) # Force evaluation.
    delete = links.filter(count__lt=1, posted=True)
    len(delete) # Force evaluation.

    if add:
        post('terms/add', [
            {
                "term": x.term,
                "context": settings.POEDITOR_CONTEXT,
                "reference": x.references,
            } for x in add
        ])
        add.update(posted=True)
        
    if update:
        post('terms/update', [
            {
                "term": x.term,
                "context": settings.POEDITOR_CONTEXT,
                "reference": x.references,
            } for x in update
        ])

    if delete:
        post('terms/delete', [
            {
                "term": x.term,
                "context": settings.POEDITOR_CONTEXT,
            } for x in delete
        ])
        delete.delete()


def sync_existing_models():
    for model in get_models():
        try:
            fields = model._poeditor_com_field_fields
        except AttributeError:
            continue

        link_pks = []
        for obj in model.objects.all():
            for field in fields:
                term = make_term(obj, field)
                Link.objects.select_for_update().filter(term=term)
                try:
                    link = Link.objects.get(
                        term=term.value,
                    )
                    if term.reference not in link.references:
                        link.count += 1
                        link.references += term.reference
                        link.save()
                        link_pks.append(link.pk)
                except Link.DoesNotExist:
                    link = Link.objects.create(
                        term=term.value,
                        count=1,
                        references=term.reference,
                    )
                    link_pks.append(link.pk)

            sync_links(link_pks)
