from math import sqrt

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FullResultSet
from django.db import connection


def is_gfk(content_field):
    return isinstance(content_field, GenericForeignKey)


def query_has_where(query):
    try:
        where, _ = query.get_compiler(using="default").compile(query.where)
        return bool(where)
    except FullResultSet:
        return False


def query_as_sql(query):
    return query.get_compiler(connection=connection).as_sql()


def sim_euclidean_distance(ratings_queryset, factor_a, factor_b):
    rating_model = ratings_queryset.model

    if isinstance(factor_a, User):
        filter_field = "user_id"
        match_on = "hashed"
        lookup_a = factor_a.pk
        lookup_b = factor_b.pk
    else:
        filter_field = "hashed"
        match_on = "user_id"
        lookup_a = rating_model(content_object=factor_a).generate_hash()
        lookup_b = rating_model(content_object=factor_b).generate_hash()

    sql = """
    SELECT r1.score - r2.score AS diff
    FROM
        %(ratings_table)s AS r1
    INNER JOIN
        %(ratings_table)s AS r2
    ON r1.%(match_on)s = r2.%(match_on)s
    WHERE
        r1.%(filter_field)s = '%(lookup_a)s' AND
        r2.%(filter_field)s = '%(lookup_b)s'
        %(queryset_filter)s
    """

    rating_query = ratings_queryset.values_list("pk").query
    if query_has_where(rating_query):
        queryset_filter = ""
    else:
        q, p = query_as_sql(rating_query)
        rating_qs_sql = q % p
        queryset_filter = f" AND r1.id IN ({rating_qs_sql})"

    params = {
        "ratings_table": rating_model._meta.db_table,
        "filter_field": filter_field,
        "match_on": match_on,
        "lookup_a": lookup_a,
        "lookup_b": lookup_b,
        "queryset_filter": queryset_filter,
    }

    cursor = connection.cursor()
    cursor.execute(sql % params)

    sum_of_squares = 0
    while True:
        result = cursor.fetchone()
        if result is None:
            break
        sum_of_squares += result[0] ** 2

    return 1 / (1 + sum_of_squares)


def sim_pearson_correlation(ratings_queryset, factor_a, factor_b):
    rating_model = ratings_queryset.model

    if isinstance(factor_a, User):
        filter_field = "user_id"
        match_on = "hashed"
        lookup_a = factor_a.pk
        lookup_b = factor_b.pk
    else:
        filter_field = "hashed"
        match_on = "user_id"
        lookup_a = rating_model(content_object=factor_a).generate_hash()
        lookup_b = rating_model(content_object=factor_b).generate_hash()

    sql = """
    SELECT
        SUM(r1.score) AS r1_sum,
        SUM(r2.score) AS r2_sum,
        SUM(r1.score*r1.score) AS r1_square_sum,
        SUM(r2.score*r2.score) AS r2_square_sum,
        SUM(r1.score*r2.score) AS p_sum,
        COUNT(r1.id) AS sample_size
    FROM
        %(ratings_table)s AS r1
    INNER JOIN
        %(ratings_table)s AS r2
    ON r1.%(match_on)s = r2.%(match_on)s
    WHERE
        r1.%(filter_field)s = '%(lookup_a)s' AND
        r2.%(filter_field)s = '%(lookup_b)s'
        %(queryset_filter)s
    """

    rating_query = ratings_queryset.values_list("pk").query
    if query_has_where(rating_query):
        queryset_filter = ""
    else:
        q, p = query_as_sql(rating_query)
        rating_qs_sql = q % p
        queryset_filter = f" AND r1.id IN ({rating_qs_sql})"

    params = {
        "ratings_table": rating_model._meta.db_table,
        "filter_field": filter_field,
        "match_on": match_on,
        "lookup_a": lookup_a,
        "lookup_b": lookup_b,
        "queryset_filter": queryset_filter,
    }

    cursor = connection.cursor()
    cursor.execute(sql % params)

    result = cursor.fetchone()

    if not result:
        return 0

    sum1, sum2, sum1_sq, sum2_sq, psum, sample_size = result

    if sum1 is None or sum2 is None or sample_size == 0:
        return 0

    num = psum - (sum1 * sum2 / sample_size)
    den = sqrt((sum1_sq - pow(sum1, 2) / sample_size) * (sum2_sq - pow(sum2, 2) / sample_size))

    if den == 0:
        return 0

    return num / den


def top_matches(ratings_queryset, items, item, n=5, similarity=sim_pearson_correlation):
    scores = [
        (similarity(ratings_queryset, item, other), other) for other in items if other != item
    ]
    scores.sort()
    scores.reverse()
    return scores[:n]


def recommendations(ratings_queryset, people, person, similarity=sim_pearson_correlation):
    already_rated = ratings_queryset.filter(user=person).values_list("hashed")

    totals = {}
    sim_sums = {}

    for other in people:
        if other == person:
            continue

        sim = similarity(ratings_queryset, person, other)

        if sim <= 0:
            continue

        items = ratings_queryset.filter(user=other).exclude(hashed__in=already_rated)

        # now, score the items person hasn't rated yet
        for item in items:
            totals.setdefault(item.content_object, 0)
            totals[item.content_object] += item.score * sim

            sim_sums.setdefault(item.content_object, 0)
            sim_sums[item.content_object] += sim

    rankings = [(total / sim_sums[pk], pk) for pk, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def calculate_similar_items(ratings_queryset, num=10):
    # get distinct items from the ratings queryset - this can be optimized
    field = ratings_queryset.model._meta.get_field("content_object")

    if is_gfk(field):
        rated_ctypes = ratings_queryset.values_list("content_type", flat=True).distinct()
        ctypes = ContentType.objects.filter(pk__in=rated_ctypes)
        for ctype in ctypes:
            ratings_subset = ratings_queryset.filter(content_type=ctype)
            rating_ids = ratings_subset.values_list("object_id")
            model_class = ctype.model_class()
            queryset = model_class._default_manager.filter(pk__in=rating_ids)
            _store_top_matches(ratings_queryset, queryset, num, True)
    else:
        rated_model = field.rel.to
        rating_ids = ratings_queryset.values_list("content_object__pk")
        queryset = rated_model._default_manager.filter(pk__in=rating_ids)
        _store_top_matches(ratings_queryset, queryset, num, False)


def _store_top_matches(ratings_queryset, rated_queryset, num, is_gfk):
    from ratings.models import SimilarItem

    ctype = ContentType.objects.get_for_model(rated_queryset.model)
    rated_queryset.values_list("pk")  # fill cache

    for item in rated_queryset.iterator():
        matches = top_matches(ratings_queryset, rated_queryset, item, num)
        for score, match in matches:
            si, created = SimilarItem.objects.get_or_create(
                content_type=ctype,
                object_id=item.pk,
                similar_content_type=ContentType.objects.get_for_model(match),
                similar_object_id=match.pk,
            )
            if created or si.score != score:
                si.score = score
                si.save()


def recommended_items(ratings_queryset, user):
    from ratings.models import SimilarItem

    scores = {}
    total_sim = {}

    for item in ratings_queryset.filter(user=user):
        similar_items = SimilarItem.objects.get_for_item(item.content_object)
        for similar_item in similar_items:
            actual = similar_item.similar_object
            lookup_kwargs = ratings_queryset.model.lookup_kwargs(actual)
            lookup_kwargs["user"] = user

            if ratings_queryset.filter(**lookup_kwargs):
                continue

            scores.setdefault(actual, 0)
            scores[actual] += similar_item.score * item.score

            total_sim.setdefault(actual, 0)
            total_sim[actual] += similar_item.score

    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings
