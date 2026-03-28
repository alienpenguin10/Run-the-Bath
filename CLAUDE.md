# Run The Bath — ML / MediaPipe module

## Project purpose
Python component for the "Run The Bath" hackathon game.
Detects player pose via webcam and streams gesture data to Unity over UDP.

## Stack
- Python 3.11 (conda env: `run-the-bath`)
- mediapipe 0.10+
- opencv-python
- socket (stdlib UDP)

## Environment setup
```bash
conda activate run-the-bath
pip install -r requirements.txt
```

## How to run
```bash
conda activate run-the-bath
python pose_detector.py
```

## Output format
Sends JSON over UDP to localhost:5005 at ~30fps:
```json
{ "lean": -0.3, "jump": false }
```
- lean: float -1.0 (full left) to +1.0 (full right), dead zone ±0.05
- jump: bool, true when rapid upward wrist velocity detected

## Key files
- pose_detector.py — webcam capture + MediaPipe pose
- udp_sender.py — UDP socket wrapper, call send(lean, jump)

## Gotchas
- Use the `run-the-bath` conda env (Python 3.11) — no need for --break-system-packages inside it
- MediaPipe landmark indices: left shoulder=11, right shoulder=12, left hip=23, right hip=24
- Lean is calculated from shoulder midpoint minus hip midpoint (normalised to frame width)
- Jump trigger: wrist y-velocity threshold is 0.04 per frame — tune this first if jumps feel unresponsive
- UDP is fire-and-forget — no error on Unity side being down, that's intentional

## Tests
Run pose detection without webcam (uses test image):
```bash
python pose_detector.py --test
```
Verify UDP is sending:
```bash
python udp_sender.py --debug
```