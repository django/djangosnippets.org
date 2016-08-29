import re

from django_comments.moderation import CommentModerator
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .models import Keyword


class SpamFighterModerator(CommentModerator):
    # Check with Akismet for spam
    akismet_check = False

    # If Akismet marks this message as spam, delete it instantly (False) or
    # add it the comment the moderation queue (True). Default is True.
    akismet_check_moderate = True

    # Do a keyword check
    keyword_check = True

    # If a keyword is found, delete it instantly (False) or add the comment to
    # the moderation queue (True). Default is False.
    keyword_check_moderate = False

    def _keyword_check(self, comment, content_object, request):
        """
        Checks each keyword from the keyword table to the fields of the comment.
        Returns True if a keyword matches. Otherwise returns False.
        """
        # Iterate over all keywords
        for keyword in Keyword.objects.filter(active=True):

            # Iterate over all fields
            for field_name in keyword.fields.split(','):

                # Check that the given field is in the comments class. If
                # settings.DEBUG is False, fail silently.
                field_value = getattr(comment, field_name, None)
                if not field_value:
                    if settings.DEBUG:
                        raise ImproperlyConfigured('"%s" is not a field within your comments class.')
                    continue

                # A regular expression check against the field value.
                if keyword.is_regex:
                    if re.match(keyword.keyword, field_value, re.MULTILINE):
                        return True

                # A simple string check against the field value.
                else:
                    if keyword.keyword.lower() in field_value.lower():
                        return True
        return False

    def _akismet_check(self, comment, content_object, request):
        """
        Connects to Akismet and returns True if Akismet marks this comment as
        spam. Otherwise returns False.
        """

        # Check if the akismet library is installed, fail silently if
        # settings.DEBUG is False and return False (not moderated)
        try:
            from akismet import Akismet
        except ImportError:
            raise ImportError('Akismet library is not installed. "easy_install akismet" does the job.')

        # Check if the akismet api key is set, fail silently if
        # settings.DEBUG is False and return False (not moderated)
        AKISMET_API_KEY = getattr(settings, 'AKISMET_SECRET_API_KEY', False)
        if not AKISMET_API_KEY:
            raise ImproperlyConfigured('You must set AKISMET_SECRET_API_KEY with your api key in your settings file.')

        from django.utils.encoding import smart_str
        akismet_api = Akismet(key=AKISMET_API_KEY,
                              blog_url='%s://%s/' % (request.is_secure() and 'https' or 'http',
                                                     Site.objects.get_current().domain))
        if akismet_api.verify_key():
            akismet_data = {'comment_type': 'comment',
                            'referrer': '',
                            'user_agent': '',
                            'user_ip': comment.ip_address}

            if akismet_api.comment_check(smart_str(comment.comment),
                                         data=akismet_data,
                                         build_data=True):
                return True
        return False

    def allow(self, comment, content_object, request):
        """
        Determine whether a given comment is allowed to be posted on
        a given object.

        Return ``True`` if the comment should be allowed, ``False
        otherwise.
        """
        # Original CommentModerator check
        orig_allow = super(SpamFighterModerator, self).allow(comment, content_object, request)
        if not orig_allow:
            return False

        # Keyword check
        if self.keyword_check and not self.keyword_check_moderate:
            # Return False if a keyword matches
            if self._keyword_check(comment, content_object, request):
                return False

        # Akismet check
        if self.akismet_check and not self.akismet_check_moderate:
            # Return False if akismet marks this comment as spam.
            if self._akismet_check(comment, content_object, request):
                return False

        return True

    def moderate(self, comment, content_object, request):
        """
        Determine whether a given comment on a given object should be
        allowed to show up immediately, or should be marked non-public
        and await approval.

        Return ``True`` if the comment should be moderated (marked
        non-public), ``False`` otherwise.
        """
        orig_moderate = super(SpamFighterModerator, self).moderate(comment, content_object, request)
        if orig_moderate:
            return True

        # Keyword check
        if self.keyword_check and self.keyword_check_moderate:
            # Return True if a keyword matches and we want to moderate it
            if self._keyword_check(comment, content_object, request):
                return True

        # Akismet check
        if self.akismet_check and self.akismet_check_moderate:
            # Return True if akismet marks this comment as spam and we want to moderate it.
            if self._akismet_check(comment, content_object, request):
                return True

        return False
