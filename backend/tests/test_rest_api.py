from bias_detection_api.rest_api import app 

def test_remove_bias():
    client = app.test_client()
    response = client.post(
        "/remove-bias",
        json={
            "text": "The manager claimed that the younger women on the team shouldn’t handle negotiations because they’re too emotional, and instead suggested giving the important tasks to the older men, who he said are naturally more reliable. He also remarked that employees from that specific Asian community usually struggle with leadership roles and should stick to basic support work."
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    print(data["result"])
