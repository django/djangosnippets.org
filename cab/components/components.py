from django_components import Component, register
from pydantic import BaseModel

from base.main import ObjectList


@register("snippet_list")
class SnippetListComponent(Component):

    template_file = "snippet_list.html"

    class Kwargs(BaseModel):
        snippet_list: ObjectList
        model_config = {"arbitrary_types_allowed": True}

    def get_template_data(self, args, kwargs, slots, context):
        return {
            "snippet_list": kwargs.snippet_list.result_objects,
        }
