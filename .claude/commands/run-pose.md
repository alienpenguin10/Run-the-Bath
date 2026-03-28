# /run-pose

Start the pose detector with a visible debug window showing the skeleton overlay and current lean/jump values.

Steps:
1. Check requirements are installed: `pip install -r requirements.txt --break-system-packages`
2. Run: `python pose_detector.py --debug`
3. Watch the terminal output — lean and jump values should update at ~30fps
4. Press Q to quit

If the webcam doesn't open, try setting OPENCV_CAMERA_INDEX=1 as an env var.