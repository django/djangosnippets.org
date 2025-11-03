from .pagination import PAGE_VAR, Pagination

TAB_VAR = "tab"


class ObjectList:
    pagination_class = Pagination
    base_ordering = ()
    sorting_tabs = {}

    def __init__(self, request, model, queryset, list_per_page):
        self.model = model
        self.opts = model._meta
        self.queryset = queryset
        self.list_per_page = list_per_page
        self.params = dict(request.GET.dict())
        self.current_tab = self.params.get(TAB_VAR, None)
        if self.opts.ordering:
            self.base_ordering = list(self.opts.ordering)
        if PAGE_VAR in self.params:
            del self.params[PAGE_VAR]
        self.result_objects = self.get_objects(request, queryset)

    def __iter__(self):
        return iter(self.result_objects)

    def tab_sort(self, queryset):
        result_queryset = queryset
        if self.current_tab:
            sort_value = self.sorting_tabs[self.current_tab]
            result_queryset = result_queryset.order_by(*sort_value, *self.base_ordering)
        else:
            for tab_name, tab_order in self.sorting_tabs.items():
                if list(tab_order) == self.base_ordering:
                    self.current_tab = tab_name
                    break

        return result_queryset

    def paginate(self, request, queryset):
        pagination = self.pagination_class(
            request,
            self.model,
            queryset,
            self.list_per_page,
        )
        self.pagination = pagination
        return pagination.get_objects()

    def get_objects(self, request, queryset):
        tab_result = self.tab_sort(queryset)
        return self.paginate(request, tab_result)
