# /test-bridge

Test that the UDP bridge is sending data correctly.

Steps:
1. Run the sender in debug mode: `python udp_sender.py --debug`
2. In a second terminal, listen on the UDP port:
   `python -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.bind(('',5005)); [print(s.recvfrom(1024)) for _ in range(20)]"`
3. You should see JSON packets arriving every ~33ms
4. Confirm lean changes when you tilt, jump triggers on rapid arm raise