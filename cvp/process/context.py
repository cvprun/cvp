# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class MultiprocessingContextMethod(StrEnum):
    """
    Depending on the platform, multiprocessing supports three ways to start a process.

    https://docs.python.org/3.12/library/multiprocessing.html#multiprocessing-start-methods
    """

    spawn = auto()
    """
    The parent process starts a fresh Python interpreter process. The child process will
    only inherit those resources necessary to run the process object’s run() method. In
    particular, unnecessary file descriptors and handles from the parent process will
    not be inherited. Starting a process using this method is rather slow compared to
    using fork or forkserver.

    Available on POSIX and Windows platforms. The default on Windows and macOS.
    """

    fork = auto()
    """
    The parent process uses os.fork() to fork the Python interpreter. The child process,
    when it begins, is effectively identical to the parent process. All resources of the
    parent are inherited by the child process. Note that safely forking a multithreaded
    process is problematic.

    Available on POSIX systems. Currently the default on POSIX except macOS.

    Note:
        The default start method will change away from fork in Python 3.14. Code that
        requires fork should explicitly specify that via get_context() or
        set_start_method().
    """

    forkserver = auto()
    """
    When the program starts and selects the forkserver start method, a server process is
    spawned. From then on, whenever a new process is needed, the parent process connects
    to the server and requests that it fork a new process. The fork server process is
    single threaded unless system libraries or preloaded imports spawn threads as a
    side-effect so it is generally safe for it to use os.fork(). No unnecessary
    resources are inherited.

    Available on POSIX platforms which support passing file descriptors over Unix pipes
    such as Linux.
    """
