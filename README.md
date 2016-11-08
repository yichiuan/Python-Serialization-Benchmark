# Python Serialization Benchmark

## Install Protocol buffers

[protobuf](https://github.com/google/protobuf/tree/master/python)

## Build proto

`inv build_proto` for Protocol buffers
`inv build_pyrobuf` for pyrobuf

## Run

`pytest benchmark.py` small data
`pytest benchmark_big.py` bigger data
