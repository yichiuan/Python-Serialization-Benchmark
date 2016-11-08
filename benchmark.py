import pytest

import json
import ujson
import rapidjson
import simplejson
import msgpack


@pytest.fixture(scope='module')
def data():
    return ['foo', {'bar': ('baz', None, 1.0, 2)}]


# json
@pytest.fixture(scope='module')
def load_data_json(data):
    return json.dumps(data)


# msgpack
@pytest.fixture(scope='module')
def msgpack_load_data(data):
    return msgpack.packb(data, use_bin_type=True)

# protocol buffer
from message import mydata_pb2

@pytest.fixture(scope='module')
def person_pb():
    person = mydata_pb2.Person()
    person.name = 'foo'

    person.phone.number.append('12345')
    person.phone.number.append('4567')
    person.phone.number.append('7564')
    person.phone.number.append('98787')
    return person


@pytest.fixture(scope='module')
def person_serial(person_pb):
    return person_pb.SerializeToString()


@pytest.fixture(scope='module')
def person2_pb():
    return mydata_pb2.Person()

# pyrobuf
from mydata_proto import Person

@pytest.fixture(scope='module')
def person_pr():
    person = Person()
    person.name = 'foo'

    person.phone.number.append('12345')
    person.phone.number.append('4567')
    person.phone.number.append('7564')
    person.phone.number.append('98787')
    return person


@pytest.fixture(scope='module')
def person_pr_serial(person_pr):
    return person_pr.SerializeToString()


@pytest.fixture(scope='module')
def person2_pr():
    return Person()


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


def test_protobuf_dump(benchmark, person_pb):
    benchmark.pedantic(person_pb.SerializeToString, iterations=10, rounds=rounds)
    assert True


def test_protobuf_load(benchmark, person2_pb, person_serial):
    benchmark.pedantic(person2_pb.ParseFromString, args=(person_serial, ), iterations=10, rounds=rounds)
    assert True


def test_pyrobuf_dump(benchmark, person_pr):
    benchmark.pedantic(person_pr.SerializeToString, iterations=10, rounds=rounds)
    assert True


def test_pyrobuf_load(benchmark, person2_pr, person_pr_serial):
    benchmark.pedantic(person2_pr.ParseFromString, args=(person_pr_serial, ), iterations=10, rounds=rounds)
    assert True
