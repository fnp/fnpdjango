from textile import Textile


class TextilePL(Textile):
    """Polish version of Textile.

    Changes opening quote to Polish lower-double.
    """
    glyph_definitions = dict(Textile.glyph_definitions,
        quote_double_open = '&#8222;'
    )


def textile_pl(text):
    return TextilePL().parse(text)


def textile_restricted_pl(text):
    return TextilePL(restricted=True, lite=True, noimage=True).parse(
        text, rel='nofollow')
