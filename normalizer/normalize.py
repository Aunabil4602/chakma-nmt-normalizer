import unicodedata
import re
import string
from ftfy import fix_text
from . import const


def fix_quotes(text):
    text = const.SINGLE_QUOTE_REGEX.sub("'", text)
    text = const.DOUBLE_QUOTE_REGEX.sub('"', text)
    return text


def normalize_chakma_script(text, punctuation_enable = True, ck_enable = True, bn_enable = True, punctuation_space = True):

    ################################ chakma script normalization
    # brackets and dari
    if punctuation_enable:
        text = re.sub('\[', '(', text)
        text = re.sub('\{', '(', text)
        text = re.sub('\]', ')', text)
        text = re.sub('\}', ')', text)
        text = re.sub('[\𑅁\৷\|]', '।', text)
        text = re.sub('[\—\−\–]', '-', text)
        text = re.sub('𑅃', '?', text)

    if ck_enable:
        # ja
        text = re.sub(r'𑄡', '𑄎', text)

        # core vowels
        text = re.sub(r'(?<!𑄳)𑄄', '𑄃𑄨', text)
        text = re.sub(r'(?<!𑄳)𑄅', '𑄃𑄪', text)
        text = re.sub(r'(?<!𑄳)𑄆', '𑄃𑄬', text)

        # Oi
        text = re.sub(r'𑅆', '𑄰', text)
        text = re.sub(r'𑄳𑄆', '𑄰', text)

        # kar
        text = re.sub(r'𑄲', '𑄱', text)
        text = re.sub(r'𑄩', '𑄨', text)
        text = re.sub(r'𑄫', '𑄪', text)

        # single joint kar
        text = re.sub(r'𑄯', '𑄮', text)
        text = re.sub(r'𑄮', '𑄮', text)

        # double/multiple E kar
        text = re.sub(r'𑄬+', '𑄬', text)

    ################################ bangla script normalization

    # this is for bn2ck, things will be different for ck2bn
    if bn_enable:
        
        # # single character rather than separate dot
        # text = re.sub(r'য়', 'য়' , text) 
        
        # # simplification
        # text = re.sub(r'য', 'জ', text)
        # text = re.sub(r'শ', 'স', text)
        # text = re.sub(r'ষ', 'স', text)
        # text = re.sub(r'ড়', 'র', text)
        # text = re.sub(r'ঢ়', 'র', text)
        # text = re.sub(r'ঋ', 'রি', text)
        # text = re.sub(r'ৎ', 'ত্', text)
        # text = re.sub(r'ঈ', 'ই', text)
        # text = re.sub(r'ঊ', 'উ', text)
        # text = re.sub(r'ী', 'ি', text)
        # text = re.sub(r'ূ', 'ু', text)
        # text = re.sub(r'ৃ', '্রি', text)

        pass


    ################################ spaces before every punctutaions
    # string.punctuation = !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    # '।' # include daari

    if punctuation_space:
        text=re.sub(r'(?<!\s)!', ' '+'!', text)
        text=re.sub(r'(?<!\s)"', ' '+'"', text)
        text=re.sub(r'(?<!\s)#', ' '+'#', text)
        text=re.sub(r'(?<!\s)\$', ' '+'$', text)
        text=re.sub(r'(?<!\s)%', ' '+'%', text)
        text=re.sub(r'(?<!\s)&', ' '+'&', text)
        text=re.sub(r'(?<!\s)\'', ' '+'\'', text)
        text=re.sub(r'(?<!\s)\(', ' '+'(', text)
        text=re.sub(r'(?<!\s)\)', ' '+')', text)
        text=re.sub(r'(?<!\s)\*', ' '+'*', text)
        text=re.sub(r'(?<!\s)\+', ' '+'+', text)
        text=re.sub(r'(?<!\s),', ' '+',', text)
        text=re.sub(r'(?<!\s)-', ' '+'-', text)
        text=re.sub(r'(?<!\s)\.', ' '+'.', text)
        text=re.sub(r'(?<!\s)/', ' '+'/', text)
        text=re.sub(r'(?<!\s):', ' '+':', text)
        text=re.sub(r'(?<!\s);', ' '+';', text)
        text=re.sub(r'(?<!\s)<', ' '+'<', text)
        text=re.sub(r'(?<!\s)=', ' '+'=', text)
        text=re.sub(r'(?<!\s)>', ' '+'>', text)
        text=re.sub(r'(?<!\s)\?', ' '+'?', text)
        text=re.sub(r'(?<!\s)@', ' '+'@', text)
        text=re.sub(r'(?<!\s)\[', ' '+'[', text)
        text=re.sub(r'(?<!\s)\\', ' \\\\', text) # still not clear how it gets replaced
        text=re.sub(r'(?<!\s)\]', ' '+']', text)
        text=re.sub(r'(?<!\s)\^', ' '+'^', text)
        text=re.sub(r'(?<!\s)_', ' '+'_', text)
        text=re.sub(r'(?<!\s)`', ' '+'`', text)
        text=re.sub(r'(?<!\s){', ' '+'{', text)
        text=re.sub(r'(?<!\s)\|', ' '+'|', text)
        text=re.sub(r'(?<!\s)}', ' '+'}', text)
        text=re.sub(r'(?<!\s)~', ' '+'~', text)
        text=re.sub(r'(?<!\s)।', ' '+'।', text)

    return text

def normalize(
    text,
    unicode_norm="NFKC",
    punct_replacement=None,
    url_replacement=None,
    emoji_replacement=None,
    apply_unicode_norm_last=True,
    punctuation_enable = True,
    ck_enable = True,
    bn_enable = True,
    punctuation_space = True
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
        text = unicodedata.normalize(unicode_norm, text)

    # apply unicode replacements
    text = const.UNICODE_REPLACEMENTS_REGEX.sub(
        lambda match: const.UNICODE_REPLACEMENTS.get(
            match.group(0), f"{match.group(1)}\u09cc"),
        text
    )

    if apply_unicode_norm_last:
        text = unicodedata.normalize(unicode_norm, text)

    # normalize chakma script
    text = normalize_chakma_script(text,
                                   punctuation_enable = punctuation_enable,
                                   ck_enable = ck_enable,
                                   bn_enable = bn_enable,
                                   punctuation_space = punctuation_space)

    # finally clean up extra whitespaces
    text = const.WHITESPACE_HANDLER_REGEX.sub(" ", text)

    return text
