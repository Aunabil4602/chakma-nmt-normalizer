import unicodedata
import re
from ftfy import fix_text
from . import const


def fix_quotes(text):
    text = const.SINGLE_QUOTE_REGEX.sub("'", text)
    text = const.DOUBLE_QUOTE_REGEX.sub('"', text)
    return text


def normalize_chakma_script(text, ck_replace_cg=True, ck_replace_vs=True, ck_replace_s=True):
    if ck_replace_s:
        text = re.sub('\[', '(', text)
        text = re.sub('\{', '(', text)
        text = re.sub('\]', ')', text)
        text = re.sub('\}', ')', text)
        text = re.sub('[\𑅁\৷\|]', '।', text)
        text = re.sub('[\—\−\–]', '-', text)

    if ck_replace_cg:
        # not used in real pronunciation
        text = re.sub(r'𑄑', '𑄖', text)
        text = re.sub(r'𑄒', '𑄗', text)
        text = re.sub(r'𑄓', '𑄘', text)
        text = re.sub(r'𑄔', '𑄙', text)
        text = re.sub(r'𑄕', '𑄚', text)

        # ja
        text = re.sub(r'(?<!𑄳)𑄡', '𑄎', text)

        # core vowels
        text = re.sub(r'(?<!𑄳)𑄄', '𑄃𑄨', text)
        text = re.sub(r'(?<!𑄳)𑄅', '𑄃𑄪', text)
        text = re.sub(r'(?<!𑄳)𑄆', '𑄃𑄬', text)

    if ck_replace_vs:
        text = re.sub(r'𑅆', '𑄳𑄆', text)

        text = re.sub(r'𑄲', '𑄱', text)
        text = re.sub(r'𑄩', '𑄨', text)
        text = re.sub(r'𑄫', '𑄪', text)

        text = re.sub(r'𑄯', '𑄮', text)
        text = re.sub(r'𑄯', '𑄮', text)
        text = re.sub(r'𑄮', '𑄮', text)

    return text

def normalize(
    text,
    unicode_norm="NFKC",
    punct_replacement=None,
    url_replacement=None,
    emoji_replacement=None,
    apply_unicode_norm_last=True,
    ck_replace_cg=True,
    ck_replace_vs=True,
    ck_replace_s=True
):
    # fix encoding related issues first
    # and group characters for future
    # char replacements to work
    text = fix_text(
        text,
        normalization="NFC",
        explain=False,

    )

    # normalize variations of quotes
    text = fix_quotes(text)

    # replace punctuations with specified replacement (if any)
    if punct_replacement is not None:
        text = const.PUNCT_HANDLER_REGEX.sub(punct_replacement, text)

    # replace URLS in text with specified replacement (if any)
    if url_replacement is not None:
        text = const.URL_HANDLER_REGEX.sub(url_replacement, text)

    # replace emojis in text with specified replacement (if any)
    if emoji_replacement is not None:
        text = const.EMOJI_HANDLER_REGEX.sub(emoji_replacement, text)

    # apply char replacements
    text = text.translate(const.CHAR_REPLACEMENTS)

    if not apply_unicode_norm_last:
        text = unicodedata.normalize(text, unicode_norm)

    # apply unicode replacements
    text = const.UNICODE_REPLACEMENTS_REGEX.sub(
        lambda match: const.UNICODE_REPLACEMENTS.get(
            match.group(0), f"{match.group(1)}\u09cc"),
        text
    )

    # normalize chakma script
    text = normalize_chakma_script(text)

    if apply_unicode_norm_last:
        text = unicodedata.normalize(unicode_norm, text)

    # finally clean up extra whitespaces
    text = const.WHITESPACE_HANDLER_REGEX.sub(" ", text)

    return text
