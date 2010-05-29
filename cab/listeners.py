from django.db.models import signals
from ratings.models import RatedItem

def update_rating_score(sender, instance, *args, **kwargs):
    instance.content_object.update_rating()

def start_listening():
    signals.post_save.connect(update_rating_score, sender=RatedItem)
    signals.post_delete.connect(update_rating_score, sender=RatedItem)
