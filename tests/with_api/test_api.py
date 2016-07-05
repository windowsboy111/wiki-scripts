#! /usr/bin/env python3

from nose.tools import assert_equals, assert_false, raises
from nose.plugins.attrib import attr

from . import fixtures

from ws.core.api import LoginFailed

@attr(speed="slow")
class test_api:
    """
    Some basic sanity checks, intended mostly for detecting changes in the
    ArchWiki configuration.
    """

    # uncategorized categories on ArchWiki (should be only these all the time)
    uncat_cats = ["Category:Archive", "Category:DeveloperWiki", "Category:Languages", "Category:Maintenance", "Category:Sandbox"]

# TODO: not sure if this is such a good idea...
#    # test LoginFailed exception
#    @raises(LoginFailed)
#    def test_login_failed(self):
#        fixtures.api.login("wiki-scripts testing invalid user", "invalid password")

    def test_max_ids_per_query(self):
        assert_equals(fixtures.api.max_ids_per_query, 50)

    # testing on uncategorized categories (should contain only 5 items all the time)
    def test_query_continue(self):
        q = fixtures.api.query_continue(action="query", list="querypage", qppage="Uncategorizedcategories", qplimit=1)
        titles = []
        for chunk in q:
            titles += [i["title"] for i in chunk["querypage"]["results"]]
        assert_equals(titles, self.uncat_cats)

    def test_list(self):
        q = fixtures.api.list(list="querypage", qppage="Uncategorizedcategories", qplimit="max")
        titles = []
        for i in q:
            titles.append(i["title"])
        assert_equals(titles, self.uncat_cats)

    def test_generator(self):
        q = fixtures.api.generator(generator="querypage", gqppage="Uncategorizedcategories", gqplimit="max")
        titles = []
        for i in q:
            titles.append(i["title"])
        assert_equals(titles, self.uncat_cats)

    def test_resolve_redirects(self):
        pageids = [1216, 17719]
        expected = [
            {'from': 'ABS', 'to': 'Arch Build System'},
            {'from': 'Main Page', 'to': 'Main page'},
        ]
        assert_equals(fixtures.api.resolve_redirects(*pageids), expected)
