import uuid

from django.db import models
from FAY.models.model_profile import Profile


class Follow(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return (
            str(self.following.user.username)
            + " follows "
            + str(self.followed.user.username)
        )
