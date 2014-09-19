from disqus.wxr_feed import ContribCommentsWxrFeed
from cab.models import Snippet
from cab.templatetags.safe_markup import safe_markdown


class SnippetWxrFeed(ContribCommentsWxrFeed):
    link = "/feeds/wxr/"
    description_template = 'feeds/snippet/description.html'

    def items(self):
        return Snippet.objects.all()

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.title

    def comment_comment(self, comment):
        comment = super(SnippetWxrFeed, self).comment_comment(comment)
        return safe_markdown(comment, 'safe')
