import sys
import io
import time
import threading
from contextlib import redirect_stdout, redirect_stderr
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Dict, Any, Optional, Tuple
from ..core.config import settings


class CodeTimeoutError(Exception):
    pass


class SafePythonExecutor:
    """Simple and safe Python code executor with basic restrictions"""
    
    ALLOWED_BUILTINS = {
        'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'divmod',
        'enumerate', 'filter', 'float', 'format', 'frozenset', 'hex',
        'int', 'len', 'list', 'map', 'max', 'min', 'oct', 'ord', 'pow',
        'range', 'reversed', 'round', 'set', 'sorted', 'str', 'sum',
        'tuple', 'type', 'zip', '__import__', 'print', 'locals', 'globals',
        'callable', '__build_class__',
        # Exception types
        'Exception', 'ValueError', 'TypeError', 'IndexError', 'KeyError',
        'AttributeError', 'RuntimeError', 'ZeroDivisionError', 'NameError'
    }
    
    ALLOWED_MODULES = {
        'math', 'statistics', 'random', 'datetime', 'json', 'numpy', 'pandas'
    }
    
    def __init__(self):
        self.restricted_builtins = {
            name: builtin for name, builtin in __builtins__.items()
            if name in self.ALLOWED_BUILTINS
        }
    
    def _execute_code_worker(self, code: str, safe_globals: dict) -> Tuple[str, str]:
        """Worker function to execute code in a separate thread"""
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, safe_globals)
        
        return stdout_capture.getvalue(), stderr_capture.getvalue()
    
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
        parsed_args = []
        if args:
            try:
                # Simple argument parsing - expect comma-separated values
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
        else:
            safe_globals['args'] = []
        
        start_time = time.time()
        
        try:
            # Use ThreadPoolExecutor for timeout handling
            with ThreadPoolExecutor(max_workers=1) as executor:
                # Add code to call main function if it exists
                enhanced_code = code + "\n\n# Auto-execute main function if it exists\ntry:\n    if 'main' in globals() and callable(main):\n        main(*args)\nexcept NameError:\n    pass\n"
                
                future = executor.submit(self._execute_code_worker, enhanced_code, safe_globals)
                
                try:
                    stdout_result, stderr_result = future.result(timeout=settings.code_execution_timeout)
                    execution_time = time.time() - start_time
                    
                    if stderr_result:
                        return False, None, stderr_result, execution_time
                    
                    return True, stdout_result or "Code executed successfully", None, execution_time
                    
                except FutureTimeoutError:
                    execution_time = time.time() - start_time
                    return False, None, f"Code execution timed out after {settings.code_execution_timeout} seconds", execution_time
                    
        except Exception as e:
            execution_time = time.time() - start_time
            return False, None, str(e), execution_time


# Global executor instance
executor = SafePythonExecutor()