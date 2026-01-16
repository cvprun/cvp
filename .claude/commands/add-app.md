# Add New CVP App

Add a new CVP Application Entrypoint.

## Parameters
- `$ARGUMENTS`: App name (e.g., `monitor`, `dashboard`)

## Instructions

Use the app name `$ARGUMENTS` provided by the user to perform the following steps.

### 1. Modify cvp/arguments.py

Follow the existing pattern to add:

```python
# Define constants (add near existing CMD_* definitions)
CMD_{NAME_UPPER}: Final[str] = "{name_lower}"
CMD_{NAME_UPPER}_HELP: Final[str] = "{description}"
CMD_{NAME_UPPER}_EPILOG = f"""
Simply usage:
  {PROG} {CMD_{NAME_UPPER}}
"""

# Add to CMDS tuple
CMDS: Final[Sequence[str]] = CMD_PLAYER, CMD_WORKER, CMD_AGENT, CMD_CLI, CMD_TESTER, CMD_{NAME_UPPER}

# Add parser function (near existing add_*_parser functions)
def add_{name_lower}_parser(subparsers) -> None:
    # noinspection SpellCheckingInspection
    parser = subparsers.add_parser(
        name=CMD_{NAME_UPPER},
        help=CMD_{NAME_UPPER}_HELP,
        formatter_class=RawDescriptionHelpFormatter,
        epilog=CMD_{NAME_UPPER}_EPILOG,
    )
    assert isinstance(parser, ArgumentParser)

# Add call inside default_argument_parser()
add_{name_lower}_parser(subparsers)
```

### 2. Create cvp/apps/{name_lower}/ directory

Create `cvp/apps/{name_lower}/__init__.py` file:

```python
# -*- coding: utf-8 -*-

from argparse import Namespace


def {name_lower}_main(args: Namespace) -> None:
    # TODO: Implement {name_lower} application
    raise NotImplementedError("{name_lower} app is not implemented yet")
```

### 3. Modify cvp/apps/__init__.py

```python
# Add import
from cvp.apps.{name_lower} import {name_lower}_main
from cvp.arguments import ..., CMD_{NAME_UPPER}

# Add to cmd_apps() dictionary
CMD_{NAME_UPPER}: {name_lower}_main,
```

## Checklist

- [ ] Add CMD constants to `cvp/arguments.py`
- [ ] Update CMDS tuple in `cvp/arguments.py`
- [ ] Add parser function to `cvp/arguments.py`
- [ ] Call parser in `default_argument_parser()` of `cvp/arguments.py`
- [ ] Create `cvp/apps/{name}/` directory
- [ ] Create `cvp/apps/{name}/__init__.py`
- [ ] Add import to `cvp/apps/__init__.py`
- [ ] Add entry to `cmd_apps()` dictionary in `cvp/apps/__init__.py`
