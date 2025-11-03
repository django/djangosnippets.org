from django.test import RequestFactory, TestCase

from base.components.components import SortingTabs
from base.main import ObjectList

from .models import Fish


class FishList(ObjectList):
    sorting_tabs = {
        "newest": ("-id",),
        "oldest": ("id",),
        "high_price": ("-price",),
        "low_price": ("price",),
    }


class SortingTabsComponentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fish_data = [Fish(name=f"fish-{i}", price=i * 100) for i in range(1, 21)]
        cls.factory = RequestFactory()
        fishs = Fish.objects.bulk_create(fish_data)
        cls.queryset = Fish.objects.filter(pk__in=[f.pk for f in fishs])
        cls.components = SortingTabs()

    def test_create_tab_items(self):
        request = self.factory.get("?tab=high_price")
        object_list = FishList(request, Fish, self.queryset, 10)
        tab = self.components.create_tab(object_list, "newest")
        self.assertEqual(tab.text, "Newest")
        self.assertFalse(tab.is_current)
        self.assertEqual(tab.attrs, {"href": "?tab=newest"})

        tab = self.components.create_tab(object_list, "high_price")
        self.assertEqual(tab.text, "High Price")
        self.assertTrue(tab.is_current)
        self.assertEqual(tab.attrs, {"aria-selected": "true", "href": "?tab=high_price"})

    def test_create_all_tab_items(self):
        request = self.factory.get("")
        object_list = FishList(request, Fish, self.queryset, 10)
        tabs = self.components.create_all_tabs(object_list)
        self.assertEqual(len(tabs), 4)
        self.assertEqual(tabs[0].text, "Newest")
        self.assertEqual(tabs[1].text, "Oldest")
        self.assertEqual(tabs[2].text, "High Price")
        self.assertEqual(tabs[3].text, "Low Price")
