import pytest
from PythonUtils.storer import Store
from PythonUtils.record import Record

data = "data11,data12,data13,data14\ndata21,data22,data23,data24\n"

@pytest.fixture(autouse=True)
def example_store(tmp_path):
    p = tmp_path / "example_store.csv"
    with open(p, "w") as example_file:
        example_file.write(data)
    yield


def test_create_storer(tmp_path):
    p = tmp_path / "example_store.csv"
    store = Store(p, Record)
    assert True


def test_read(tmp_path):
    p = tmp_path / "example_store.csv"
    store = Store(p, Record)
    expected_record = Record("data11", "data12", "data13", "data14")
    assert store.read()[0] == expected_record


def test_write_new_record(tmp_path):
    p = tmp_path / "example_store.csv"
    store = Store(p, Record)
    store.write_new_record("data31", "data32", "data33", "data34")
    with open(p, "r") as outfile:
        assert outfile.readlines()[-1] == "data31,data32,data33,data34\n"
