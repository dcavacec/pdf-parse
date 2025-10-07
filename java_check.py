"""
Java Runtime Detection
Checks if Java is available for Tabula-py dependency.
"""

import subprocess
import shutil
from typing import Optional


def check_java_available() -> bool:
    """
    Check if Java runtime is available on the system.
    
    Returns:
        True if Java is available, False otherwise
    """
    try:
        # Try to find java executable
        java_path = shutil.which('java')
        if not java_path:
            return False
        
        # Try to run java -version to verify it works
        result = subprocess.run(
            ['java', '-version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return False


def get_java_version() -> Optional[str]:
    """
    Get Java version string if available.
    
    Returns:
        Java version string or None if not available
    """
    try:
        result = subprocess.run(
            ['java', '-version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            # Extract version from stderr (java -version outputs to stderr)
            version_line = result.stderr.split('\n')[0]
            return version_line.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


# Global flag for Java availability
JAVA_AVAILABLE = check_java_available()
JAVA_VERSION = get_java_version() if JAVA_AVAILABLE else None
