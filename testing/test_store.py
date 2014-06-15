import os
import pytest
import json

from json_store import JSONStore
from json_store.store import CannotSerialize

@pytest.fixture
def store():
    return JSONStore()

@pytest.fixture
def append_data(store):
    data = {'a': 10}
    store.append(data)
    return store, data

def test_construction(tmpdir):
    j = JSONStore(name=tmpdir.join('store.json'))
    assert j.filename == tmpdir.join('store.json')

def test_default_construction(store):
    assert os.path.basename(store.filename) == 'store.json'

def test_read(tmpdir):
    data_file = tmpdir.join("store.json")
    data_file.write(json.dumps([{'a': 10}]))

    store = JSONStore(name=str(data_file))
    assert store.read() == [{'a': 10 }]

def test_read_blank_file(tmpdir):
    data_file = tmpdir.join("store.json")
    store = JSONStore(name=str(data_file))
    assert store.read() == []

def test_append_data(append_data):
    store, data = append_data
    with open(store.filename) as infile:
        assert json.load(infile) == [data]

def test_append_twice(append_data):
    store, data = append_data
    store.append({'b': 12})

    with open(store.filename) as infile:
        assert json.load(infile) == [
            {'a': 10},
            {'b': 12},
        ]

def test_to_string(store):
    assert str(store) == '<JSONStore fname:{0} contents:{1}>'.format(
        store.filename, store.read())

def test_bad_serialise(store):
    with pytest.raises(CannotSerialize) as err:
        store.append({'a': object()})

def test_append_with_kwargs(append_data):
    store, data = append_data
    store.append(b=15)
    assert store.read() == [
        {'a': 10},
        {'b': 15},
    ]
