import pytest
from unittest.mock import patch, MagicMock
from backend.model.pipeline import Pipeline
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
import datetime
from uuid import uuid4
import pandas as pd

@pytest.fixture
def mock_crop() -> Crop:
    return Crop(
        name="Example crop",
        t_base=10,
        stages={
            "sowing": {"day": 111},
            "germination": {"day": 151},
            "tillering": {"day": 182},
            "heading": {"day": 243},
            "maturity": {"day": 304}
        }
    )

@pytest.fixture
def pipeline():
    return Pipeline()

# test initialising the pipeline
def test_init(pipeline):
    assert pipeline is not None


def test_load_model_data(pipeline):
    result: pd.DataFrame = pipeline.load_model_data("3f76f41f-f166-4248-a7bb-56acef104f7a")
    # returns model_data = pd.DataFrame(response.data) so check if it is a dataframe
    assert result is not None
    assert isinstance(result, pd.DataFrame)

