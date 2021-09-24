from django.test import TestCase


class TestApiRouter(TestCase):
    def test_path_args(self):
        resp = self.client.get(
            "/intro/test_path_and_query_parameters", dict(arg1="abc", arg2="def")
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(
            "/intro/test_path_and_query_parameters/abc", dict(arg2="def")
        )
        resp_json = resp.json()
        self.assertEqual(resp_json["arg1"], "abc")
        self.assertEqual(resp_json["arg2"], "def")

    def test_query_args_with_schema(self):
        resp = self.client.get(
            "/intro/basic_check_on_path_or_query_parameter/abc",
            dict(arg1="abc", arg2="def"),
        )
        self.assertEqual(resp.status_code, 422)

        resp_json = self.client.get(
            "/intro/get_request_with_json_schema_query_args",
            dict(arg1="abc", arg2="5", arg3="1"),
        ).json()
        self.assertEqual(resp_json["arg1"], "abc")
        self.assertEqual(resp_json["arg2"], 5)
        self.assertEqual(resp_json["arg3"], True)
