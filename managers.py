"""
Custom managers for most of the models; these add useful logic for
various custom filters and queries.

"""

from django.db import models


class BookmarksManager(models.Manager):
    """
    Custom manager for the Bookmark model.
    
    Adds shortcuts for some common related-object filters, retrieving
    the most-bookmarked Snippets, and the ability to quickly determine
    whether someone's bookmarked a particular Snippet.
    
    """
    def already_bookmarked(self, user_id, snippet_id):
        """
        Returns ``True`` if the given User has Bookmarked the given
        Snippet, ``False`` otherwise.
        
        """
        try:
            self.get(user__pk=user_id,
                     snippet__pk=snippet_id)
        except self.model.DoesNotExist:
            return False
        return True
    
    def distinct_list(self, object_type, username):
        """
        Returns a list of distinct objects related to a User's
        Bookmarks.
        
        Acceptable values for ``object_type`` are:
        
         * 'author' -- returns a list of all the authors of the User's
           Bookmarks.
         * 'language' -- returns a list of all Languages in the User's
           Bookmarks.
         * 'tag' -- returns a list of all Tags attached to the User's
           Bookmarks.
        
        """
        # We need all of these up-front so we can get the right DB
        # tables into the mapping dictionary.
        from django.contrib.auth.models import User
        from models import Language, Tag, Snippet
        
        # Looking up table names in ``_meta`` is slightly hackish and
        # completely undocumented, but also extremely handy and
        # completely foolproof.
        object_mapping = {
            'author': { 'model': User,
                        'related_table': Snippet._meta.db_table,
                        'distinct_col': 'author_id',
                        'related_col': 'id' },
            'language': { 'model': Language,
                          'related_table': Snippet._meta.db_table,
                          'distinct_col': 'language_id',
                          'related_col': 'id' },
            'tag': {'model': Tag,
                    'related_table': Snippet._meta.get_field('tags').m2m_db_table(),
                    'distinct_col': 'tag_id',
                    'related_col': 'snippet_id' }
            }
        params = object_mapping[object_type]
        user = User.objects.get(username__exact=username)
        bookmark_table = self.model._meta.db_table # We need this repeatedly.
        
        from django.db import connection
        cursor = connection.cursor()
        query = """SELECT DISTINCT(%s.%s)
        FROM %s
        INNER JOIN %s
        ON %s.snippet_id = %s.%s
        WHERE %s.user_id = %%s""" % (params['related_table'], params['distinct_col'],
                                    bookmark_table, params['related_table'],
                                    bookmark_table, params['related_table'],
                                    params['related_col'], bookmark_table)
        cursor.execute(query, [user.id])
        
        # Use an ``id__in`` lookup instead of ``in_bulk`` because this gets us
        # a QuerySet we can pass to generic views.
        return params['model']._default_manager.filter(id__in=[row[0] for row in cursor.fetchall()])
    
    def get_by_author(self, username, author_username):
        """
        Returns all of a User's Bookmarks written by a particular author.
        
        """
        return self.get_for_user(username).filter(snippet__author__username__exact=author_username)
    
    def get_by_language(self, username, language_slug):
        """
        Returns all of a User's Bookmarks for a particular Language.
        
        """
        return self.get_for_user(username).filter(snippet__language__slug__exact=language_slug)
    
    def get_by_tag(self, username, tag_slug):
        """
        Returns all of a User's Bookmarks which have a particular
        Tag.
        
        """
        return self.get_for_user(username).filter(snippet__tags__slug__exact=tag_slug)
    
    def get_for_user(self, username):
        """
        Returns a particular User's Bookmarks.
        
        """
        return self.filter(user__username__exact=username)
    
    def most_bookmarked(self, num=5):
        """
        Returns the ``num`` most-bookmarked Snippets.
        
        """
        from models import Snippet
        query = """SELECT snippet_id, COUNT(*) AS score
        FROM %s
        GROUP BY snippet_id
        ORDER BY score DESC""" % self.model._meta.db_table
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [])
        snippet_ids = [row[0] for row in cursor.fetchall()]
        snippet_dict = Snippet.objects.in_bulk(snippet_ids)
        return [snippet_dict[snippet_id] for snippet_id in snippet_ids]


