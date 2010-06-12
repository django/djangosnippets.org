from django.contrib.auth.models import User
from django.test import TestCase

from cab.models import Snippet, Language, Bookmark
from ratings.models import RatedItem
from taggit.models import Tag, TaggedItem

class BaseCabTestCase(TestCase):
    def assertQuerysetEqual(self, a, b):
        self.assertEqual(sorted(list(a), key=lambda x: x.pk),
                         sorted(list(b), key=lambda x: x.pk))
    
    def setUp(self):
        self.user_a = User.objects.create(username='a')
        self.user_b = User.objects.create(username='b')
        
        self.python = Language.objects.create(
            name='Python',
            slug='python',
            language_code='python',
            mime_type='text/x-python',
            file_extension='py')
        
        self.sql = Language.objects.create(
            name='SQL',
            slug='sql',
            language_code='sql',
            mime_type='text/x-sql',
            file_extension='sql')
        
        self.snippet1 = Snippet.objects.create(
            title='Hello world',
            language=self.python,
            author=self.user_a,
            description='A greeting\n==========',
            code='print "Hello, world"')
        self.snippet1.tags.add('hello', 'world')
        
        self.snippet2 = Snippet.objects.create(
            title='Goodbye world',
            language=self.python,
            author=self.user_b,
            description='A farewell\n==========',
            code='print "Goodbye, world"')
        self.snippet2.tags.add('goodbye', 'world')
        
        self.snippet3 = Snippet.objects.create(
            title='One of these things is not like the others',
            language=self.sql,
            author=self.user_a,
            description='Haxor some1z db',
            code='DROP TABLE accounts;')
        self.snippet3.tags.add('haxor')
        
        self.bookmark1 = Bookmark.objects.create(snippet=self.snippet1, user=self.user_a)
        self.bookmark2 = Bookmark.objects.create(snippet=self.snippet1, user=self.user_b)
        self.bookmark3 = Bookmark.objects.create(snippet=self.snippet3, user=self.user_a)
        
        self.snippet1.ratings.rate(self.user_a, 1)
        self.snippet1.ratings.rate(self.user_b, 1)
        self.snippet2.ratings.rate(self.user_a, -1)
        self.snippet2.ratings.rate(self.user_b, -1)
        self.snippet3.ratings.rate(self.user_a, 1)
        self.snippet3.ratings.rate(self.user_b, -1)
        
        self.snippet1 = Snippet.objects.get(pk=self.snippet1.pk)
        self.snippet2 = Snippet.objects.get(pk=self.snippet2.pk)
        self.snippet3 = Snippet.objects.get(pk=self.snippet3.pk)


class ManagerTestCase(BaseCabTestCase):
    def test_top_languages(self):
        top_languages = Language.objects.top_languages()
        self.assertEqual(top_languages[0], self.python)
        self.assertEqual(top_languages[1], self.sql)
        
        self.assertEqual(top_languages[0].score, 2)
        self.assertEqual(top_languages[1].score, 1)
    
    def test_top_authors(self):
        top_authors = Snippet.objects.top_authors()
        self.assertEqual(top_authors[0], self.user_a)
        self.assertEqual(top_authors[1], self.user_b)
        
        self.assertEqual(top_authors[0].score, 2)
        self.assertEqual(top_authors[1].score, 1)
        
    def test_top_tags(self):
        top_tags = Snippet.objects.top_tags()
        self.assertEqual(top_tags[0].name, 'world')
        self.assertEqual(top_tags[0].num_times, 2)
        
        self.assertEqual(top_tags[1].name, 'goodbye')
        self.assertEqual(top_tags[2].name, 'haxor')
        self.assertEqual(top_tags[3].name, 'hello')
    
    def test_top_rated(self):
        top_rated = Snippet.objects.top_rated()
        self.assertEqual(top_rated[0], self.snippet1)
        self.assertEqual(top_rated[1], self.snippet3)
        self.assertEqual(top_rated[2], self.snippet2)
    
    def test_most_bookmarked(self):
        most_bookmarked = Snippet.objects.most_bookmarked()
        self.assertEqual(most_bookmarked[0], self.snippet1)
        self.assertEqual(most_bookmarked[1], self.snippet3)
        self.assertEqual(most_bookmarked[2], self.snippet2)


class ModelTestCase(BaseCabTestCase):
    def test_ratings_hooks(self):
        # setUp() will actually fire off most of these hooks
        self.assertEqual(self.snippet1.rating_score, 2)
        
        # calling the hooks manually doesn't affect the results
        self.snippet1.update_rating()
        self.assertEqual(self.snippet1.rating_score, 2)
        
        # check the other snippets
        self.assertEqual(self.snippet2.rating_score, -2)
        self.assertEqual(self.snippet3.rating_score, 0)
        
        self.snippet1.ratings.rate(self.user_a, -1)
        self.snippet1 = Snippet.objects.get(pk=self.snippet1.pk) # refresh from the db
        self.assertEqual(self.snippet1.rating_score, 0)
        
        self.snippet3.ratings.rate(self.user_a, -1)
        self.snippet3 = Snippet.objects.get(pk=self.snippet3.pk) # refresh from the db
        self.assertEqual(self.snippet3.rating_score, -2)
    
    def test_bookmark_hooks(self):
        self.assertEqual(self.snippet1.bookmark_count, 2)
        
        self.snippet1.update_bookmark_count()
        self.assertEqual(self.snippet1.bookmark_count, 2)
        
        self.assertEqual(self.snippet2.bookmark_count, 0)
        self.assertEqual(self.snippet3.bookmark_count, 1)
        
        b = Bookmark.objects.create(user=self.user_b, snippet=self.snippet2)
        self.snippet2 = Snippet.objects.get(pk=self.snippet2.pk) # refresh from the db
        self.assertEqual(self.snippet2.bookmark_count, 1)
    
        b.delete()
        self.snippet2 = Snippet.objects.get(pk=self.snippet2.pk) # refresh from the db
        self.assertEqual(self.snippet2.bookmark_count, 0)
    
    def test_snippet_description(self):
        self.assertEqual(self.snippet1.description_html, '<h1>A greeting</h1>')
        
        self.snippet1.description = '**Booyakasha**'
        self.snippet1.save()
        self.assertTrue('<strong>Booyakasha</strong>' in self.snippet1.description_html)
    
    def test_tag_string(self):
        self.assertEqual(self.snippet1.get_tagstring(), 'hello, world')
        self.assertEqual(self.snippet2.get_tagstring(), 'goodbye, world')
        self.assertEqual(self.snippet3.get_tagstring(), 'haxor')


class ViewTestCase(BaseCabTestCase):
    pass
