import re

import googletrans

from pypubmed.util.logger import MyLogger


class Translate(object):

    logger = MyLogger('Translate')

    def __init__(self, url='translate.google.cn'):
        self.url = url
        self.translator = googletrans.Translator(service_urls=[url])
        self.check_service()
        self.nltk_checked = False

    def check_service(self):
        try:
            self.translator.detect('hello world')
        except Exception as e:
            self.logger.error('service not avaiable: {}'.format(self.url))
            exit(1)

    def check_nltk(self):
        """
            - download from Python
            >>> import nltk
            >>> nltk.download('punkt')

            - download from command line
            $ python -m nltk.downloader punkt

            - more: http://www.nltk.org/data.html
        """
        try:
            import nltk
        except SyntaxError:
            self.logger.warning('nltk is not available for Python2, use Python3 please.')
            exit(1)

        try:
            nltk.sent_tokenize('hello world')
            self.logger.info('nltk is ok!')
        except Exception:
            self.logger.warning('nltk_data not found! downloading start ...')
            try:
                nltk.download('punkt')
                self.nltk_checked = True
            except:
                self.logger.error('nltk_data download failed! you can also try: python -m nltk.downloader punkt')
                exit(1)

    def translate(self, text, dest='zh-cn', **kwargs):
        texts = self.split_text(text)

        result = []
        for text in texts:
            text = self.translator.translate(text, dest=dest, **kwargs).text
            result.append(text)
        result = ''.join(result)

        return result

    def split_text(self, text, max_len=5000):
        """
            googletrans limits 5000 characters

            split text with nltk.sent_tokenize

            >>> nltk.sent_tokenize('hello world!')
        """
        if len(text) <= max_len:
            return [text]

        if not self.nltk_checked:
            self.check_nltk()

        self.logger.info('split text with nltk')

        texts = []
        for sent in nltk.sent_tokenize(text):
            if (not texts) or (len(texts[-1]) + len(sent) > max_len):
                texts.append(sent)
            else:
                texts[-1] += ' ' + sent
        return texts


if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('text', help='the text to translate', nargs='*')
    parser.add_argument('-u', '--url', help='the service url of googletrans [%(default)s]', default='translate.google.cn')
    parser.add_argument('-d', '--dest', help='the dest language [%(default)s]', default='zh-cn')
    parser.add_argument('-o', '--output', help='the output filename [stdout]')
    
    args = vars(parser.parse_args())

    if not args['text']:
        parser.print_help()
        exit()

    t = Translate(url=args['url'])
    out = open(args['output']) if args['output'] else sys.stdout
    with out:
        r = t.translate(' '.join(args['text']), dest=args['dest'])
        out.write(r + '\n')
