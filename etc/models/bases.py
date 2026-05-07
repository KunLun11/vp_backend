import uuid

from django.db import models


class IDBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True
        ordering = ("id",)


class UUIDBaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        ordering = ("-uuid",)


class IDTimeBaseModel(IDBaseModel):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class UUIDTimeBaseModel(UUIDBaseModel):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
