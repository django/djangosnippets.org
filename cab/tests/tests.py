from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase

from cab.models import Snippet, Language, Bookmark
from ratings.models import RatedItem
from taggit.models import Tag, TaggedItem

class BaseCabTestCase(TestCase):
    urls = 'cab.tests.urls'
    
    def assertQSEqual(self, a, b):
        """
        Takes 2 lists/querysets/iterables, sorts them by pk, and checks for
        equality
        """
        self.assertEqual(sorted(list(a), key=lambda x: x.pk),
                         sorted(list(b), key=lambda x: x.pk))
    
    def setUp(self):
        """
        Because tags and ratings use GFKs which require content-type-ids, and
        as I am running 1.1.X at the moment, do all this stuff in the setUp()
        """
        self.user_a = User.objects.create_user('a', 'a', 'a')
        self.user_b = User.objects.create_user('b', 'b', 'b')
        
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

    def ensure_login_required(self, url, username, password):
        """
        A little shortcut that will hit a url, check for a login required
        redirect, then after logging in return the logged-in response
        """
        self.client.logout()
        
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/accounts/login/?next=%s' % url)
        
        self.client.login(username=username, password=password)
        
        resp = self.client.get(url)
        
        self.client.logout()
        return resp


class ManagerTestCase(BaseCabTestCase):
    """
    Tests covering manager methods -- currently most "popular" this or that
    are handled by managers.
    """
    
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
    """
    Tests to make sure that custom model signal handlers, denormalized fields,
    work as expected
    """
    def test_snippet_escaping(self):
        self.snippet1.description = '<script>alert("hacked");</script>'
        self.snippet1.save()
        self.assertEqual(self.snippet1.description_html, '<p>&lt;script&gt;alert(&quot;hacked&quot;);&lt;/script&gt;</p>')
    
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
        
        # update_bookmark_count() doesn't screw things up
        self.snippet1.update_bookmark_count()
        self.assertEqual(self.snippet1.bookmark_count, 2)
        
        self.assertEqual(self.snippet2.bookmark_count, 0)
        self.assertEqual(self.snippet3.bookmark_count, 1)
        
        # create a new bookmark and check that the count got updated
        b = Bookmark.objects.create(user=self.user_b, snippet=self.snippet2)
        self.snippet2 = Snippet.objects.get(pk=self.snippet2.pk) # refresh from the db
        self.assertEqual(self.snippet2.bookmark_count, 1)
    
        # delete a bookmark and check that the count got updated
        b.delete()
        self.snippet2 = Snippet.objects.get(pk=self.snippet2.pk) # refresh from the db
        self.assertEqual(self.snippet2.bookmark_count, 0)
    
    def test_snippet_description(self):
        # these may be pointless, but make sure things get marked-down on save
        self.assertEqual(self.snippet1.description_html, '<h1>A greeting</h1>')
        
        self.snippet1.description = '**Booyakasha**'
        self.snippet1.save()
        self.assertTrue('<strong>Booyakasha</strong>' in self.snippet1.description_html)
    
    def test_tag_string(self):
        # yes.  test a list comprehension
        self.assertEqual(self.snippet1.get_tagstring(), 'hello, world')
        self.assertEqual(self.snippet2.get_tagstring(), 'goodbye, world')
        self.assertEqual(self.snippet3.get_tagstring(), 'haxor')


