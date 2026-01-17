# Add New CVP Node

Add a new Node to CVP flow graph system.

## Parameters
- `$ARGUMENTS`: `{category} {name}` format (e.g., `essential counter`, `casting datetime`)

## Instructions

Use the arguments `$ARGUMENTS` provided by the user to perform the following steps.

**Naming conventions:**
- `{category}` = snake_case category name (e.g., `essential`, `casting`, `operators`)
- `{name}` = snake_case node file name (e.g., `counter`, `datetime_casting`)
- `{Name}` = PascalCase class name (e.g., `Counter`, `DatetimeCasting`)

**Existing categories:**
- `essential` - Core nodes (Empty, Entrypoint, Getter, Setter, Logging)
- `casting` - Type casting nodes (Boolean, Floating, Integer, String)
- `operators` - Operator nodes
- `numpy` - NumPy operations
- `opencv` - OpenCV operations
- `pandas` - Pandas operations

### 1. Create Node File

Create `cvp/nodes/defaults/{category}/{name}.py`:

```python
# -*- coding: utf-8 -*-

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.pins.special import NextPin, PrevPin
from cvp.types.override import override


class {Name}(Node):
    """{Description of what this node does}"""

    def __init__(self):
        self._prev = PrevPin()
        self._next = NextPin()
        # Define input pins
        self._input = DataInputPin(
            name=PinName("input"),
            dtype=Dtype.any(),  # Or specific type: Dtype(int), Dtype(str), etc.
            docs="Input value",
            required=True,
        )
        # Define output pins
        self._output = DataOutputPin(
            name=PinName("output"),
            dtype=Dtype.any(),
            docs="Output value",
        )
        super().__init__(self._prev, self._next, self._input, self._output)

    @override
    def run(self, record: NodeRecord) -> Pin:
        # Get input values
        value = record.get(self._input)
        # Process and set output
        record.set(self._output, value)
        return self._next
```

### 2. Register Node in Category's `__init__.py`

Modify `cvp/nodes/defaults/{category}/__init__.py`:

#### 2.1 Add Import (in alphabetical order)

```python
from cvp.nodes.defaults.{category}.{name} import {Name}
```

#### 2.2 Add to `get_{category}_types()` Tuple

```python
@lru_cache
def get_{category}_types() -> Sequence[Type]:
    return (
        ...,
        {Name},  # Add in alphabetical order
        ...,
    )
```

### 3. (Optional) Create New Category

If the category doesn't exist, create a new one:

#### 3.1 Create Category Directory

```bash
mkdir -p cvp/nodes/defaults/{category}
```

#### 3.2 Create Category's `__init__.py`

Create `cvp/nodes/defaults/{category}/__init__.py`:

```python
# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.{category}.{name} import {Name}
from cvp.nodes.node import Node


@lru_cache
def get_{category}_types() -> Sequence[Type]:
    return (
        {Name},
    )


@lru_cache
def get_{category}_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_{category}_types())
```

#### 3.3 Register Category in `cvp/nodes/defaults/__init__.py`

Add import:
```python
from cvp.nodes.defaults.{category} import get_{category}_nodes
```

Add to `get_default_nodes()`:
```python
result.extend(get_{category}_nodes())
```

## Pin Types Reference

### Special Pins (Flow Control)
| Pin | Import | Description |
|-----|--------|-------------|
| `PrevPin` | `cvp.pins.special` | Execution input |
| `NextPin` | `cvp.pins.special` | Execution output |
| `ReturnPin` | `cvp.pins.special` | Return value output |

### Data Pins
| Pin | Import | Description |
|-----|--------|-------------|
| `DataInputPin` | `cvp.pins.datas` | Data input |
| `DataOutputPin` | `cvp.pins.datas` | Data output |

### DataInputPin Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `PinName` | Pin identifier |
| `dtype` | `Dtype` | Data type |
| `docs` | `str` | Documentation |
| `required` | `bool` | Is required (default: False) |
| `hidden` | `bool` | Hidden in UI (default: False) |
| `default` | `Any` | Default value (default: None) |

### Common Dtype Examples
```python
Dtype.any()      # Any type
Dtype(int)       # Integer
Dtype(float)     # Float
Dtype(str)       # String
Dtype(bool)      # Boolean
Dtype(list)      # List
Dtype(dict)      # Dictionary
```

## Node Templates

### Simple Processor (with flow)
```python
class {Name}(Node):
    """Process data with flow control"""

    def __init__(self):
        self._prev = PrevPin()
        self._next = NextPin()
        self._input = DataInputPin(...)
        self._output = DataOutputPin(...)
        super().__init__(self._prev, self._next, self._input, self._output)

    @override
    def run(self, record: NodeRecord) -> Pin:
        value = record.get(self._input)
        record.set(self._output, processed_value)
        return self._next
```

### Pure Function (no flow)
```python
class {Name}(Node):
    """Pure function without flow control"""

    def __init__(self):
        self._input = DataInputPin(...)
        self._return = ReturnPin(Dtype(result_type))
        super().__init__(self._input, self._return)

    @override
    def run(self, record: NodeRecord) -> Pin:
        value = record.get(self._input)
        record.set(self._return, result)
        return self.nonext()
```

### Casting Node (inheriting base)
```python
from cvp.nodes.defaults.casting._base import CastingNode


class {Name}Casting(CastingNode):
    """{Description}"""

    def __init__(self):
        super().__init__(target_type)  # e.g., int, float, str
```

## Checklist

- [ ] Create `cvp/nodes/defaults/{category}/{name}.py` with Node class
- [ ] Add import to `cvp/nodes/defaults/{category}/__init__.py`
- [ ] Add class to `get_{category}_types()` tuple
- [ ] (If new category) Create category directory
- [ ] (If new category) Create category's `__init__.py`
- [ ] (If new category) Register in `cvp/nodes/defaults/__init__.py`
- [ ] Implement `run()` method with node logic
- [ ] Add proper docstring to class

## Example Usage

```bash
# Add a Counter node to essential category
/add-node essential counter

# Add a DatetimeCasting node to casting category
/add-node casting datetime

# Add a node to a new category
/add-node math arithmetic
```
