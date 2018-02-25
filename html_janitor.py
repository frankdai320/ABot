from html.parser import HTMLParser


class Cleaner(HTMLParser):
    @classmethod
    def clean(cls, text):
        cleaner = cls()
        cleaner.feed(text)
        cleaner.close()
        return cleaner.text

    @property
    def level(self):
        return len(self._tag_path)

    @property
    def text(self):
        return ''.join(self._text_parts)

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self._tag_path = []
        self._text_parts = []

    def handle_starttag(self, tag, attrs):
        self._tag_path.append(tag)

        if self.level <= 1:  # it will only ever be one, not zero, but this reads more nicely
            self._text_parts.append('<{}>'.format(tag))

    def handle_endtag(self, tag):
        if self._tag_path[-1] != tag:
            raise ValidationError('Mismatched tags.')

        if self.level <= 1:  # it will only ever be one, not zero, but this reads more nicely
            self._text_parts.append('</{}>'.format(tag))

        del self._tag_path[-1]

    def handle_data(self, data):
        self._text_parts.append(data)


class ValidationError(ValueError):
    pass
