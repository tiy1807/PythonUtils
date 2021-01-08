import mock
import pytest
from PythonUtils.option import Option
from PythonUtils.record_expenditure import ExpenditureRecord
from PythonUtils.storer import Store
from PythonUtils.petrol_record import PetrolRecord
import json
import os
from pathlib import Path


parameters = ("test_record, expected_output",
    [
        (["01/01/2020", "3.00", "Example Shop", "Food"],
         {"date": "01/01/2020", "amount": "3.00", "where": "Example Shop", "type": "Food"}
         ),
        (["28/02/2019", "100.00", "Amazon", "Presents"],
         {"date": "28/02/2019", "amount": "100.00", "where": "Amazon", "type": "Presents"}
         )
    ])


@pytest.mark.parametrize(*parameters)
def test_read(test_record, expected_output):
    record = ExpenditureRecord(*test_record)
    assert(record.date == expected_output["date"])
    assert(record.amount == expected_output["amount"])
    assert(record.where == expected_output["where"])
    assert(record.type == expected_output["type"])


@pytest.mark.parametrize(*parameters)
def test_string(test_record, expected_output):
    record = ExpenditureRecord(*test_record)
    assert record.to_string() == ",".join(test_record)
