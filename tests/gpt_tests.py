import pytest
from prefect import flow, task
from prefect.utilities.testing import prefect_test_harness

from gpt import get_current_time, check_website, find_owners, check_wikipedia, gpt

@pytest.mark.parametrize("website", ["https://www.google.com", "https://www.facebook.com"])
def test_gpt(website):
    with prefect_test_harness() as test_harness:
        flow_result = test_harness.run(gpt, websites=[website])

        assert flow_result.is_successful()

        for task_run in flow_result.task_runs:
            assert task_run.is_successful()

        for task_log in flow_result.task_runs.values():
            if task_log.task_id == "check_website":
                assert task_log.result == True
            if task_log.task_id == "find_owners":
                assert task_log.result is not None
            if task_log.task_id == "check_wikipedia":
                assert task_log.result == True
