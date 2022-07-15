import functools as _functools
import time as _time
from types import TracebackType as _TracebackType
from typing import Callable as _Callable, ParamSpec as _ParamSpec, Type as _Type, TypeVar as _TypeVar
from typing_extensions import Self as _Self

_P = _ParamSpec("_P")
_T = _TypeVar("_T")

class Timer(object):
    """
    A simple timer for MATLAB-style tic and toc.
    
    Attributes
    ----------
    name: str
        The name of the timer. 
    verbose: bool
        Whether the timer's results should be returned or printed to stderr.
    precision: int | None
        The decimal degit precision to which seconds should be printed.
    
    Methods
    -------
    tic() -> None
        Start the timer. Raises a RuntimeError if the timer has already been tic-ced without a toc.
    toc() -> float | None
       Returns the timer's results if verbose; otherwise, prints to stderr.
    tictoc(Callable[P, T]) -> Callable[P, T]
        A decorator for calling tic, then toc. Only useful when verbose.
    
    Notes
    -----
    verbose is False when name is None, the default value.
    Timer objects can be used as context managers, inspired by answers under https://stackoverflow.com/questions/5849800/what-is-the-python-equivalent-of-matlabs-tic-and-toc-functions.
    For assessing performance, use Python's timeit module instead.
    Calling the functions tic and toc are necessary; simply typing tic or toc on a line does not do anything.
    tic, toc, and tictoc are also functions that can be used as a DEFAULT timer's methods.
    """
    
    def __init__(self, name: str | None=None, precision: int | None=2) -> None:
        """
        Create a timer object.
        
        Parameters
        ----------
        name: str | None=None
            The name of the counter to print.
        precision: int | None=2
            The degree of precision to print the seconds. If precision is None, print all digits of accuracy.
        """
        
        self.tstart = None
        self.name = name
        self.precision = precision
        self.verbose = name is not None
        
    def tic(self) -> None:
        """
        Begin the timer.
        
        Returns
        -------
        None
        
        Raises
        ------
        RuntimeError
            Do not call tic more than once without first calling toc. Each tic should correspond to a toc.
        """
        
        if self.tstart is not None:
            raise RuntimeError(f"Timer {self.name} is still in tic, toc first before tic-ing again.")
        
        self.tstart = _time.perf_counter()
        
    def toc(self) -> float | None:
        """
        Stop the timer.
        
        Returns
        -------
        float | None
            Return the float if the timer is not verbose. Otherwise, return None and print the results to stderr.
        
        Raises
        ------
        RuntimeError
            Do not call toc more than once without first calling tic. Each toc should correspond to a tic.
            
        Notes
        -----
        precision is not applied if the timer is not verbose.
        """
        
        if self.tstart is None:
            raise RuntimeError(f"Timer {self.name} is still in toc, tic first before toc-ing again.")

        diff_seconds = _time.perf_counter() - self.tstart
        
        if not self.verbose:
            return diff_seconds
        
        if self.precision is not None:
            diff_seconds = round(diff_seconds, self.precision)
        
        diff_time = f"{diff_seconds}s"
        if diff_seconds >= 60:
            diff_minutes, diff_seconds = divmod(diff_seconds, 60)
            diff_time = f"{diff_minutes}m {diff_seconds}s"
            if diff_minutes >= 60:
                diff_hours, diff_minutes = divmod(diff_minutes, 60)
                diff_time = f"{diff_hours}h {diff_minutes}m {diff_seconds}s"
        print(f'[{self.name}] Elapsed: {diff_time}')
        self.tstart = None
        
    def tictoc(self, func: _Callable[_P, _T]) -> _Callable[_P, _T]:
        """A decorator for timing functions."""
        
        @_functools.wraps(func)
        def inner(*args, **kwargs):
            self.tic()
            result = func(*args, **kwargs)
            self.toc()
            return result
        return inner
    
    def __enter__(self) -> _Self:
        self.tic()
        return self
        
    def __exit__(self, exc_type: _Type[BaseException] | None, exc_value: BaseException | None, exception_traceback: _TracebackType | None) -> bool:
        self.toc()
        return False
    
TIMER = Timer(__name__)
def tic():
    TIMER.tic()
def toc():
    TIMER.toc()
def tictoc(func: _Callable[_P, _T]) -> _Callable[_P, _T]:
    return TIMER.tictoc(func)