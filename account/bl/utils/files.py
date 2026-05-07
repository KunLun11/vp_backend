import base64
import uuid

import filetype
from django.core.files.base import ContentFile


def decode_base64_image(data_uri: str) -> ContentFile:
    if data_uri.startswith("data:"):
        header, encoded = data_uri.split(",", 1)
        mime = header.split(":")[1].split(";")[0]
    else:
        encoded = data_uri
        mime = None

    file_data = base64.b64decode(encoded)
    if not mime:
        kind = filetype.guess(file_data)
        if kind is not None:
            mime = kind.mime
        else:
            mime = "image/jpeg"  # fallback

    file_name = f"profile_{uuid.uuid4()}.jpg"
    content_file = ContentFile(file_data, name=file_name)
    content_file.content_type = mime  # добавляем атрибут для _validate_photo

    return content_file
