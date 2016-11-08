import pytest

import json
import ujson
import rapidjson
import simplejson
import msgpack


@pytest.fixture(scope='module')
def data():
    p1 = {
        'name': 'John Doe',
        'id': 1234,
        'email': 'jdoe@example.com',
        'phone_numbers': [{'number': '555-4321', 'type': 2}, {'number': '777-4321', 'type': 1}]
    }

    return [p1, p1, p1]


@pytest.fixture(scope='module')
def load_data_json(data):
    return json.dumps(data)


@pytest.fixture(scope='module')
def msgpack_load_data(data):
    return msgpack.packb(data, use_bin_type=True)


# protocol buffer
from message import addressbook_pb2


def add_person_pb_to(addressbook_pb):
    person = addressbook_pb.person.add()
    person.id = 1234
    person.name = "John Doe"
    person.email = "jdoe@example.com"

    phone = person.phone.add()
    phone.number = "555-4321"
    phone.type = addressbook_pb2.HOME
    phone2 = person.phone.add()
    phone2.number = "555-4321"
    phone2.type = addressbook_pb2.HOME
    return person


@pytest.fixture(scope='module')
def addressbook_big_pb():
    addressbook_big_pb = addressbook_pb2.AddressBook()
    add_person_pb_to(addressbook_big_pb)
    add_person_pb_to(addressbook_big_pb)
    add_person_pb_to(addressbook_big_pb)
    return addressbook_big_pb


@pytest.fixture(scope='module')
def addressbook_big_pb_serialed(addressbook_big_pb):
    return addressbook_big_pb.SerializeToString()


@pytest.fixture(scope='module')
def addressbook2_big_pb():
    return addressbook_pb2.AddressBook()

# pyrobuf
from addressbook_proto import Person, AddressBook


@pytest.fixture(scope='module')
def addressbook_pr():
    addressbook_pr = AddressBook()
    add_person_pb_to(addressbook_pr)
    add_person_pb_to(addressbook_pr)
    add_person_pb_to(addressbook_pr)
    return addressbook_pr


@pytest.fixture(scope='module')
def addressbook_pr_seri(addressbook_pr):
    return addressbook_pr.SerializeToString()


@pytest.fixture(scope='module')
def addressbook2_pr():
    return AddressBook()


rounds = 200


def test_json_dump(benchmark, data):
    benchmark.pedantic(json.dumps, args=(data,), iterations=10, rounds=rounds)
    assert True


def test_json_load(benchmark, load_data_json):
    benchmark.pedantic(json.loads, args=(load_data_json,), iterations=10, rounds=rounds)
    assert True


def test_ujson_dump(benchmark, data):
    benchmark.pedantic(ujson.dumps, args=(data,), iterations=10, rounds=rounds)
    assert True


def test_ujson_load(benchmark, load_data_json):
    benchmark.pedantic(ujson.loads, args=(load_data_json,), iterations=10, rounds=rounds)
    assert True


def test_rapidjson_dump(benchmark, data):
    benchmark.pedantic(rapidjson.dumps, args=(data,), iterations=10, rounds=rounds)
    assert True


def test_rapidjson_load(benchmark, load_data_json):
    benchmark.pedantic(rapidjson.loads, args=(load_data_json,), iterations=10, rounds=rounds)
    assert True


def test_simplejson_dump(benchmark, data):
    benchmark.pedantic(simplejson.dumps, args=(data,), iterations=10, rounds=rounds)
    assert True


def test_simplejson_load(benchmark, load_data_json):
    benchmark.pedantic(simplejson.loads, args=(load_data_json,), iterations=10, rounds=rounds)
    assert True


def test_msgpack_dump(benchmark, data):
    benchmark.pedantic(msgpack.packb, args=(data,), kwargs={'use_bin_type': True}, iterations=10, rounds=rounds)
    assert True


def test_msgpack_load(benchmark, msgpack_load_data):
    benchmark.pedantic(msgpack.unpackb, args=(msgpack_load_data, ), kwargs={'use_list': False}, iterations=10, rounds=rounds)
    assert True


def test_protobuf_dump(benchmark, addressbook_big_pb):
    benchmark.pedantic(addressbook_big_pb.SerializeToString, iterations=10, rounds=rounds)
    assert True


def test_protobuf_load(benchmark, addressbook2_big_pb, addressbook_big_pb_serialed):
    benchmark.pedantic(addressbook2_big_pb.ParseFromString, args=(addressbook_big_pb_serialed, ), iterations=10, rounds=rounds)
    assert True


def test_pyrobuf_dump(benchmark, addressbook_pr):
    benchmark.pedantic(addressbook_pr.SerializeToString, iterations=10, rounds=rounds)
    assert True


def test_pyrobuf_load(benchmark, addressbook2_pr, addressbook_pr_seri):
    benchmark.pedantic(addressbook2_pr.ParseFromString, args=(addressbook_pr_seri, ), iterations=10, rounds=rounds)
    assert True
