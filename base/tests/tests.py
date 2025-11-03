from django.test import RequestFactory, TestCase

from base.main import ObjectList
from base.pagination import Pagination

from .models import Fish


class FishList(ObjectList):
    sorting_tabs = {
        "name_asc": ("name",),
        "high_price": ("-price",),
        "low_price": ("price",),
    }


class ObjectListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fishs = [
            Fish(name="Atlantic Salmon", price=80000),
            Fish(name="Bluefin Tuna", price=500000),
            Fish(name="Giant Squid", price=300000),
            Fish(name="King Crab", price=200000),
            Fish(name="Live Abalone", price=80000),
            Fish(name="Longtooth Grouper", price=250000),
            Fish(name="Red Seabream", price=90000),
            Fish(name="Tiger Prawn", price=70000),
            Fish(name="Wild Flatfish", price=180000),
            Fish(name="Yellow Corvina", price=150000),
        ]
        Fish.objects.bulk_create(fishs)
        cls.queryset = Fish.objects.all()
        cls.fish_list = list(cls.queryset)
        cls.factory = RequestFactory()

    def test_objects_paginate(self):
        request = self.factory.get("?page=2")
        object_list = ObjectList(request, Fish, self.queryset, 2)
        fish_names = [fish.name for fish in object_list]
        self.assertEqual(len(fish_names), 2)
        self.assertEqual(fish_names[0], "Giant Squid")
        self.assertEqual(fish_names[1], "King Crab")

        request = self.factory.get("?page=4")
        object_list = ObjectList(request, Fish, self.queryset, 3)
        fish_names = [fish.name for fish in object_list]
        self.assertEqual(len(fish_names), 1)
        self.assertEqual(fish_names[0], "Yellow Corvina")

    def test_select_default_tab(self):
        request = self.factory.get("")
        object_list = FishList(request, Fish, self.queryset, 5)
        self.assertEqual(object_list.base_ordering, ["name"])
        self.assertEqual(object_list.current_tab, "name_asc")

    def test_objects_tab_sorting(self):
        request = self.factory.get("?tab=high_price")
        object_list = FishList(request, Fish, self.queryset, 5)
        self.assertEqual(object_list.current_tab, "high_price")
        high_price_fishs = list(object_list)
        self.assertEqual(high_price_fishs[0].name, "Bluefin Tuna")
        self.assertEqual(high_price_fishs[1].name, "Giant Squid")
        self.assertEqual(high_price_fishs[2].name, "Longtooth Grouper")

        request = self.factory.get("?tab=low_price")
        object_list = FishList(request, Fish, self.queryset, 5)
        self.assertEqual(object_list.current_tab, "low_price")
        low_price_fishs = list(object_list)
        self.assertEqual(low_price_fishs[0].name, "Tiger Prawn")
        self.assertEqual(low_price_fishs[1].name, "Atlantic Salmon")
        self.assertEqual(low_price_fishs[2].name, "Live Abalone")


class PaginationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        fishs = [Fish(name=f"fish-{i}", price=i * 100) for i in range(1, 101)]
        Fish.objects.bulk_create(fishs)
        cls.queryset = Fish.objects.all()
        cls.factory = RequestFactory()

    def test_pagination_attributes(self):
        request = self.factory.get("/fake-url/")
        pagination = Pagination(request, Fish, self.queryset, 5)
        self.assertEqual(pagination.result_count, 100)
        self.assertTrue(pagination.multi_page)
        pagination = Pagination(request, Fish, self.queryset, 200)
        self.assertFalse(pagination.multi_page)

    def test_pagination_page_range(self):
        request = self.factory.get("/fake-url/")
        ellipsis = "…"
        case = [
            (2, 6, [1, 2, 3, 4, 5, 6, 7, 8, 9, ellipsis, 49, 50]),
            (3, 10, [1, 2, ellipsis, 7, 8, 9, 10, 11, 12, 13, ellipsis, 33, 34]),
            (4, 23, [1, 2, ellipsis, 20, 21, 22, 23, 24, 25]),
            (5, 20, [1, 2, ellipsis, 17, 18, 19, 20]),
            (10, 8, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            (20, 1, [1, 2, 3, 4, 5]),
        ]
        for list_per_page, current_page, expected_page_range in case:
            with self.subTest(list_per_page=list_per_page, current_page=current_page):
                pagination = Pagination(request, Fish, self.queryset, list_per_page)
                pagination.page_num = current_page
                self.assertEqual(list(pagination.page_range), expected_page_range)

    def test_pagination_result_objects(self):
        request = self.factory.get("/fake-url/")
        case = [
            (2, 25, ["49", "50"]),
            (4, 12, ["45", "46", "47", "48"]),
            (5, 10, ["46", "47", "48", "49", "50"]),
            (7, 11, ["71", "72", "73", "74", "75", "76", "77"]),
            (10, 10, ["91", "92", "93", "94", "95", "96", "97", "98", "99", "100"]),
            (200, 1, [str(i) for i in range(1, 101)]),
        ]
        Fish.objects.all().delete()
        fishs = [Fish(name=i, price=i * 100) for i in range(1, 101)]
        Fish.objects.bulk_create(fishs)
        queryset = Fish.objects.all().order_by("id")
        for list_per_page, current_page, expect_object_names in case:
            pagination = Pagination(request, Fish, queryset, list_per_page)
            pagination.page_num = current_page
            objects = pagination.get_objects()
            object_names = list(objects.values_list("name", flat=True))
            self.assertEqual(object_names, expect_object_names)