class ViewTestCase(BaseCabTestCase):
    def test_bookmark_views(self):
        # gotta have it
        user_bookmarks = reverse('cab_user_bookmarks')
        self.assertEqual(user_bookmarks, '/bookmarks/')
        
        # test for the login-required bits
        resp = self.ensure_login_required(user_bookmarks, 'a', 'a')
        self.assertQSEqual(resp.context['object_list'], [self.bookmark1, self.bookmark3])
        
        resp = self.ensure_login_required(user_bookmarks, 'b', 'b')
        self.assertQSEqual(resp.context['object_list'], [self.bookmark2])
        
        add_bookmark = reverse('cab_bookmark_add', args=[self.snippet2.pk])
        self.assertEqual(add_bookmark, '/bookmarks/add/%d/' % self.snippet2.pk)
        
        # add a bookmark -- this does *not* require a POST for some reason so
        # this test will need to be amended when I get around to fixing this
        resp = self.ensure_login_required(add_bookmark, 'a', 'a')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/snippets/%d/' % self.snippet2.pk)
        
        new_bookmark = Bookmark.objects.get(user=self.user_a, snippet=self.snippet2)
        
        resp = self.ensure_login_required(user_bookmarks, 'a', 'a')
        self.assertQSEqual(resp.context['object_list'], [self.bookmark1, self.bookmark3, new_bookmark])
        
        # make sure we have to log in to delete a bookmark
        delete_bookmark = reverse('cab_bookmark_delete', args=[self.snippet2.pk])
        self.assertEqual(delete_bookmark, '/bookmarks/delete/%d/' % self.snippet2.pk)
        
        resp = self.ensure_login_required(delete_bookmark, 'a', 'a')
        
        # login and post to delete the bookmark
        self.client.login(username='a', password='a')
        resp = self.client.post(delete_bookmark)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/snippets/%d/' % self.snippet2.pk)
        
        # the bookmark is gone!
        self.assertRaises(Bookmark.DoesNotExist, Bookmark.objects.get, user=self.user_a, snippet=self.snippet2)
        
        # check the bookmark list view and make sure
        resp = self.ensure_login_required(user_bookmarks, 'a', 'a')
        self.assertQSEqual(resp.context['object_list'], [self.bookmark1, self.bookmark3])        
    
    def test_language_views(self):
        # where would we be without you
        language_url = reverse('cab_language_list')
        self.assertEqual(language_url, '/languages/')
        
        resp = self.client.get(language_url)
        self.assertEqual(resp.status_code, 200)
        self.assertQSEqual(resp.context['object_list'], [self.python, self.sql])
        
        language_detail = reverse('cab_language_detail', args=['python'])
        self.assertEqual(language_detail, '/languages/python/')
        
        resp = self.client.get(language_detail)
        self.assertEqual(resp.status_code, 200)
        self.assertQSEqual(resp.context['object_list'], [self.snippet1, self.snippet2])
        self.assertEqual(resp.context['language'], self.python)
    
    def test_popular_views(self):
        top_authors = reverse('cab_top_authors')
        self.assertEqual(top_authors, '/users/')
        
        resp = self.client.get(top_authors)
        self.assertEqual(resp.status_code, 200)
        user_a, user_b = resp.context['object_list']
        self.assertEqual(user_a, self.user_a)
        self.assertEqual(user_b, self.user_b)
        
        top_languages = reverse('cab_top_languages')
        self.assertEqual(top_languages, '/popular/languages/')
        
        resp = self.client.get(top_languages)
        self.assertEqual(resp.status_code, 200)
        python, sql = resp.context['object_list']
        self.assertEqual(python, self.python)
        self.assertEqual(sql, self.sql)
        
        top_tags = reverse('cab_top_tags')
        self.assertEqual(top_tags, '/tags/')
        
        resp = self.client.get(top_tags)
        self.assertEqual(resp.status_code, 200)
        tag_names = [tag.name for tag in resp.context['object_list']]
        self.assertEqual(tag_names, ['world', 'goodbye', 'haxor', 'hello'])
        
        top_bookmarked = reverse('cab_top_bookmarked')
        self.assertEqual(top_bookmarked, '/popular/bookmarked/')
        
        resp = self.client.get(top_bookmarked)
        self.assertEqual(resp.status_code, 200)
        s1, s3, s2 = resp.context['object_list']
        self.assertEqual(s1, self.snippet1)
        self.assertEqual(s3, self.snippet3)
        self.assertEqual(s2, self.snippet2)
        
        top_rated = reverse('cab_top_rated')
        self.assertEqual(top_rated, '/popular/rated/')
        
        resp = self.client.get(top_rated)
        self.assertEqual(resp.status_code, 200)
        s1, s3, s2 = resp.context['object_list']
        self.assertEqual(s1, self.snippet1)
        self.assertEqual(s3, self.snippet3)
        self.assertEqual(s2, self.snippet2)
    
    def test_tag_detail(self):
        tag_detail = reverse('cab_snippet_matches_tag', args=['world'])
        self.assertEqual(tag_detail, '/tags/world/')
        
        resp = self.client.get(tag_detail)
        self.assertEqual(resp.status_code, 200)
        self.assertQSEqual(resp.context['object_list'], [self.snippet1, self.snippet2])
    
    def test_author_detail(self):
        author_detail = reverse('cab_author_snippets', args=['a'])
        self.assertEqual(author_detail, '/users/a/')
        
        resp = self.client.get(author_detail)
        self.assertEqual(resp.status_code, 200)
        self.assertQSEqual(resp.context['object_list'], [self.snippet1, self.snippet3])

    def test_feeds(self):
        # I don't want to put much time into testing these since the response
        # is kind of fucked up.
        resp = self.client.get('/feeds/latest/')
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.get('/feeds/author/a/')
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.get('/feeds/author/c/')
        self.assertEqual(resp.status_code, 404)
        
        resp = self.client.get('/feeds/tag/world/')
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.get('/feeds/tag/nothing/')
        self.assertEqual(resp.status_code, 404)
        
        resp = self.client.get('/feeds/language/python/')
        self.assertEqual(resp.status_code, 200)
        
        resp = self.client.get('/feeds/language/java/')
        self.assertEqual(resp.status_code, 404)


