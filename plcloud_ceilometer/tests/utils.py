"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import os
import six
import fixtures
import testscenarios
import testtools
from oslo_serialization import jsonutils
from requests_mock.contrib import fixture as requests_mock_fixture

AUTH_URL = "http://localhost:5002/auth_url"
AUTH_URL_V1 = "http://localhost:5002/auth_url/v1.0"
AUTH_URL_V2 = "http://localhost:5002/auth_url/v2.0"


class TestCase(testtools.TestCase):
    TEST_REQUEST_BASE = {
        'verify': True,
    }

    def setUp(self):
        super(TestCase, self).setUp()
        if (os.environ.get('OS_STDOUT_CAPTURE') == 'True' or
                    os.environ.get('OS_STDOUT_CAPTURE') == '1'):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if (os.environ.get('OS_STDERR_CAPTURE') == 'True' or
                    os.environ.get('OS_STDERR_CAPTURE') == '1'):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        self.requests_mock = self.useFixture(requests_mock_fixture.Fixture())

    def assert_request_id(self, request_id_mixin, request_id_list):
        self.assertEqual(request_id_list, request_id_mixin.request_ids)


class FixturedTestCase(testscenarios.TestWithScenarios, TestCase):
    client_fixture_class = None
    data_fixture_class = None

    def setUp(self):
        super(FixturedTestCase, self).setUp()

        self.data_fixture = None
        self.client_fixture = None
        self.cs = None

        if self.client_fixture_class:
            fix = self.client_fixture_class(self.requests_mock)
            self.client_fixture = self.useFixture(fix)
            self.cs = self.client_fixture.client

        if self.data_fixture_class:
            fix = self.data_fixture_class(self.requests_mock)
            self.data_fixture = self.useFixture(fix)

    def assert_called(self, method, path, body=None):
        self.assertEqual(self.requests_mock.last_request.method, method)
        self.assertEqual(self.requests_mock.last_request.path_url, path)

        if body:
            req_data = self.requests_mock.last_request.body
            if isinstance(req_data, six.binary_type):
                req_data = req_data.decode('utf-8')
            if not isinstance(body, six.string_types):
                # json load if the input body to match against is not a string
                req_data = jsonutils.loads(req_data)
            self.assertEqual(req_data, body)
