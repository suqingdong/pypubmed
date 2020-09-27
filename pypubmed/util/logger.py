import sys
import logging


class MyLogger(logging.Logger):
    def __init__(self,
                 name=None,
                 level=logging.INFO,
                 fmt=None,
                 datefmt=None,
                 logfile=None,
                 filemode='w',
                 stream=sys.stderr,
                 verbose=False,
                 colored=True,
                 **kwargs):

        if verbose:
            level = logging.DEBUG

        super(MyLogger, self).__init__(name, level)

        self.fmt = fmt or '[%(asctime)s %(funcName)s %(levelname)s] %(message)s'
        self.datefmt = datefmt or '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter(self.fmt, self.datefmt)

        if logfile:
            self._addFilehandler(logfile, filemode)
            stream_colored = open(logfile, mode=filemode)
        else:
            self._addStreamHandler(stream)
            stream_colored = None

        if colored:
            try:
                import coloredlogs
                coloredlogs.install(fmt=self.fmt, level=level, logger=self, stream=stream_colored)
            except ImportError:
                print('\x1b[33mcoloredlogs not installed, please install it with: \x1b[32m`pip install coloredlogs`\x1b[0m')

    def _addFilehandler(self, filename, filemode):
        file_hdlr = logging.FileHandler(filename, filemode)
        file_hdlr.setFormatter(self.formatter)
        self.addHandler(file_hdlr)

    def _addStreamHandler(self, stream):
        stream_hdlr = logging.StreamHandler(stream)
        stream_hdlr.setFormatter(self.formatter)
        self.addHandler(stream_hdlr)


if __name__ == '__main__':
    logger = MyLogger()
    logger.info('hello world')
    
    logger = MyLogger(colored=True)
    logger.info('hello world')
    logger.warning('hello world')
    