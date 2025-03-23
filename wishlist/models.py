from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishes")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    gift_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="will_gift", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
