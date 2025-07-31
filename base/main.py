from .pagination import PAGE_VAR, Pagination


class ObjectList:
    pagination_class = Pagination

    def __init__(self, request, model, queryset, list_per_page):
        self.model = model
        self.queryset = queryset
        self.list_per_page = list_per_page
        self.params = dict(request.GET.lists())
        if PAGE_VAR in self.params:
            del self.params[PAGE_VAR]
        self.result_objects = self.get_objects(request)

    def __iter__(self):
        return iter(self.result_objects)

    def paginate(self, request, queryset):
        pagination = self.pagination_class(
            request,
            self.model,
            queryset,
            self.list_per_page,
        )
        self.pagination = pagination
        return pagination.get_objects()

    def get_objects(self, request):
        paginate_result = self.paginate(request, self.queryset)
        return paginate_result
