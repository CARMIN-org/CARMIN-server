from marshmallow import Schema, fields, post_load

UPLOAD_TYPES = ["File", "Archive"]


class UploadData():
    def __init__(self, base64_content: str, upload_type: str, md5: str = None):
        self.base64_content = base64_content
        self.upload_type = upload_type
        self.md5 = md5

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class UploadDataSchema(Schema):
    class Meta:
        ordered = True

    base64_content = fields.Str(
        required=True, dump_to='base64Content', load_from='base64Content')
    upload_type = fields.Str(
        validate=lambda n: n in UPLOAD_TYPES, dump_to='type', load_from='type')
    md5 = fields.Str()

    @post_load
    def to_model(self, data):
        return UploadData(**data)
