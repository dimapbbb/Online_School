from rest_framework.exceptions import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get('link_to_video')
        if link.find('youtube') == -1:
            raise ValidationError("Можно сохранить ссылку только на 'youtube'")
