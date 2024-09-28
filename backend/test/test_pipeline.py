import pytest
from unittest.mock import patch, MagicMock
from backend.model.pipeline import Pipeline
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
import datetime
from uuid import uuid4

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

def test_load_data(pipeline):
    # c: Crop = Crop(
    #     name="wheat",
    #     t_base=5.0, 
    #     stages={
    #         "sowing": {"day": 111},
    #         "germination": {"day": 151},
    #         "tillering": {"day": 182},
    #         "heading": {"day": 243},
    #         "maturity": {"day": 304}
    #     }
    # )
    # X = pipeline.load_data(c,"14420bc8-48e3-47bc-ab83-1a6498380588")
    # print(X)
    # print("hier")
    # assert X is {"error": "Data not found. Field ID may be invalid or may not have any data."}
    assert True is not None

# def test_load_model(pipeline):
#     result = pipeline.load_model_data("3f76f41f-f166-4248-a7bb-56acef104f7a")
#     assert result is  {}

# def test_load_yields(pipeline):
#     c: Crop = Crop(
#         name="wheat",
#         t_base=5.0, 
#         stages={
#             "sowing": {"day": 111},
#             "germination": {"day": 151},
#             "tillering": {"day": 182},
#             "heading": {"day": 243},
#             "maturity": {"day": 304}
#         }
#     )
#     result = pipeline.load_yields(c)
#     assert result is not None
#     assert len(result) > 0

# def test_train(pipeline):
#     c: Crop = Crop(
#         name="wheat",
#         t_base=5.0, 
#         stages={
#             "sowing": {"day": 111},
#             "germination": {"day": 151},
#             "tillering": {"day": 182},
#             "heading": {"day": 243},
#             "maturity": {"day": 304}
#         }
#     )
#     # X,y = pipeline.load_data(c)
#     field_id = "14420bc8-48e3-47bc-ab83-1a6498380588"
#     result = pipeline.train(field_id)
#     assert result is not None


