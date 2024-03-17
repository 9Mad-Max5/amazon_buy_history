import logging
import inspect

def setup_logging(log_level="DEBUG"):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Ungültiges Log-Level: %s" % log_level)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='logfile.txt', format=log_format)

    stack = inspect.stack()
    # the_method = stack[1][0].f_code.co_name
    l_name = stack[1].function
    if l_name == "__init__":
        # l_name = f"{stack[1][0].f_locals["self"].__class__.__name__}.{stack[1].function}"
        l_name = f"{stack[1][0].f_locals["self"].__class__.__name__}"


    logger = logging.getLogger(l_name)
    logger.setLevel(numeric_level)

    return logger