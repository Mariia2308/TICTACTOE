import pytest
import os

STATSFILE_NAME = "pytest_stats.json"

def pytest_sessionfinish(session, exitstatus):
    if os.path.isfile(STATSFILE_NAME):
        os.remove(STATSFILE_NAME)

