import os 
import platform
import logging
if platform.platform().startswitch('Windows'):
    logging_file=os.path.join(os.getenv('HOMEDRIVE'),
                              os.getenv('HOMEPATH'),
                              'test.log')
else:
    logging_file=os.path.join(os.getenv('HOME'),
                              'test.log')
print('logging to',logging_file)
logging.basicConfig(
    level=logging.debug,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file,
    filemode='w',
)
logging.debug('start')
logging.info('doing')
logging.warning('dying')