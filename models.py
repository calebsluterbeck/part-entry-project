# Parts Class
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Part:
    po_number: str
    num_of_parts: int
    part_number: str
    part_type: Optional[str] = None
    ref_letter: Optional[str] = None
    sharp_edges: Optional[bool] = None
    notes: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    @property
    def deburr(self) -> bool:
        return not self.sharp_edges


