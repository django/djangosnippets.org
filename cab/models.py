import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count, Sum, permalink
from pygments import formatters, highlight, lexers
from markdown import markdown

from ratings.models import Ratings
from taggit.managers import TaggableManager


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
        return User.objects.annotate(score=Count('snippet')).order_by('-score')
    
    def top_tags(self):
        return self.model.tags.most_common().order_by('-num_times', 'name')
    
    def top_rated(self):
        # this is slow
        # return self.annotate(score=Sum('ratings__score')).order_by('-score')
        return self.all().order_by('-rating_score')

    def most_bookmarked(self):
        # this is slow
        # self.annotate(score=Count('bookmarks')).order_by('-score')
        return self.all().order_by('-bookmark_count')

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
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    bookmark_count = models.IntegerField(default=0) # denormalized count
    rating_score = models.IntegerField(default=0) # denormaliazed score
    
    ratings = Ratings()
    tags = TaggableManager()
    
    objects = SnippetManager()
    
    class Meta:
        ordering = ('-pub_date',)
        
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description)
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
    
    def update_rating(self):
        self.rating_score = self.ratings.cumulative_score() or 0
        self.save()
    
    def update_bookmark_count(self):
        self.bookmark_count = self.bookmarks.count() or 0
        self.save()


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
