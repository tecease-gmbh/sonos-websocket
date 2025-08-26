import urllib.parse
import urllib.request
import json
from websocket import create_connection
import ssl

def wws_request(namespace, command, item_type, item_id, ip_address, data=None):
    # No need for an api key, you can use this one
    sonos_api_key = "123e4567-e89b-12d3-a456-426655440000"

    headers = {
        "X-Sonos-Api-Key": sonos_api_key,
        "Sec-WebSocket-Protocol": "v1.api.smartspeaker.audio"
    }

    extra = {
        "name": "Sonos Test",
	"appId": "com.test.sonos"
    }

    if data is not None:
        extra.update(data)

    request = json.dumps([
        {
            "namespace": namespace,
            "command": command,
            f"{item_type}Id": f"{item_id}",
            "sessionId": None,
            "cmdId": None
        },
        extra
    ])

    ws = create_connection(
        url=f"wss://{ip_address}:1443/websocket/api",
        timeout=5,
        header=headers,
        sslopt={"cert_reqs": ssl.CERT_NONE}
    )

    ws.send(request)
    print("Sent")
    result = ws.recv()
    print("Received '%s'" % result)
    
    json_result = json.loads(result)
    success = json_result[0]["success"]
    print(f"Success: {success}")
    ws.close()

    return success, json_result

wws_request(
    namespace="groups", 
    command="getGroups", 
    item_type="household", 
    item_id="Sonos_Bv1uue5mNqAVIIA7JNkE2quGS6.M2ZOXQzjLZxVftbbM9YV",
    ip_address="192.168.1.165",
data={}
)