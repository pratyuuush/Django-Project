from django import template
import re

register = template.Library()


@register.simple_tag
def is_following(users_profile, profile_to_check):
    return users_profile.following.filter(user_id=profile_to_check.user_id).exists()

@register.filter(name='parse_hashtags')
def parse_hashtags(field):
    hashtags_arr = re.findall(r"#(\w+)", field)
    for hashtag in hashtags_arr:
        html_tag = "<a href='/explore?hashtag=" + hashtag + "'>#" + hashtag + "</a>"
        field = field.replace("#" + hashtag, html_tag)
    return field


@register.filter(name='addClass')
def addClass(field, css):
   return field.as_widget(attrs={"class":css})


@register.filter(name='addID')
def addID(field, css):
   return field.as_widget(attrs={"id":css})