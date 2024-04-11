import logging
import sys

logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - | %(message)s |',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

output_log = logging.getLogger("output")