import argparse
import cv2
import mediapipe as mp
import udp_sender

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

prev_wrist_y = None


def calculate_lean(lm):
    shoulder_mid_x = (lm[11].x + lm[12].x) / 2
    hip_mid_x = (lm[23].x + lm[24].x) / 2
    lean = (shoulder_mid_x - hip_mid_x) * 4
    lean = max(-1.0, min(1.0, lean))
    if abs(lean) < 0.05:
        lean = 0.0
    return lean


def detect_jump(lm):
    global prev_wrist_y
    wrist_y = (lm[15].y + lm[16].y) / 2
    jump = False
    if prev_wrist_y is not None:
        velocity = prev_wrist_y - wrist_y
        if velocity > 0.04:
            jump = True
    prev_wrist_y = wrist_y
    return jump


def shoulders_visible(lm, threshold=0.5):
    return lm[11].visibility > threshold and lm[12].visibility > threshold


def process_frame(frame, pose, debug=False):
    frame = cv2.resize(frame, (640, 480))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    lean = 0.0
    jump = False

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        if shoulders_visible(lm):
            lean = calculate_lean(lm)
            jump = detect_jump(lm)
        else:
            global prev_wrist_y
            prev_wrist_y = None

        if debug:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            print(f"lean={lean:+.3f}  jump={jump}")

    udp_sender.send(lean, jump)
    return frame, lean, jump


def run_webcam(debug=False):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: cannot open webcam")
        return

    with mp_pose.Pose(min_detection_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame, lean, jump = process_frame(frame, pose, debug=debug)

            if debug:
                cv2.imshow("Run the Bath — Pose", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


def run_test():
    import numpy as np

    test_img = np.zeros((480, 640, 3), dtype=np.uint8)
    test_img[:] = (200, 200, 200)

    with mp_pose.Pose(min_detection_confidence=0.6) as pose:
        _, lean, jump = process_frame(test_img, pose, debug=True)
        print(f"\nTest result — lean: {lean:+.3f}, jump: {jump}")
        print("(No person detected is expected with a blank test image)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pose detector for Run the Bath")
    parser.add_argument("--debug", action="store_true", help="Show skeleton overlay and print values")
    parser.add_argument("--test", action="store_true", help="Run against a static test image")
    args = parser.parse_args()

    if args.test:
        run_test()
    else:
        run_webcam(debug=args.debug)
