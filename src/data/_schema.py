# Copyright 2016 TensorLab. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

# _schema.py
# Implementation of Schema and related classes.

import enum
import yaml


class SchemaFieldType(enum.Enum):
  """Defines the types of SchemaField instances.
  """
  integer = 'integer'
  real = 'real'
  discrete = 'discrete'


class SchemaField(object):
  """Defines a named and typed field within a Schema.
  """
  def __init__(self, name, type, length):
    """Initializes a SchemaField with its name and type.

    Arguments:
      name: the name of the field.
      type: the type of the field.
      length: the valence of the field (0 implies variable length)
    """
    self._name = name
    self._type = type
    self._length = length

    # TODO: Add support for default values

  @classmethod
  def discrete(cls, name, length=1):
    """Creates a field representing a discrete value.

    Arguments:
      name: the name of the field.
      length: the valence of the field (0 implies variable length)
    """
    return cls(name, SchemaFieldType.discrete, length)

  @classmethod
  def integer(cls, name, length=1):
    """Creates a field representing an integer.

    Arguments:
      name: the name of the field.
      length: the valence of the field (0 implies variable length)
    """
    return cls(name, SchemaFieldType.integer, length)

  @classmethod
  def real(cls, name, length=1):
    """Creates a field representing a real number.

    Arguments:
      name: the name of the field.
      length: the valence of the field (0 implies variable length)
    """
    return cls(name, SchemaFieldType.real, length)

  @property
  def name(self):
    """Retrieves the name of the field.
    """
    return self._name

  @property
  def type(self):
    """Retrieves the type of the field.
    """
    return self._type

  @property
  def length(self):
    """Retrieves the length of the field.
    """
    return self._length

  @property
  def numeric(self):
    """Returns whether the field is a numeric type, i.e. integer or real.
    """
    return self._type in [SchemaFieldType.integer, SchemaFieldType.real]


class Schema(object):
  """Defines the schema of a DataSet.

  The schema represents the structure of the source data before it is transformed into features.
  """
  def __init__(self, fields):
    """Initializes a Schema with the specified set of fields.

    Arguments:
      fields: a list of fields representing an ordered set of columns.
    """
    if not len(fields):
      raise ValueError('One or more fields must be specified')

    self._fields = fields
    self._field_map = dict(map(lambda f: (f.name, f), fields))

  @staticmethod
  def create(*args):
    """Creates a Schema from a set of fields.

    Arguments:
      args: a list or sequence of ordered fields defining the schema.
    Returns:
      A Schema instance.
    """
    if not len(args):
      raise ValueError('One or more fields must be specified.')

    if type(args[0]) == list:
      return Schema(args[0])
    else:
      return Schema(list(args))

  def format(self):
    """Formats a Schema instance into its YAML specification.
    
    Returns:
      A string containing the YAML specification.
    """
    fields = map(lambda f: {'name': f.name, 'type': f.type.name, 'length': f.length},
                 self._fields)
    spec = {'fields': fields}

    return yaml.safe_dump(spec, default_flow_style=False)

  @staticmethod
  def parse(spec):
    """Parses a Schema from a YAML specification.

    Arguments:
      spec: The schema specification to parse.
    Returns:
      A Schema instance.
    """
    if isinstance(spec, Schema):
      return spec

    spec = yaml.safe_load(spec)
    fields = map(lambda f: SchemaField(f['name'], SchemaFieldType[f['type']], f.get('length', 1)),
                 spec['fields'])
    return Schema(fields)

  @property
  def fields(self):
    """Retrieve the names of the fields in the schema.
    """
    return map(lambda f: f.name, self._fields)

  def __getitem__(self, index):
    """Retrives the specified SchemaField by name or position.

    Arguments:
      index: the name or index of the field.
    Returns:
      The SchemaField if it exists; None otherwise.
    """
    if type(index) is int:
      return self._fields[index] if len(self._fields) > index else None
    else:
      return self._field_map.get(index, None)

  def __iter__(self):
    """Creates an iterator to iterate over the fields.
    """
    for field in self._fields:
      yield field

  def __len__(self):
    """Retrieves the number of SchemaFields defined.
    """
    return len(self._fields)
