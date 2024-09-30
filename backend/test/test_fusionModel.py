import pytest
from unittest.mock import patch, MagicMock
from backend.model.FusionModel import FusionModel
from backend.definitions.entry import Entry
from backend.definitions.crop import Crop
import datetime
from uuid import uuid4


@pytest.fixture
def fusion_model():
    return FusionModel()


# def test_train(fusion_model):
#     result = fusion_model.train()
#     assert result is not None