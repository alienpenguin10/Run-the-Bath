using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class UdpReceiver : MonoBehaviour
{
    [Header("Network")]
    [SerializeField] private int port = 5005;

    public float Lean { get; private set; }
    public bool Jump { get; private set; }

    private UdpClient _client;
    private Thread _thread;
    private bool _running;

    [Serializable]
    private class PoseData
    {
        public float lean;
        public bool jump;
    }

    private void Start()
    {
        _client = new UdpClient(port);
        _running = true;
        _thread = new Thread(Listen) { IsBackground = true };
        _thread.Start();
        Debug.Log($"[UdpReceiver] Listening on port {port}");
    }

    private void Listen()
    {
        var endPoint = new IPEndPoint(IPAddress.Any, 0);
        while (_running)
        {
            try
            {
                byte[] bytes = _client.Receive(ref endPoint);
                string json = Encoding.UTF8.GetString(bytes);
                PoseData data = JsonUtility.FromJson<PoseData>(json);
                Lean = data.lean;
                Jump = data.jump;
            }
            catch (SocketException)
            {
                // Socket closed during shutdown — expected
            }
        }
    }

    private void OnDestroy()
    {
        _running = false;
        _client?.Close();
        _thread?.Join(500);
    }
}
