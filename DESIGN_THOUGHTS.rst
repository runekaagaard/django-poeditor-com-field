Design thoughts.

HashTable - bad
    hash       count      webservice_status
    kejfewie   1          SHIP_ME
    owkeofkw   2          SHIPPED
    okwefko    2          

HashTable - good
    hash         shipped     content_type_id      object_id     field      
    kejfewie     true         2                    3            title
    owkeofkw     true         4                    4            description
    owkeofkw     true         4                    6            description
    okwefko      false        3                    3            subject
    okwefko      false        3                    4            subject

Events
    Field changed/created
        if new value in EMPTY_VALUES:
            remove from hashtable if exists, delete_term
        else:
            create/update entry in hashtable, save_term

All gettext data should have the context "django-poeditor-com-field".
            
Code

def api.save_term(term, meta):
    """
    Ships term to poeditor.com.
    """

def api.delete_term(term, meta):
    """
    Deletes term at poeditor.com.
    """
    
@task
def save_term(term, content_type_id, object_id, field):
    """
    Updates or creates a term.
    """
    
    update_poeditor_com = False
    if not exists in db:
        create it
    if other terms with same hash has already been shipped:
        set shipped = true
    else:
        try:
            api.save_term(term)
            set shipped = true
        except RestError:
            set shipped = false

    return term

@task
def delete_term():
    delete term in hashtable
    if other terms with same hash does not exist:
        api.delete_term()

def sync_terms():
    
