import re


def rm_punctuation(raw_txt):
    return "".join(re.findall('[\u4e00-\u9fa5a-zA-z0-9]+', raw_txt, re.S))


if __name__ == '__main__':
    print(rm_punctuation('aaa+sd-asf=)af'))
