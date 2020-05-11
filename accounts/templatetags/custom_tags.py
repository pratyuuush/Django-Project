from django import template
import re

register = template.Library()


@register.simple_tag
def is_following(users_profile, profile_to_check):
    return users_profile.following.filter(user_id=profile_to_check.user_id).exists()
  