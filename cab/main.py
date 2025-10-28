from base.main import ObjectList


class SnippetList(ObjectList):
    sorting_tabs = {
        "newest": ("-pub_date",),
        "latest_updated": ("-updated_date",),
        "highest_rated": ("-rating_score",),
        "most_bookmarked": ("-bookmark_count",),
    }
