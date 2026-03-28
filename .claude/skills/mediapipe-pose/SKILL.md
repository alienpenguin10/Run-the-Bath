---
name: mediapipe-pose
description: >
  Use this skill when writing or modifying any code that uses MediaPipe
  pose landmarks, calculates lean angle, detects jump gestures, or sends
  UDP game input data. Also use when debugging webcam or socket issues.
---

## What this skill covers
Real-time human pose → game input pipeline using MediaPipe Pose.

## Landmark indices (memorise these)
| Point | Index |
|---|---|
| Left shoulder | 11 |
| Right shoulder | 12 |
| Left hip | 23 |
| Right hip | 24 |
| Left wrist | 15 |
| Right wrist | 16 |

## Lean calculation
```python
shoulder_mid_x = (lm[11].x + lm[12].x) / 2
hip_mid_x      = (lm[23].x + lm[24].x) / 2
lean = (shoulder_mid_x - hip_mid_x) * 4  # scale to ~-1..+1
lean = max(-1.0, min(1.0, lean))
if abs(lean) < 0.05: lean = 0.0          # dead zone
```

## Jump detection
```python
prev_wrist_y = None
def detect_jump(lm):
    global prev_wrist_y
    wrist_y = (lm[15].y + lm[16].y) / 2
    jump = False
    if prev_wrist_y is not None:
        velocity = prev_wrist_y - wrist_y   # positive = moving up
        if velocity > 0.04:
            jump = True
    prev_wrist_y = wrist_y
    return jump
```

## UDP packet
```python
import socket, json
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def send(lean, jump):
    data = json.dumps({"lean": round(lean, 3), "jump": bool(jump)})
    sock.sendto(data.encode(), ("127.0.0.1", 5005))
```

## Gotchas
- `mp.solutions.pose.Pose(min_detection_confidence=0.6)` — lower than 0.5 causes too many ghost detections
- Landmarks are normalised 0..1 — always use `.x` and `.y`, never pixel coords for lean
- MediaPipe drops frames if resolution is too high — cap at 640×480 with `cv2.resize`
- On first run MediaPipe downloads a model file (~25MB) — needs internet
- Jump threshold of 0.04 is a starting point — test with your actual player standing 1.5–2m from camera
- `visibility` score on landmarks — skip frame if shoulder visibility < 0.5