import json
from time import time

from marshmallow import Schema, fields, validates_schema, ValidationError, post_load


class Transaction(Schema):
    timestamp = fields.Int()
    sender = fields.Str()
    receiver = fields.Str()
    amount = fields.Int()
    signature = fields.Str()

    class Meta:
        ordered = True

class Block(Schema):
    transactions = fields.Nested(Transaction(many=True))
    mined_by = fields.Str(required=False)
    height = fields.Int(required=True)
    hash = fields.Str(required=True)
    previous_hash = fields.Str(required=True, allow_none=True)
    nonce = fields.Str(required=True)
    timestamp = fields.Int(required=True)

    class Meta:
        ordered = True

    # @validates_schema
    # def validate_hash(self, data, **kwargs):
    #     block = data.copy()
    #     block.pop("hash")
    #     if(data["previous_hash"] == None):
    #         return
    #     if data["hash"] != json.dumps(block, sort_keys=True):
    #         raise ValidationError("Fraudulent block: hash is wrong")


class Peer(Schema):
    ip = fields.Str(required=True)
    port = fields.Int(required=True)


class Ping(Schema):
    block_height = fields.Int()
    peer_count = fields.Int()
    is_miner = fields.Bool()






