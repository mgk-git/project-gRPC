# Example protos

## Contents

- [helloworld.proto]
  - The simple example used in the overview.
- [route_guide.proto]
  - An example service described in detail in the tutorial.
  

## command to generate artifacts.
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. protos/service.proto