import hashlib
import json
from typing import Dict, Any

def generate_tamper_proof_hash(payload: Dict[str, Any]) -> str:
    """
    Generates a deterministic SHA-256 hash for a given payload (e.g. an approved claim or a policy).
    This simulates a blockchain transaction hash for the hackathon.
    """
    # Deterministic serialization: sort_keys=True ensures the same dictionary 
    # always produces the exact same JSON string
    serialized_payload = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    
    # Generate SHA-256 hash
    return hashlib.sha256(serialized_payload.encode('utf-8')).hexdigest()
