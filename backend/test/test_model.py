import pytest
from backend.model.model import Model
from backend.definitions.crop import Crop
from backend.definitions.field import Field
from backend.database.supabaseInstance import supabaseInstance
from backend.database.supabaseFunctions import supabaseFunctions
import uuid

@pytest.fixture(scope="module")
def setup_field():
    # Create a test field
    field_id = str(uuid.uuid4())
    f = Field(
        field_id=field_id,
        field_area=[
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0],
            [0, 0]
        ],
        hectare=1,
        field_name="Test Field",
        crop_type="wheat",
        team_id="d8d64098-b290-4fd2-b810-cadb1fe213ea"
    )
    return f

@pytest.fixture(scope="module")
def setup_supabase():
    # Create Supabase client and functions instance
    sb = supabaseInstance().get_client()
    sf = supabaseFunctions()
    return sf

@pytest.fixture(scope="module")
def setup_model():
    # Create model instance
    return Model()

def test_create_and_get_crop(setup_field, setup_supabase):
    f = setup_field
    sf = setup_supabase
    
    # Upload a field
    sf.createField(f)
    
    # Get the crop
    c : Crop = sf.getCrop(f.crop_type)
    assert c.name == "wheat"
    assert c.t_base == 10
    assert c is not None

# def test_load_data(setup_field, setup_supabase, setup_model):
#     f = setup_field
#     sf = setup_supabase
#     m = setup_model

#     # Get the crop
#     c : Crop = sf.getCrop(f.crop_type)
#     assert c.name == "wheat"
#     assert c.t_base == 10
#     assert c is not None

#     result = m.load_data("038f59ee-e1f1-49d8-94c2-96c2ada5852f", c)
#     print(result)
#     assert result is not None
#     assert "error" not in result

def test_load_model_data(setup_field, setup_model):
    f = setup_field
    m = setup_model

    result = m.load_model_data(f.field_id)
    assert result is not None
    assert "error" not in result

def test_load_yields(setup_supabase, setup_model):
    sf = setup_supabase
    m = setup_model

    # Get the crop
    c : Crop = sf.getCrop("wheat")

    result = m.load_yields(c)
    assert result is not None
    assert "error" not in result

# def test_train(setup_field, setup_supabase, setup_model):
#     f = setup_field
#     sf = setup_supabase
#     m = setup_model

#     # Get the crop
#     c : Crop = sf.getCrop(f.crop_type)

#     result = m.train(f.field_id, c)
#     assert result is not None
#     assert "error" not in result
#     assert result["status"] == "Model trained successfully"
#     assert result["mse"] > 0
#     assert result["predictions"] is not None

# def test_predict(setup_field, setup_model):
#     f = setup_field
#     m = setup_model

#     result = m.predict(f.field_id, test=True)
#     assert result is not None
#     assert result > 0
