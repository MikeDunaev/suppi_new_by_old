from analytics.settings import BASE_DIR
from os.path import join
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.FileHandler(join(BASE_DIR, f'calculations/services/logs/error.log'))
f_handler = logging.FileHandler(join(BASE_DIR, f'calculations/services/logs/error.log'))
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
f_format = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
