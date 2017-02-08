# -*- coding: utf-8 -*-

from django.db import models

"""
Design thoughts.

HashTable - bad
    hash       count      webservice_status
    kejfewie   1          SHIP_ME
    owkeofkw   2          SHIPPED
    okwefko    2          

HashTable - good
    hash         shipped     content_type_id      object_id    field      
    kejfewie     true        2                    3            title
    owkeofkw     false       4                    4            description
    owkeofkw     false       4                    6            description
    okwefko      true        3                    3            subject
    okwefko      true        3                    4            subject

Signals
    Field was changed
        Hvis fra not None:
            Fjern en række af gammel hash
        Tilføj række med ny hash

Celery tasks

@task
def field_changed(field):
    '''
    - Syncs a single term to poeditor.com.
    - Adds single term to HashTable.
    - Removes old hash from HashTable.
    '''

@periodic_task
def sync_terms():
    '''
    Loops over all terms and syncs with poeditor.com
    '''
    pass

"""


class Terms(models.Model):
    hash =
    shipped =
    content_type_id
    object_id
    field_name
