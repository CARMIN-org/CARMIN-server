from server.test.resources.test_executions import test_config, number_of_executions, pipeline
from server.test.fakedata.users import standard_user
from server.test.utils import load_json_data
from server.test.conftest import test_client, session


class TestExecutionsCountResource():
    def test_get_0_executions(self, test_client):
        response = test_client.get(
            '/executions/count', headers={"apiKey": standard_user().api_key})
        json_response = load_json_data(response)
        assert json_response == 0

    def test_get_10_executions(self, test_client, number_of_executions):
        response = test_client.get(
            '/executions/count', headers={"apiKey": standard_user().api_key})
        json_response = load_json_data(response)
        assert json_response == number_of_executions
