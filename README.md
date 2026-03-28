# Run the Bath

Python component for the "Run the Bath" hackathon game. Detects player pose via webcam using MediaPipe and streams gesture data to Unity over UDP.

## Setup

```bash
conda activate run-the-bath
pip install -r requirements.txt
```

## Usage

Run the pose detector:

```bash
python pose_detector.py
```

With debug overlay (skeleton + terminal output):

```bash
python pose_detector.py --debug
```

Test without a webcam:

```bash
python pose_detector.py --test
```

Test UDP sending:

```bash
python udp_sender.py --debug
```

## How it works

The pose detector captures webcam frames, runs MediaPipe Pose to extract body landmarks, and calculates two values:

- **lean** — float from -1.0 (left) to +1.0 (right), based on shoulder-to-hip offset
- **jump** — bool, triggered by rapid upward wrist movement

These are sent as JSON over UDP to `localhost:5005` at ~30fps:

```json
{ "lean": -0.3, "jump": false }
```

## Unity integration

`UdpReceiver.cs` is a MonoBehaviour that listens on port 5005 and exposes `Lean` (float) and `Jump` (bool) properties. Attach it to any GameObject in your Unity scene.

## Files

| File | Description |
|---|---|
| `pose_detector.py` | Webcam capture + MediaPipe pose detection |
| `udp_sender.py` | UDP socket wrapper |
| `UdpReceiver.cs` | Unity UDP consumer |
| `requirements.txt` | Python dependencies |
