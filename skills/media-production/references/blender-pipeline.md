# 3D with Blender, headless, driven by a JSON scene spec

Use when a recurring character, product or set must look identical in every shot, from any angle, at near-zero marginal cost. Tags as in `SKILL.md`. Blender is free (GPL); the Python API and command line are documented in the manual (bib. 1). The script below was run on Blender 5.3.0 headless on 18/11/2026 and rendered a 1080x1920 PNG in about 5 s on an Apple-silicon Mac (one cube, 16 samples, a simple scene; real scenes are slower, measure yours).

## 1. When 3D beats AI images
3D wins for a recurring character or product, any camera angle, reused poses, exact product geometry, and cost per piece after setup. AI wins for speed to the first piece and varied backgrounds. Hybrid is common: a 3D subject with a transparent background (`sc.render.film_transparent = True`, PNG RGBA) over AI or photo backgrounds. AI-to-3D mesh generators can give a first mesh; check their terms, topology, hands and commercial rights before use (not read here).

## 2. Command line (read in the manual, bib. 1, and from `Blender --help` on 5.3.0)
`-b` run in background (no UI); `-P file.py` run a Python script; `-o path` render output path; `-f N` render frame N; `-a` render the animation; `-S name` set the scene; `-E engine` set the engine. Everything after a bare `--` is ignored by Blender and left to the script in `sys.argv`. On macOS the binary is inside the app bundle: `/Applications/Blender.app/Contents/MacOS/Blender`.

## 3. The JSON spec
One file lists defaults and scenes. Keep it in version control with the .blend.
```json
{"defaults":{"width":1080,"height":1920,"engine":"BLENDER_EEVEE","samples":16},
 "scenes":[{"id":"01",
  "camera":{"loc":[0,-6,1.2],"rot_deg":[85,0,0],"lens":35},
  "light":{"energy":800,"loc":[3,-3,4]},
  "bg":[0.1,0.2,0.3,1],
  "objects":[{"type":"cube","loc":[0,0,1],"scale":1,"color":[0.9,0.5,0.1,1]}]}]}
```
Real projects add per scene: `pose` (action name), `expression` (shape-key values), `camera_preset`, `background_image`, `props`, `frames`.

## 4. The script (`render_scene.py`)
```python
import bpy, sys, json, math
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
spec_path, scene_id, out = argv[0], argv[1], argv[2]
spec = json.load(open(spec_path)); d = spec.get("defaults", {})
s = next(x for x in spec["scenes"] if x["id"] == scene_id)
bpy.ops.wm.read_factory_settings(use_empty=True)   # for a real rig: open your .blend instead
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = d.get("width", 1080), d.get("height", 1920)
sc.render.engine = d.get("engine", "BLENDER_EEVEE")
w = bpy.data.worlds.new("w"); w.use_nodes = True; sc.world = w
w.node_tree.nodes["Background"].inputs[0].default_value = s.get("bg", [0.05, 0.05, 0.05, 1])
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam)
c = s["camera"]; cam.location = c["loc"]; cam.rotation_euler = [math.radians(a) for a in c["rot_deg"]]
cam.data.lens = c.get("lens", 35); sc.camera = cam
l = s["light"]; ld = bpy.data.lights.new("key", "POINT"); ld.energy = l["energy"]
lo = bpy.data.objects.new("key", ld); lo.location = l["loc"]; sc.collection.objects.link(lo)
for o in s.get("objects", []):
    bpy.ops.mesh.primitive_cube_add(location=o["loc"], scale=[o.get("scale", 1)] * 3)
    m = bpy.data.materials.new("m"); m.diffuse_color = o["color"]; bpy.context.object.data.materials.append(m)
sc.render.filepath = out; sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
```
Run: `Blender -b -P render_scene.py -- scene.json 01 /tmp/out.png`. Loop over ids in the shell for a batch. The engine enum name changed between Blender versions; if you get a TypeError, list the valid names with `bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items`.
For a real character: save a `.blend` with the rig, shape keys, a **lighting rig** (key, fill, rim) and **camera presets** at the target ratio; open it with `Blender -b series.blend -P render_scene.py -- ...` and let the script only apply pose, expression, camera preset and background. Never change the rig mid-season.

## 5. Building assets (licences first)
Realistic humans: MPFB2 add-on (open source; code and asset licence files are separate, read them). Stylised: VRoid Studio is free and each creator sets terms per model; third-party models follow their own terms. Rigs and animations: Adobe Mixamo, read Adobe's current terms for commercial use and redistribution. Purchased or downloaded models follow their own licence; keep it with the project. Marketplace assets: CC0 and CC BY differ (attribution), see `rights-and-labels.md`.

## 6. Render time and cost
Measure: render 3 frames at final size on the target machine, multiply. Starting ranges to verify, not promises **[F]**: EEVEE stylised frames seconds to a minute at 1080x1920 on a recent laptop; Cycles with denoise minutes. Batch estimate = frames x seconds per frame / 3600 hours. Setup is days (model, rig, expressions, sets); break-even against AI images = setup hours / (AI cost per piece + AI retry hours saved). Decide after the story or product proves itself.
Output: PNG frames to a folder; assemble with ffmpeg or Remotion (`code-video-and-assembly.md`); add captions as text layers.
