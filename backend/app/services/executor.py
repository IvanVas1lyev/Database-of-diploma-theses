import sys
import io
import time
import signal
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional, Tuple
from ..core.config import settings


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Code execution timed out")


class SafePythonExecutor:
    """Simple and safe Python code executor with basic restrictions"""
    
    ALLOWED_BUILTINS = {
        'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'divmod',
        'enumerate', 'filter', 'float', 'format', 'frozenset', 'hex',
        'int', 'len', 'list', 'map', 'max', 'min', 'oct', 'ord', 'pow',
        'range', 'reversed', 'round', 'set', 'sorted', 'str', 'sum',
        'tuple', 'type', 'zip'
    }
    
    ALLOWED_MODULES = {
        'math', 'statistics', 'random', 'datetime', 'json'
    }
    
    def __init__(self):
        self.restricted_builtins = {
            name: builtin for name, builtin in __builtins__.items()
            if name in self.ALLOWED_BUILTINS
        }
    
    def execute_code(self, code: str, args: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str], float]:
        """
        Execute Python code safely with restrictions
        
        Returns:
            Tuple of (success, result, error, execution_time)
        """
        if len(code) > settings.max_code_length:
            return False, None, f"Code too long (max {settings.max_code_length} characters)", 0.0
        
        # Prepare execution environment
        safe_globals = {
            '__builtins__': self.restricted_builtins,
            '__name__': '__main__',
        }
        
        # Add allowed modules
        for module_name in self.ALLOWED_MODULES:
            try:
                safe_globals[module_name] = __import__(module_name)
            except ImportError:
                pass
        
        # Parse arguments if provided
        if args:
            try:
                # Simple argument parsing - expect comma-separated values
                parsed_args = []
                for arg in args.split(','):
                    arg = arg.strip()
                    if arg.isdigit():
                        parsed_args.append(int(arg))
                    elif arg.replace('.', '').isdigit():
                        parsed_args.append(float(arg))
                    else:
                        parsed_args.append(arg.strip('"\''))
                safe_globals['args'] = parsed_args
            except Exception as e:
                return False, None, f"Error parsing arguments: {str(e)}", 0.0
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        
        try:
            # Set timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(settings.code_execution_timeout)
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals)
            
            execution_time = time.time() - start_time
            
            # Get output
            stdout_result = stdout_capture.getvalue()
            stderr_result = stderr_capture.getvalue()
            
            if stderr_result:
                return False, None, stderr_result, execution_time
            
            return True, stdout_result or "Code executed successfully", None, execution_time
            
        except TimeoutError:
            return False, None, f"Code execution timed out after {settings.code_execution_timeout} seconds", time.time() - start_time
        except Exception as e:
            execution_time = time.time() - start_time
            return False, None, str(e), execution_time
        finally:
            signal.alarm(0)  # Cancel the alarm


# Global executor instance
executor = SafePythonExecutor()