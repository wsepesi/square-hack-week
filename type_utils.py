from typing import NamedTuple

# class ID(str):
#     def __init__(self, value: str):
#         if not value.startswith(('s', 'g')):
#             raise ValueError("ID must start with 's' or 'g'")
#         super().__init__(value)

class ProcessedData(NamedTuple):
    id: str
    text: str
    metadata: dict
