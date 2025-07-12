from django.core.paginator import InvalidPage, Paginator

from .exceptions import IncorectLookupParameter

PAGE_VAR = "page"


class Pagination:
    def __init__(
        self,
        request,
        model,
        queryset,
        list_per_page,
    ):
        self.model = model
        self.opts = model._meta
        self.queryset = queryset
        self.list_per_page = list_per_page
        try:
            # Get the current page from the query string.
            self.page_num = int(request.GET.get(PAGE_VAR, 1))
        except ValueError:
            self.page_num = 1
        self.params = dict(request.GET.lists())
        self.setup()

    @property
    def page_range(self):
        """
        Returns the full range of pages.
        """
        return self.paginator.get_elided_page_range(self.page_num) if self.multi_page else []

    def setup(self):
        paginator = Paginator(self.queryset, self.list_per_page)
        result_count = paginator.count
        # Determine use pagination.
        multi_page = result_count > self.list_per_page

        self.result_count = result_count
        self.multi_page = multi_page
        self.paginator = paginator
        self.page = paginator.get_page(self.page_num)

    def get_objects(self):
        if not self.multi_page:
            result_list = self.queryset._clone()
        else:
            try:
                result_list = self.paginator.page(self.page_num).object_list
            except InvalidPage:
                raise IncorectLookupParameter
        return result_list
