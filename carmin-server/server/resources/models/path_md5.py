from marshmallow import Schema, fields, post_load


class PathMD5():
    def __init__(self, md5: str):
        self.md5 = md5


class PathMD5Schema(Schema):
    md5 = fields.Str(required=True)

    @post_load
    def to_model(self, data):
        return PathMD5(**data)
