from tortoise import fields
from tortoise.models import Model


class Players(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    age = fields.IntField()
    email = fields.TextField()
    phone = fields.CharField(max_length=12)
    password = fields.CharField(max_length=128, null=False)
    telegram_id = fields.IntField(unique=True, null=True)
    is_superuser = fields.BooleanField(default=False)
    games = fields.ManyToManyField(
        model_name='models.Games',
        related_name='players',
        through='players_games',
    )


class Games(Model):
    id = fields.IntField(pk=True)
    game_name = fields.CharField(max_length=50, unique=True)
    players: fields.ManyToManyRelation['Players']


class Files(Model):
    id = fields.IntField(pk=True)
    file_key = fields.UUIDField(null=False)
    name = fields.TextField(null=False)
    file_format = fields.CharField(max_length=4, null=False)
    content_type = fields.CharField(max_length=255, null=False)
