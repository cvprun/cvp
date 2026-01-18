# CLAUDE.md

## Project Overview

**CVP (Computer Vision Player)** - Python multimedia application with computer vision, media playback, and visual programming. Requires Python 3.12+.

## Commands

| Script | Purpose |
|--------|---------|
| `./python` | Python executable |
| `./black.sh` | Format code |
| `./flake8.sh` | PEP8 linting |
| `./isort.sh` | Sort imports |
| `./mypy.sh` | Type checking |
| `./pytest.sh` | Run tests |
| `./ci.sh` | Full CI pipeline |
| `./build.sh` | Build package |
| `./run` | Run application |

### Testing
```bash
./pytest.sh                           # All tests
./pytest.sh tester/module/test_foo.py # Specific file
./pytest.sh tester/module/            # Module tests
```
Coverage output: `build/cov/`

## Architecture

### Application Modes
- `cvp player` - Desktop GUI (ImGui/PyGame)
- `cvp worker` - Flow graph processing
- `cvp agent` - Background service
- `cvp tester` - Capability testing

### Module Structure
| Module | Purpose |
|--------|---------|
| `cvp/pygame/` | Graphics primitives |
| `cvp/imgui/` | UI bindings |
| `cvp/ffmpeg/` | Media processing |
| `cvp/cv/` | Computer vision |
| `cvp/gl/` | OpenGL utilities |
| `cvp/flow/` | Node graph system |
| `cvp/ws/` | WebSocket communication |

## Configuration

### Environment Variables
- `CVP_HOME`, `CVP_DEBUG`, `CVP_LOGGING_SEVERITY`
- `CVP_USE_UVLOOP`, `SDL_VIDEO_X11_FORCE_EGL`

### Config Files
`setup.cfg`, `pytest.ini`, `mypy.ini`, `flake8.ini`, `isort.cfg`

## Coding Guidelines

1. **One class per file**
2. **Explicit imports**: `from module import Name` not `import module`
3. **Type annotations**: All functions with params, returns, attributes
4. **Test mirroring**: `cvp/mod/foo.py` → `tester/mod/test_foo.py`
5. **Fix warnings**: No `# type: ignore` or `# noqa` unless unavoidable
6. **Constants with Final**: Use `Final` for constant values
7. **Test main block**: Always add `if __name__ == "__main__":\n    main()` at test file end
8. **Empty `__init__.py`**: Keep `__init__.py` files empty when possible
9. **Self-documenting code**: Prefer clear naming over comments
10. **Line width 88**: Comments and docstrings must not exceed 88 characters
11. **Override decorator**: Use `@override` from `cvp.types.override` for overridden methods
12. **Abstract methods**: Always `raise NotImplementedError` in `@abstractmethod` bodies
