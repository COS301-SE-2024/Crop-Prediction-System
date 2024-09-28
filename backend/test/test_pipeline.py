import pytest
from unittest.mock import patch, MagicMock
from backend.model.pipeline import Pipeline
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
import datetime
from uuid import uuid4


@pytest.fixture
def pipeline():
    return Pipeline()

# test initialising the pipeline
def test_init(pipeline):
    assert pipeline is not None

def test_train_all(pipeline):
    result = pipeline.train_all()
    assert result is not None

# def test_load_data(pipeline):
#     result = pipeline.load_data()
#     assert result is not None

