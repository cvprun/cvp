# Add New CVP Player Mode

Add a new Mode to CVP Player application.

## Parameters
- `$ARGUMENTS`: Mode name in snake_case (e.g., `audio`, `network_scanner`)

## Instructions

Use the mode name `$ARGUMENTS` provided by the user to perform the following steps.

**Naming conventions:**
- `{name}` = snake_case (e.g., `audio`, `network_scanner`)
- `{Name}` = PascalCase (e.g., `Audio`, `NetworkScanner`)
- `{NAME}` = UPPER_CASE (e.g., `AUDIO`, `NETWORK_SCANNER`)

### 1. Create Mode Directory and File

Create `cvp/apps/player/modes/{name}/__init__.py`:

```python
# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import APPLICATION  # Choose appropriate icon
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.types.override import override


class {Name}Mode(BaseMode):
    __cvp_mode_name__ = "{Display Name}"  # User-visible name
    __cvp_mode_icon__ = APPLICATION  # Icon from cvp.assets.fonts.mdi

    def __init__(self, context: Context):
        super().__init__(context)
        # Initialize mode-specific attributes here

    @override
    def on_main_menu(self) -> None:
        # Optional: Add menu items to the main menu bar
        pass

    @override
    def on_status_menu(self) -> None:
        # Optional: Add status information to the status bar
        pass

    @override
    def on_process(self) -> None:
        # Main UI rendering logic
        with self.begin_mode_context():
            with begin_child_context("Main"):
                imgui.text("TODO: Implement {Name}Mode UI")
```

### 2. Register Mode in ModeManager

Modify `cvp/apps/player/modes/__init__.py`:

#### 2.1 Add Import (in alphabetical order with existing imports)

```python
from cvp.apps.player.modes.{name} import {Name}Mode
```

#### 2.2 Create Mode Instance (in region: Initialize Mode Instances)

```python
self.{name}_mode = {Name}Mode(context)
```

#### 2.3 Add to Menu (in `_menu_modes` tuple or `_submenu_modes` dict)

For main menu:
```python
self._menu_modes = (
    ...,
    self.{name}_mode,  # Add in appropriate position
    ...,
)
```

For submenu (e.g., under Games):
```python
self._submenu_modes = OrderedDict(
    {
        f"{mdi.NINTENDO_GAME_BOY} Games": (..., self.{name}_mode),
    }
)
```

## Icon Reference

Common icons from `cvp.assets.fonts.mdi`:
- `APPLICATION` - Generic app
- `FILE_DOCUMENT` - Document/text
- `FILE_LOCK` - Security/hash
- `VIDEO` - Video/media
- `IMAGE` - Image
- `FOLDER` - Files/folders
- `COG` - Settings
- `CONSOLE` - Terminal
- `CHART_LINE` - Charts/data
- `MAP` - Maps/location
- `NETWORK` - Network

Browse `cvp/assets/fonts/mdi.py` for full icon list.

## Mode Structure Reference

### Base Class (`BaseMode`)
- Inherits from `ModeInterface` and `MsgCallbacks`
- Provides helper methods:
  - `self.context` - Access to Context
  - `self.begin_mode_context()` - Context manager for mode UI
  - `self.selected_submenu` - Get/set selected submenu item
  - `self.menu_recent_items()` - Recent items menu
  - `text_success/normal/warning/error()` - Colored text helpers

### Key Methods to Override
| Method | Purpose | When Called |
|--------|---------|-------------|
| `on_process()` | Main UI rendering | Every frame |
| `on_main_menu()` | Menu bar items | When menu visible |
| `on_status_menu()` | Status bar items | When status bar visible |
| `on_event(event)` | Handle pygame events | On any event |
| `on_keyboard(keys)` | Handle keyboard input | Every frame |
| `on_msg(msg)` | Handle internal messages | When message received |

### Class Variables
| Variable | Type | Description |
|----------|------|-------------|
| `__cvp_mode_name__` | `str` | Display name in mode selector |
| `__cvp_mode_icon__` | `str` | Icon from mdi font |
| `__cvp_mode_show__` | `bool` | Show in menu (default: True) |

## Checklist

- [ ] Create `cvp/apps/player/modes/{name}/` directory
- [ ] Create `cvp/apps/player/modes/{name}/__init__.py` with Mode class
- [ ] Add import to `cvp/apps/player/modes/__init__.py`
- [ ] Create mode instance in `ModeManager.__init__()`
- [ ] Add mode to `_menu_modes` or `_submenu_modes`
- [ ] Choose appropriate icon from `cvp.assets.fonts.mdi`
- [ ] Implement `on_process()` method with UI logic

## Example Usage

```bash
# Add a simple "Audio" mode
/add-mode audio

# Add a "Network Scanner" mode
/add-mode network_scanner
```