class SnippetViewsTestCase(BaseCabTestCase):
    def test_index(self):
        snippet_index = reverse('cab_snippet_list')
        self.assertEqual(snippet_index, '/snippets/')
        
        resp = self.client.get(snippet_index)
        self.assertEqual(resp.status_code, 200)
        self.assertQSEqual(resp.context['object_list'], [self.snippet1, self.snippet2, self.snippet3])
    
    def test_snippet_detail(self):
        snippet_detail = reverse('cab_snippet_detail', args=[self.snippet1.pk])
        self.assertEqual(snippet_detail, '/snippets/%d/' % self.snippet1.pk)
        
        resp = self.client.get(snippet_detail)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object'], self.snippet1)
    
    def test_snippet_download(self):
        snippet_download = reverse('cab_snippet_download', args=[self.snippet1.pk])
        self.assertEqual(snippet_download, '/snippets/%d/download/' % self.snippet1.pk)
        
        resp = self.client.get(snippet_download)
        self.assertEqual(resp['content-type'], 'text/x-python')
        self.assertEqual(resp.content, 'print "Hello, world"')
    
    def test_snippet_rate(self):
        self.snippet1.ratings.clear()
        self.snippet1 = Snippet.objects.get(pk=self.snippet1.pk)
        self.assertEqual(self.snippet1.rating_score, 0)
        self.assertEqual(self.snippet1.ratings.count(), 0)
        
        snippet_rate = reverse('cab_snippet_rate', args=[self.snippet1.pk])
        self.assertEqual(snippet_rate, '/snippets/%d/rate/' % self.snippet1.pk)
        
        resp = self.client.get(snippet_rate + '?score=up')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('accounts/login' in resp['location'])
        
        self.client.login(username='a', password='a')
        resp = self.client.get(snippet_rate + '?score=NaN')
        self.assertEqual(self.snippet1.ratings.count(), 0)
        
        resp = self.client.get(snippet_rate + '?score=up')
        self.assertEqual(self.snippet1.ratings.count(), 1)
        self.assertEqual(self.snippet1.ratings.cumulative_score(), 1)
        
        resp = self.client.get(snippet_rate + '?score=down')
        self.assertEqual(self.snippet1.ratings.count(), 1)
        self.assertEqual(self.snippet1.ratings.cumulative_score(), -1)
    
    def test_snippet_edit(self):
        snippet_edit = reverse('cab_snippet_edit', args=[self.snippet1.pk])
        self.assertEqual(snippet_edit, '/snippets/%d/edit/' % self.snippet1.pk)
        
        resp = self.client.get(snippet_edit)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('accounts/login' in resp['location'])
        
        self.client.login(username='b', password='b')
        
        resp = self.client.get(snippet_edit)
        self.assertEqual(resp.status_code, 403)
        
        self.client.login(username='a', password='a')
        
        resp = self.client.get(snippet_edit)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form'].instance, self.snippet1)
        
        payload = {'title': 'Hi', 'django_version': '1.1', 'language': str(self.python.pk), 'description': 'wazzah\n======', 'code': 'print "Hi"', 'tags': 'hi, world'}
        resp = self.client.post(snippet_edit, payload)

        snippet1 = Snippet.objects.get(pk=self.snippet1.pk)
        self.assertEqual(snippet1.title, 'Hi')
        self.assertEqual(snippet1.description_html, '<h1>wazzah</h1>')
        self.assertEqual(snippet1.code, 'print "Hi"')
        self.assertEqual([t.name for t in snippet1.tags.all()], ['hi', 'world'])
        
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/snippets/%d/' % snippet1.pk)
    
    def test_snippet_add(self):
        snippet_add = reverse('cab_snippet_add')
        self.assertEqual(snippet_add, '/snippets/add/')
        
        resp = self.ensure_login_required(snippet_add, 'a', 'a')
        
        self.client.login(username='a', password='a')
        payload = {'title': 'Hi', 'django_version': '1.1', 'language': str(self.python.pk), 'description': 'wazzah\n======', 'code': 'print "Hi"', 'tags': 'hi, world'}
        resp = self.client.post(snippet_add, payload)

        new_snippet = Snippet.objects.get(title='Hi')
        self.assertEqual(new_snippet.title, 'Hi')
        self.assertEqual(new_snippet.description_html, '<h1>wazzah</h1>')
        self.assertEqual(new_snippet.code, 'print "Hi"')
        self.assertEqual([t.name for t in new_snippet.tags.all()], ['hi', 'world'])
        
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/snippets/%d/' % new_snippet.pk)


class TemplatetagTestCase(BaseCabTestCase):
    def test_cab_tags(self):
        t = Template("{% load cab_tags %}{% if snippet|is_bookmarked:user %}Y{% else %}N{% endif %}")
        c = Context({'snippet': self.snippet1, 'user': self.user_a})
        rendered = t.render(c)
        
        self.assertEqual(rendered, 'Y')
        
        Bookmark.objects.filter(user=self.user_a, snippet=self.snippet1).delete()
        
        rendered = t.render(c)
        self.assertEqual(rendered, 'N')
        
        c = Context({'snippet': self.snippet1, 'user': AnonymousUser()})
        rendered = t.render(c)
        self.assertEqual(rendered, 'N')
    
    def test_core_tags(self):
        t = Template('{% load core_tags %}{% for s in "cab.snippet"|latest:2 %}{{ s.title }}|{% endfor %}')
        rendered = t.render(Context({}))
        self.assertEqual(rendered, '%s|%s|' % (self.snippet3.title, self.snippet2.title))
        
        t = Template('{% load core_tags %}{% for t in "cab.snippet"|call_manager:"top_tags"|slice:":2" %}{{ t.name }}|{% endfor %}')
        rendered = t.render(Context({}))
        self.assertEqual(rendered, 'world|goodbye|')
