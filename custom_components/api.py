import logging
import json

_LOGGER = logging.getLogger(__name__)
FACEBOOK_MSG_API = "https://graph.facebook.com/v21.0/me/messages?access_token={token}"


class GenericError(Exception):
    pass


async def send_message(async_client, message, image_bytes, targets, token):
    successful_sends = 0
    url = FACEBOOK_MSG_API.format(token=token)

    for target in targets:
        _LOGGER.info("Posting to %s", target)

        if image_bytes:
            upload_data = {
                "recipient": json.dumps({"id": target}),
                "message": json.dumps({"attachment": {"type": "image", "payload": {}}}),
            }
            files = {"filedata": ("image.jpg", image_bytes, "image/jpeg")}
            try:
                up_resp = await async_client.post(url, data=upload_data, files=files)
                up_resp.raise_for_status()
            except Exception as e:
                raise GenericError(e)
            j = up_resp.json()

            _LOGGER.info("result: %s", j)
        else:
            data = {
                "recipient": {"id": target},
                "message": {"text": message},
            }
            try:
                response = await async_client.post(url, json=data, timeout=10)
                response.raise_for_status()
            except Exception as e:
                raise GenericError(e)

        successful_sends += 1

    return successful_sends
