from django.contrib.auth.models import User
from django.contrib.comments.moderation import moderator
from django.conf import settings
from django.db import models
from django.db.models import Count, permalink

from comments_spamfighter.moderation import SpamFighterModerator
from ratings.models import Ratings
from taggit.managers import TaggableManager

from markdown import markdown
from pygments import formatters, highlight, lexers


VERSIONS = getattr(settings, 'CAB_VERSIONS', ())


class LanguageManager(models.Manager):
    def top_languages(self):
        return self.annotate(score=Count('snippet')).order_by('-score')


class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    language_code = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100)
    file_extension = models.CharField(max_length=10)

    objects = LanguageManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('cab_language_detail', (), {'slug': self.slug})

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)


class SnippetManager(models.Manager):
    def top_authors(self):
        return User.objects.annotate(
            score=Count('snippet')).order_by('-score', 'username')

    def top_tags(self):
        return self.model.tags.most_common().order_by('-num_times', 'name')

    def top_rated(self):
        # this is slow
        # return self.annotate(score=Sum('ratings__score')).order_by('-score')
        return self.all().order_by('-rating_score', '-pub_date')

    def most_bookmarked(self):
        # this is slow
        # self.annotate(score=Count('bookmarks')).order_by('-score')
        return self.all().order_by('-bookmark_count', '-pub_date')

    def matches_tag(self, tag):
        return self.filter(tags__in=[tag])


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language)
    author = models.ForeignKey(User)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    version = models.FloatField(choices=VERSIONS, default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    bookmark_count = models.IntegerField(default=0)  # denormalized count
    rating_score = models.IntegerField(default=0)  # denormaliazed score

    ratings = Ratings()
    tags = TaggableManager()

    objects = SnippetManager()

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description, safe_mode="escape")
        self.highlighted_code = self.highlight()
        super(Snippet, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('cab_snippet_detail', (), {'snippet_id': self.id})

    def highlight(self):
        return highlight(self.code,
                         self.language.get_lexer(),
                         formatters.HtmlFormatter(linenos=True))

    def get_tagstring(self):
        return ", ".join([t.name for t in self.tags.order_by('name').all()])

    def get_version(self):
        return dict(VERSIONS)[self.version]

    def update_rating(self):
        self.rating_score = self.ratings.cumulative_score() or 0
        self.save()

    def update_bookmark_count(self):
        self.bookmark_count = self.bookmarks.count() or 0
        self.save()


class SnippetFlag(models.Model):
    FLAG_SPAM = 1
    FLAG_INAPPROPRIATE = 2
    FLAG_CHOICES = (
        (FLAG_SPAM, 'Spam'),
        (FLAG_INAPPROPRIATE, 'Inappropriate'),
    )
    snippet = models.ForeignKey(Snippet, related_name='flags')
    user = models.ForeignKey(User)
    flag = models.IntegerField(choices=FLAG_CHOICES)

    def __unicode__(self):
        return '%s flagged as %s by %s' % (
            self.snippet.title,
            self.get_flag_display(),
            self.user.username,
        )

    def remove_and_ban(self):
        user = self.snippet.author
        user.set_unusable_password()
        user.is_active = False
        user.save()
        self.snippet.delete()


class Bookmark(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='bookmarks')
    user = models.ForeignKey(User, related_name='cab_bookmarks')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return "%s bookmarked by %s" % (self.snippet, self.user)

    def save(self, *args, **kwargs):
        super(Bookmark, self).save(*args, **kwargs)
        self.snippet.update_bookmark_count()

    def delete(self, *args, **kwargs):
        super(Bookmark, self).delete(*args, **kwargs)
        self.snippet.update_bookmark_count()


class SnippetModerator(SpamFighterModerator):
    # Regular options by Django's contributed CommentModerator
    email_notification = True

    # Spam fighter options:
    # Check with Akismet for spam
    akismet_check = True
    # If Akismet marks this message as spam, delete it instantly (False) or
    # add it the comment the moderation queue (True). Default is True.
    akismet_check_moderate = True
    # Do a keyword check
    keyword_check = True
    # If a keyword is found, delete it instantly (False) or add the comment to
    # the moderation queue (True). Default is False.
    keyword_check_moderate = True


moderator.register(Snippet, SnippetModerator)


from cab.listeners import start_listening
start_listening()
