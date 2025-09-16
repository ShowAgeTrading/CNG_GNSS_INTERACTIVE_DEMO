# GNSS/RTK 3D Demo App – Python Implementation Plan

## 1. Project Structure

```
GNSS_RTK_Python_Demo/
  README.md
  requirements.txt
  main.py
  core/
    __init__.py
    app.py                # App entry, main loop, window management
    simulation_clock.py   # Simulation time, speed, direction
    event_bus.py          # Event/message system
  graphics/
    __init__.py
    globe.py              # 3D globe rendering, camera controls
    satellite.py          # Satellite marker rendering, orbits
    receiver.py           # Receiver marker rendering, selection
    materials.py          # Material/texture loading
    fade_boundary.py      # Fade effect for globe boundaries
    multi_view.py         # Multi-globe viewports
  ui/
    __init__.py
    main_ui.py            # Main UI overlay (PyQt5, DearPyGui, or pyglet)
    time_controls.py      # Time manipulation UI
    receiver_controls.py  # Receiver selection UI
    satellite_controls.py # Satellite/constellation selection UI
    error_controls.py     # Error toggles UI
  data/
    __init__.py
    receiver_profiles.json
    satellite_constellations.json
    locations.json
    error_models.json
  assets/
    models/               # Blender-exported .obj/.glb files (globe, satellites, receivers)
    textures/             # Earth, clouds, night lights, etc.
    icons/                # UI icons
  logs/
    session_logs/         # CSV logs of simulation runs
  tests/
    test_simulation.py
    test_graphics.py
    test_data.py
```

## 2. Technology Choices
- 3D Engine: Panda3D (recommended for Python, good 3D, easy model import, cross-platform)
  - Alternatives: pyglet + pyrr, moderngl, PyOpenGL (more manual, less high-level)
- UI: Panda3D built-in UI, or overlay with PyQt5/DearPyGui for advanced controls
- Data: JSON for receiver/satellite/location/error configs
- Logging: CSV for session data

## 3. Development Phases

### Phase 1: Project Setup
- Create folder structure as above
- Set up virtual environment, requirements.txt (Panda3D, numpy, etc.)
- Add README.md with setup/run instructions

### Phase 2: Core App & Window
- Implement app.py: window creation, main loop, event handling
- Implement simulation_clock.py: time scaling, direction, pause/play
- Implement event_bus.py: simple pub/sub for decoupling

### Phase 3: 3D Globe & Camera
- Implement globe.py: load globe model, apply textures, basic lighting
- Implement camera controls: orbit, zoom, pan, clamp zoom
- Implement fade_boundary.py: radial fade effect (shader or alpha mask)

### Phase 4: Satellite & Receiver Rendering
- Implement satellite.py: load satellite models, propagate orbits, group by constellation/plane
- Implement receiver.py: load receiver models, place on globe, allow selection
- Implement multi_view.py: support up to 4 globe viewports, each with independent controls

### Phase 5: UI & Controls
- Implement main_ui.py: overlay for controls and status
- Implement time_controls.py: play, pause, reverse, speed, scrub
- Implement receiver_controls.py: select receiver(s), base/rover/standalone
- Implement satellite_controls.py: select constellations/orbits
- Implement error_controls.py: toggle error models (iono, tropo, multipath, etc.)

### Phase 6: Data & Simulation
- Implement data loading (JSON): receiver profiles, satellite constellations, locations, error models
- Implement error model logic: apply effects to simulated signals
- Implement location database: multipath/interference probabilities by area

### Phase 7: Logging & Export
- Implement session logging: record user actions, simulation state, satellite/receiver data to CSV
- Implement export for graphing (S/N, satellite plot, etc.)

### Phase 8: Testing & Optimization
- Add unit tests for core logic, data loading, and simulation
- Profile performance, optimize rendering and data handling

## 4. Asset Workflow
- Model in Blender, export as .obj or .glb (apply transforms, Y up, Z forward)
- Place models in assets/models/
- Place textures in assets/textures/
- Reference assets in config/data files as needed

## 5. Next Steps
1. Confirm Panda3D or request another engine
2. Set up the folder structure and requirements.txt
3. Request code for app.py, simulation_clock.py, and globe.py to bootstrap the project
4. Import your Blender models/textures as they are ready
5. Continue requesting code for each subsystem as you progress

---

This plan is designed for incremental, testable development. You can copy this file to your new project root and use it as a checklist. For each step, request the code or guidance you need.