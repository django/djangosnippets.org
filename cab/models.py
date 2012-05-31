import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count, Sum, permalink

from ratings.models import Ratings
from taggit.managers import TaggableManager

from markdown import markdown
from pygments import formatters, highlight, lexers


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
        return User.objects.annotate(score=Count('snippet')).order_by('-score', 'username')

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

DJANGO_VERSIONS = (
    (1.4, '1.4'),
    (1.3, '1.3'),
    (1.2, '1.2'),
    (1.1, '1.1'),
    (1, '1.0'),
    (.96, '.96'),
    (.95, 'Pre .96'),
    (0, 'Not specified'),
)

VERSION_MAPPING = (
    (1.4, datetime.datetime(2012, 3, 23)),
    (1.3, datetime.datetime(2011, 3, 23)),
    (1.2, datetime.datetime(2010, 5, 17)),
    (1.1, datetime.datetime(2009, 7, 29)),
    (1.0, datetime.datetime(2008, 9, 3)),
    (.96, datetime.datetime(2007, 3, 23)),
    (.95, datetime.datetime(2000, 1, 1)),
)


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language)
    author = models.ForeignKey(User)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    django_version = models.FloatField(choices=DJANGO_VERSIONS, default=0)
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
        return ", ".join([t.name for t in self.tags.all()])

    def get_version(self):
        return dict(DJANGO_VERSIONS)[self.django_version]

    def update_rating(self):
        self.rating_score = self.ratings.cumulative_score() or 0
        self.save()

    def update_bookmark_count(self):
        self.bookmark_count = self.bookmarks.count() or 0
        self.save()


SNIPPET_FLAG_SPAM = 1
SNIPPET_FLAG_INAPPROPRIATE = 2
SNIPPET_FLAG_CHOICES = (
    (SNIPPET_FLAG_SPAM, 'Spam'),
    (SNIPPET_FLAG_INAPPROPRIATE, 'Inappropriate'),
)


class SnippetFlag(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='flags')
    user = models.ForeignKey(User)
    flag = models.IntegerField(choices=SNIPPET_FLAG_CHOICES)

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

from cab.listeners import start_listening
start_listening()
