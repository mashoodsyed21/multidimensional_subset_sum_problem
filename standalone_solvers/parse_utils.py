import sys
from pathlib import Path

# Add parent directory to path to allow importing mss
sys.path.append(str(Path(__file__).parent.parent))

from mss.models import MSSInstance

def parse_instance_file(filepath: str) -> MSSInstance:
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
    if not lines:
        raise ValueError("File is empty or contains only comments.")
        
    def parse_vector(line: str) -> tuple[int, ...]:
        line = line.replace(',', ' ')
        parts = line.split()
        return tuple(int(x) for x in parts)
        
    target = parse_vector(lines[0])
    vectors = tuple(parse_vector(line) for line in lines[1:])
    
    if not vectors:
        raise ValueError("No input vectors found in the file.")
        
    d = len(target)
    for v in vectors:
        if len(v) != d:
            raise ValueError(f"Target vector has dimension {d}, but found vector {v} with dimension {len(v)}.")
            
    return MSSInstance(vectors=vectors, target=target, n=len(vectors), d=d)
