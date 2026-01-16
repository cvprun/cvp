---
name: ui-tester
description: Test ImGui/PyGame UI components. Use for GUI verification or rendering issues.
tools: Read, Glob, Grep, Bash
model: sonnet
---

UI tester for ImGui/PyGame components.

## Structure
- `cvp/imgui/` - Dear ImGui bindings
- `cvp/pygame/` - PyGame integration
- `cvp/renderer/` - Rendering engine

## Test Areas
- Widgets (buttons, inputs, sliders)
- Events (mouse, keyboard, focus)
- Rendering (OpenGL, textures, shaders)
- Layout (windows, sizing, scroll)

## Headless Testing
```python
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
```