class RatingsManager(models.Manager):
    """
    Custom manager for the Rating model.

    Adds shortcuts for fetching aggregate data on a given Snippet,
    lists of top-rated Snippets, and for quickly determining whether
    someone's already rated a given Snippet.
    
    """
    def already_rated(self, user_id, snippet_id):
        """
        Determines whether a User has already rated a given Snippet.
        
        """
        try:
            rating = self.get(user__pk=user_id, snippet__pk=snippet_id)
        except self.model.DoesNotExist:
            return False
        return True
    
    def ratings_for_snippet(self, snippet_id):
        """
        Returns all Ratings for a given Snippet.
        
        """
        return self.filter(snippet__pk=snippet.id)
    
    def score_for_snippet(self, snippet_id):
        """
        Returns the current rating score for a Snippet as a dictionary
        with the following keys:
        
            score
                The total score.
            num_ratings
                The number of ratings so far.
        
        """
        query = """SELECT SUM(score), COUNT(*)
        FROM %s
        WHERE snippet_id=%%s""" % self.model._meta.db_table
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [snippet_id])
        result = cursor.fetchall()[0]
        return { 'score': result[0], 'num_ratings': result[1] }
    
    def top_rated(self, num=5):
        """
        Returns the top ``num`` Snippets with net positive ratings, in
        order of their total rating score.
        
        """
        from models import Snippet
        query = """SELECT snippet_id, SUM(score) AS rating
        FROM %s
        GROUP BY snippet_id
        ORDER BY rating DESC""" % self.model._meta.db_table
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [])
        # We only want Snippets with positive scores!
        snippet_ids = [row[0] for row in cursor.fetchall() if row[1] > 0]
        snippet_dict = Snippet.objects.in_bulk(snippet_ids)
        return [snippet_dict[snippet_id] for snippet_id in snippet_ids]


class SnippetsManager(models.Manager):
    """
    Custom manager for the Snippet model.
    
    Adds shortcuts for common filtering operations, and for retrieving
    popular related objects.
    
    """
    def get_by_author(self, username):
        """
        Returns a QuerySet of Snippets submitted by a particular User.
        
        """
        return self.filter(author__username__exact=username)
    
    def get_by_language(self, language_slug):
        """
        Returns a QuerySet of Snippets written in a particular
        Language.
        
        """
        return self.filter(language__slug__exact=language_slug)
    
    def get_by_tag(self, tag_slug):
        """
        Returns a QuerySet of Snippets which have a particular Tag.
        
        """
        return self.filter(tags__slug__exact=tag_slug)
    
    def top_items(self, item_type, num=5):
        """
        Returns a list of the top ``num`` objects of a particular
        type, based on the number of Snippets associated with them;
        for example, with ``item_type=tag``, returns a list of Tags
        based on how many Snippets they've been used for.
        
        Acceptable values for ``item_type`` are:
        
         * 'author' -- will return the users who have submitted the
           most Snippets.
         * 'language' -- will return the most-used languages.
         * 'tag' -- will return the most-used tags.
        
        """
        # Need all of these up-front so the mapping dictionary can be built
        # correctly.
        from django.contrib.auth.models import User
        from models import Language, Tag, Snippet
        
        # ``_meta`` strikes again.
        object_mapping = {
            'author': {'model': User,
                       'primary_table': User._meta.db_table,
                       'secondary_table': Snippet._meta.db_table },
            'tag': { 'model': Tag,
                     'primary_table': Tag._meta.db_table,
                     'secondary_table': Snippet._meta.get_field('tags').m2m_db_table() },
            'language': {'model': Language,
                         'primary_table': Language._meta.db_table,
                         'secondary_table': Snippet._meta.db_table },
            }
        
        params = object_mapping[item_type]
        query = """SELECT p.id AS object_id, COUNT(*) AS score
        FROM %s p INNER JOIN %s s
        ON p.id = s.%s
        GROUP BY object_id
        ORDER BY score DESC""" % (params['primary_table'], params['secondary_table'], item_type + '_id')
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [])
        object_ids = [row[0] for row in cursor.fetchall()[:num]]
        
        # Use ``in_bulk`` here instead of an ``id__in`` lookup, because ``id__in``
        # would clobber the ordering.
        object_dict = params['model']._default_manager.in_bulk(object_ids)
        return [object_dict[object_id] for object_id in object_ids]
