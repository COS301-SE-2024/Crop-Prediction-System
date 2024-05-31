import unittest
from backend.app import sbGetFieldData, sbGetFieldInfo
import mock 
from backend.app import main

def test_test():
    assert main() == "Hello, World!"

if __name__ == "__main__":
    unittest.test_test()

# test if the sbGetFieldData returns the correct data
class mockedSupabaseClient:
    def rpc(self, rpcName):
        return {"data": [{"entry_id": 1, "created_at": "2024-05-18T08:59:17.944811+00:00","weather"}]}