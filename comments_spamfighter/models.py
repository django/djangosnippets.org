from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Keyword(models.Model):

    # Default field choices. These are good inital values for the default
    # Django comments but you can override it using the settings variable
    # COMMENTS_CHECK_FIELDS_CHOICES

    FIELD_CHOICES = (
        ('user_name', _('Username')),
        ('user_email', _('User Email')),
        ('user_url', _('User URL')),
        ('comment', _('Comment text')),
        ('ip_address', _('IP Address')),
    )
    FIELD_CHOICES = getattr(settings, 'COMMENTS_CHECK_FIELDS_CHOICES', FIELD_CHOICES)

    active = models.BooleanField(_('Active'), default=True)
    keyword = models.TextField(_('Keyword'))
    is_regex = models.BooleanField(_('Is a regular expression'), default=False)
    fields = models.TextField(_('Fields to check'), max_length=255)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        ordering = ('keyword', 'created')
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

    def __unicode__(self):
        return self.keyword
