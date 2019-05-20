"""Log journal messages."""
from collections import defaultdict
from journal import *

class Logger:
    """Log messages.
    This class will not store any messages, but log them eagerly.
    For lazy logging use LazyLogger."""

    @staticmethod
    def get_level(level=Level.PROD):
        """Get a level.
        Arguments
        ~   level :: Either name of a level, or an actual Level"""
        if isinstance(level, str):
            try:
                return getattr(Level, level)
            except AttributeError as error:
                sys.stderr.write(
                    """Unknown logging level {} \n.
                    Please choose one of {}.""".format(
                        level_name,
                        [level.name for level in Level]))
                raise error

        return level if isinstance(level, Level) else Level.PROD

    def with_color(color, message):
        """Add color to the message"""
        return color + message + Color.ENDC.value if color else message

    @staticmethod
    def err_print(
            *args, **kwargs):
        """Print to stderr"""
        print(*args, file=sys.stdout, **kwargs)

    def __init__(self,
            client,
            name=None,
            level=None,
            output_dir_path=None,
            file_name=None,
            level_environment_variable="LOGLEVEL",
            line_sep=80*"=",
            *args, **kwargs):
        """Initialize Me"""
        self._level_env_var =\
            level_environment_variable
        self._level =\
            self.get_level(
                level,
                os.environ.get(
                    self._level_env_var))
        self._client = client
        self._name =\
            client if isinstance(client, str) else (
                name if name else str(client))
        self._in_file =(
            None if output_dir_path is None and file_name is None) else\
            os.path.join(
                output_dir_path if output_dir_path else os.getcwd(),
                file_name if file_name else "_".join(self._name.lower()))
        if self._in_file:
            self._log_message(self._name)
        self._statistics =\
            defaultdict(lambda: 0)
        self._line_sep=\
            line_sep
        try:
            super().__init__(
                *args, **kwargs)
        except:
            pass

    def get_source_info(self):
        """..."""
        traceback =\
            inspect.getframeinfo(
                inspect.stack()[1][0])
        return (
            "{classname}:\n\tfilename: \t{filename}\n\tlineno: \t{lineno}\n"
            "\tcode_context: \t{code_context}\n\tindex: {index}\n"\
            .format(classname=traceback.__class__.__name__,
                    filename=traceback.filename,
                    lineno=traceback.lineno,
                    code_context=traceback.code_context,
                    index=traceback.index))

    def _pretty_message_string(self,
            message,
            color=None):
        """..."""
        title = \
            Logger.with_color(
                Color.UNDERLINE,
                "{}@{} {}".format(
                    self._name,
                    message.timestamp,
                    message.labelstamp))
        formatted_message =\
            Logger.with_color(
                color,
                "{}".format(message.value))
        separator = \
            Logger.err_print(
                self._line_sep)
        return "{}\n{}\n{}\n".format(
            title,
            formatted_message,
            separator)

    def _log_message(self,
            message,#: Message
            color=None):
        """Log message with a time stamp."""
        self._statistics[message.label] += 1
        if message.level.value < self._level.value:
            return self._statistics

        if self._in_file:
            with open(self._in_file, "a") as log_file:
                log_file.write(
                    self._pretty_message_string(
                        message, color))
        return self._statistics

    def log(self, message):
        """...another word for _log_message"""
        return self._log_message(message)

    @property
    def client(self):
        """..."""
        return self._client

    def ignore(self, *messages):
        """..."""
        pass

    def info(self, *messages):
        """..."""
        return self._log_message(
            Info(*messages))
    
    def progress(self, *messages):
        """..."""
        return self._log_message(
            ProgressInfo(*messages))

    def note(self, *messages):
            """..."""
            return self._log_message(
                Note(*messages))

    def devnote(self, *messages):
        """..."""
        return self._log_message(
            DevNote(messages))

    def inform(self, *messages):
        """..."""
        return self._log_message(
            self.info(*messages))

    def study(self, *messages):
        """..."""
        return self._log_message(
            Funda(*messages))

    def remark(self, *messages):
        """..."""
        return self._log_message(
            Remark(*messages))

    def debug(self, *messages):
        """..."""
        return self._log_message(
            DebugInfo(*messages))
    
    def warning(self, *messages):
        """..."""
        return self._log_message(
            Alert(*messages))
    
    def beware(self, *messages):
        """..."""
        return self.warning(
            *messages)
    
    def warn(self, *messages):
        """..."""
        return self.warning(
            *messages)
    
    def alert(self, *messages):
        """..."""
        return self.warning(
            *messages)
    
    def error(self, *messages):
        """..."""
        return self._log_message(
            Error(*messages))
    
    def test(self, *messages):
        """..."""
        return self._log_message(
            Test(*messages))
    
    def success(self, *messages):
        """..."""
        return self._log_message(
            Success(*messages),
            color=Color.OKGREEN)
    
    def failure(self, *messages):
        """..."""
        return self._log_message(
            Failure(*messages),
            color=Color.FAIL)
    
    def dialog(self, *messages):
        """..."""
        return self._log_message(
            Dialog(*messages),
            color=Color.OKBLUE)
    
    def assertion(self, success, *messages):
        """Assert, and then log 
           Arguments
           ~   success :: Boolean"""
        assert success, messages[0]
        return self._log_message(
            Assertion(*messages))
    

class LazyLogger(Logger):
    """Log lazily.
    Store log messages in a file, and flush to disc when prompted,
    or after a given number of messages."""

    def __init__(self,
            name=None,
            level=None,
            output_dir_path=None,
            file_name=None,
            flush_threshold=10000,
            *args, **kwargs):
        """..."""
        self._logs = []
        self._flush_threshold = flush_threshold
        super().__init__(
            name=name,
            output_dir_path=output_dir_path,
            file_name=file_name,
            *args, **kwargs)
        self._in_file =\
            os.path.join(
                output_dir_path if output_dir_path else os.getcwd(),
                file_name if file_name else "output.log")

    def flush(self):
        """write all the log messages to disc"""
        with open(self._in_file, "a") as log_file:
            for message in self._logs:
                log_file.write(
                    self._pretty_message_string(message))

            self._logs = []

    def _log_message(self,
            message):
        """..."""
        self._logs.append(message)
        if len(self._logs) > self._flush_threshold:
            self.flush()


class WithLogging:
    """A base class that will allow the deriving class to log to an
    output resource. Attribute values to pass to Logger will be read
    from keyword arguments."""
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ------------------------------------------------------------------------
        output :: Either[File, stdio]#where logger will output to.
        """
        self._logger =\
            Logger(self.__class__, *args, **kwargs)

    @property
    def logger(self):
        """..."""
        return self._logger


def with_logging(level, *args, **kwargs):
    """class decorator"""
    def effective(cls):
        """class decorator"""
        cls.logger =\
            Logger(cls, level=level, *args, **kwargs)
        return cls
    return effective

class WithLazyLogging:
    """A base class that will allow the deriving class to log to an
    output resource. Attribute values to pass to Logger will be read
    from keyword arguments."""
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ------------------------------------------------------------------------
        output :: Either[File, stdio]#where logger will output to.
        """
        self.logger = LazyLogger(
            name="{}Logger".format(self.__class__.__name__),
            level=Logger.level.DEVELOP,
            output_dir_path=kwargs.get("log_output_dir_path", None),
            file_name=kwargs.get("log_file_name", None),
            flush_threshold=kwargs.get("log_flush_threshold", None)
            *args, **kwargs)

        super(WithLazyLogging, self).__init__(*args, **kwargs)

    @property
    def logger(self):
        """..."""
        return self._logger
