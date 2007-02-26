"""
Models for code snippets and related data.

Most of these models also have custom managers defined which add
convenient shortcuts for repetitive or common bits of logic; see
``managers.py`` in this directory.

"""

import datetime
from django.db import connection, models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import managers
from markdown import markdown
from pygments import highlight, lexers, formatters


RATING_CHOICES = (
    (-1, 'Not useful'),
    (1, 'Useful')
    )


class Language(models.Model):
    """
    A language in which a Snippet can be written.
    
    The ``language_code`` field should be set to an alias of a
    Pygments lexer which is capable of processing this language.
    
    The ``file_extension`` and ``mime_type`` fields will be used when
    users download Snippets, to set the filename and HTTP Content-Type
    of the download appropriately.
    
    """
    name = models.CharField(maxlength=50)
    slug = models.SlugField(editable=False)
    language_code = models.CharField(maxlength=50,
                                     help_text="This should be an alias of a Pygments lexer which can handle this language.")
    file_extension = models.CharField(maxlength=10,
                                      help_text="The file extension to use when downloading Snippets in this Language; leave out the dot.")
    mime_type = models.CharField(maxlength=100,
                                 help_text="The HTTP Content-Type to use when downloading Snippets in this Language.")
    
    class Meta:
        ordering = ('name',)
    
    class Admin:
        fields = (
            ('Language information', {
            'fields': ('name', 'language_code')}),
            ('File type information', {
            'fields': ('file_extension', 'mime_type')}),
            )
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Language, self).save()
    
    def get_absolute_url(self):
        return "/languages/%s/" % self.slug
    
    def __str__(self):
        return self.name
    
    def get_lexer(self):
        """
        Returns an instance of the Pygments lexer for this language.
        
        """
        return lexers.get_lexer_by_name(self.language_code)


class Tag(models.Model):
    """
    A descriptive tag to be applied to a Snippet.
    
    """
    name = models.CharField(maxlength=50, unique=True)
    slug = models.SlugField(editable=False)
    
    class Meta:
        ordering = ('name',)
    
    class Admin:
        pass
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Tag, self).save()
    
    def get_absolute_url(self):
        return "/tags/%s/" % self.slug
    
    def __str__(self):
        return self.name


class Snippet(models.Model):
    """
    A snippet of code in some Language.
    
    This is slightly denormalized in two ways:
    
      1. Because it's wasteful to run Pygments over the code each time
         the Snippet is viewed, it is instead run on save, and two
         copies of the code -- one the original input, the other
         highlighted by Pygments -- are stored.
      
      2. For much the same reason, Markdown is run over the Snippet's
         description on save, instead of on each view, and the result
         is stored in a separate column.
    
    Also, Tags are added through the ``tag_list`` field which, after
    the Snippet has been saved, will be iterated over to set up the
    relationships to actual Tag objects.
    
    """
    
    title = models.CharField(maxlength=250)
    language = models.ForeignKey(Language)
    description = models.TextField(help_text="Accepts Markdown syntax.")
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    
    pub_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField(editable=False)
    
    author = models.ForeignKey(User, editable=False)
    tag_list = models.CharField(maxlength=250,
                                help_text="Separate tags with spaces. Maximum 250 characters.")
    tags = models.ManyToManyField(Tag, editable=False)
    original = models.ForeignKey('self', null=True, blank=True, editable=False,
                                 help_text="Optional. Fill this in if this Snippet is based on another.")
    
    objects = managers.SnippetsManager()
    
    class Meta:
        ordering = ('-pub_date',)
    
    class Admin:
        fields = (
            ('Metadata', {
            'fields': ('title', 'language', 'author', 'tag_list', 'original')}),
            ('None', {
             'fields': ('description', 'code')}),
            )
    
    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.description_html = markdown(self.description)
        self.highlighted_code = self.highlight()
        self.tag_list = self.tag_list.lower() # Normalize to lower-case
        super(Snippet, self).save()
        
        # Now that the Snippet is saved, deal with the tags.
        current_tags = list(self.tags.all()) # We only want to query this once.
        new_tag_list = self.tag_list.split()
        
        # First, clear out tags that aren't on the Snippet anymore.
        for tag in current_tags:
            if tag.name not in new_tag_list:
                self.tags.remove(tag)
        
        # Then add any new tags.
        for tag_name in new_tag_list:
            if tag_name not in [tag.name for tag in current_tags]:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.tags.add(tag)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/snippets/%s/" % self.id
    
    def highlight(self):
        """
        Returns this Snippet's originally-input code, highlighted via
        Pygments.
        
        """
        return highlight(self.code,
                         self.language.get_lexer(),
                         formatters.HtmlFormatter(linenos=True))


class Rating(models.Model):
    """
    A particular User's rating of a particular Snippet.
    
    """
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    date = models.DateTimeField(editable=False)
    score = models.IntegerField(choices=RATING_CHOICES)
    
    objects = managers.RatingsManager()
    
    class Admin:
        pass
    
    def save(self):
        if not self.id:
            self.date = datetime.datetime.now()
        super(Rating, self).save()
    
    def __str__(self):
        return "%s rating '%s'" % (self.user.username, self.snippet.title)


class Bookmark(models.Model):
    """
    A Snippet bookmarked by a User.
    
    """
    snippet = models.ForeignKey(Snippet)
    user = models.ForeignKey(User)
    date = models.DateTimeField(editable=False)
    
    objects = managers.BookmarksManager()
    
    class Meta:
        ordering = ('date',)
    
    class Admin:
        pass
    
    def save(self):
        if not self.id:
            self.date = datetime.datetime.now()
        super(Bookmark, self).save()
    
    def __str__(self):
        return "%s bookmarked by %s" % (self.snippet.title, self.user.username)
