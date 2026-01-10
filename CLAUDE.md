# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CVP (Computer Vision Player)** is a Python-based multimedia application that provides computer vision capabilities, media playback, and visual programming tools. It includes desktop GUI components, worker processes, background agents, and a testing framework.

## Development Commands

### Core Development Scripts
- `./python` - Create/activate local Python virtual environment
- `./black.sh` - Format code with Black
- `./flake8.sh` - Run PEP8 linting
- `./isort.sh` - Sort import order
- `./mypy.sh` - Run type checking
- `./pytest.sh` - Run unit tests
- `./ci.sh` - Run full CI pipeline (all checks above)

### Build and Package
- `./build.sh` - Build the package
- `./build-pyinstaller.sh` - Build standalone executable with PyInstaller
- `./clean.sh` - Clean build artifacts
- `./run` - Run CVP player application
- `./run-demo` - Run demo/example
- `./run-style` - Run style demo

### Testing
- `./pytest.sh` - Run all tests in the `tester/` directory
- `./pytest.sh {path}` - Run specific test file or directory
  - Example: `./pytest.sh tester/module/test_foo.py` - Run specific test file
  - Example: `./pytest.sh tester/module/` - Run all tests in a module directory
- Test configuration in `pytest.ini` with coverage reporting to `build/cov/`
- Tests organized by modules: `tester/dtypes/`, `tester/context/`, etc.

## Architecture

### Application Modes (cvp/apps/)
The application has four primary modes accessible via CLI:

1. **Player** (`cvp player`) - Desktop GUI application (default mode)
   - Main graphical interface with ImGui/PyGame
   - Media player with FFmpeg integration
   - Layout and window management

2. **Worker** (`cvp worker`) - Flow graph processing
   - Visual programming with node-based processing
   - OpenCV, NumPy, CuPy, Pandas integration
   - Pipeline execution with asyncio support

3. **Agent** (`cvp agent`) - Background agent service
   - Background processing and monitoring
   - Service-oriented functionality

4. **Tester** (`cvp tester`) - Configuration and capability testing
   - System configuration validation
   - OpenGL capability testing

### Core Modules Structure

- **cvp/pygame/** - PyGame integration and graphics primitives
- **cvp/imgui/** - Dear ImGui bindings for UI
- **cvp/ffmpeg/** - FFmpeg wrapper for media processing
- **cvp/cv/** - Computer vision utilities (OpenCV integration)
- **cvp/gl/** - OpenGL utilities and pixel buffer objects
- **cvp/flow/** - Visual programming and node graph system
- **cvp/process/** - Subprocess management and control
- **cvp/logging/** - Logging configuration and formatters
- **cvp/config/** - Configuration management
- **cvp/resources/** - Asset and resource management

### Key Dependencies
- **ImGui Bundle** - Primary UI framework
- **PyGame CE** - Graphics and event handling
- **OpenCV** - Computer vision processing
- **FFmpeg** (via python-mpv) - Media playback
- **NumPy/CuPy** - Numerical computing
- **PyOpenGL** - OpenGL bindings
- **Asyncio/Uvloop** - Asynchronous programming

## Configuration

### Environment Variables
Key environment variables (see `cvp/system/environ_keys.py`):
- `CVP_HOME` - Application home directory
- `CVP_DEBUG` - Enable debug mode
- `CVP_LOGGING_SEVERITY` - Set logging level
- `CVP_USE_UVLOOP` - Use uvloop for async operations
- `SDL_VIDEO_X11_FORCE_EGL` - Force EGL on X11
- `PYOPENGL_USE_ACCELERATE` - Enable PyOpenGL acceleration

### Configuration Files
- `.env.test` - Test environment configuration
- `setup.cfg` - Package metadata and configuration
- `pytest.ini` - Test configuration with coverage settings
- `mypy.ini` - Type checking configuration
- `flake8.ini` - Linting configuration
- `isort.cfg` - Import sorting configuration

## Development Notes

### Python Version
- Requires Python 3.12+
- Uses modern Python features and type hints extensively

### Code Style
- Black formatting is enforced
- PEP8 compliance via flake8
- Import sorting with isort
- Type checking with mypy
- All scripts use `# -*- coding: utf-8 -*-` headers

#### Coding Guidelines
- **One class per file**: Prefer organizing code with one class per file for better modularity and maintainability
- **Explicit imports**: Use `from ... import SpecificName` instead of `import package` to explicitly specify what is being used
  - Example: `from typing import List, Dict` instead of `import typing`
  - This improves code clarity and makes dependencies more explicit
- **Test file creation**: When creating a class in `cvp/`, create a corresponding test file in `tester/` following the pattern `test_{name}.py`
  - Example: If creating `cvp/module/foo.py`, create `tester/module/test_foo.py`
  - Test files should mirror the source structure for easy navigation and maintenance

### Testing Structure
- Tests are in the `tester/` directory (excluded from package)
- Coverage reporting configured to `build/cov/`
- Source coverage includes `cvp` package

### Package Structure
- Main package: `cvp/`
- Entry point: `cvp.entrypoint:main`
- Console script: `cvp` command
- Version defined in `cvp/__init__.py`

### Media and Graphics
- Supports hardware-accelerated graphics (OpenGL/EGL)
- Font management and rendering capabilities
- Multi-platform display support with configurable backends
- Media playbook with FFmpeg integration for various formats

The codebase follows a modular architecture where each major feature area is separated into distinct modules, with clear separation between GUI components, processing pipelines, and system integration layers.