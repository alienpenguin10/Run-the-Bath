import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TARGET = ("127.0.0.1", 5005)


def send(lean, jump):
    data = json.dumps({"lean": round(lean, 3), "jump": bool(jump)})
    sock.sendto(data.encode(), TARGET)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="UDP sender for Run the Bath")
    parser.add_argument("--debug", action="store_true", help="Send test packets and print them")
    args = parser.parse_args()

    if args.debug:
        import time

        test_values = [
            (0.0, False),
            (-0.5, False),
            (0.5, False),
            (0.0, True),
            (-1.0, False),
            (1.0, True),
        ]
        for lean, jump in test_values:
            data = json.dumps({"lean": round(lean, 3), "jump": bool(jump)})
            print(f"Sending: {data}")
            sock.sendto(data.encode(), TARGET)
            time.sleep(0.1)
        print("Done — sent 6 test packets to 127.0.0.1:5005")
