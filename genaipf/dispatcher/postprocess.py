import asyncio
from typing import Union
from abc import abstractmethod
from dataclasses import dataclass

@dataclass
class PostTextParam:
    language: str = "en"
    subtype: Union[str, None] = None

default_ptp = PostTextParam()

class PostTextBase:
    @abstractmethod
    def get_text(self, ptp: PostTextParam):
        ...
    
    async def get_text_agenerator(self, ptp: PostTextParam):
        for c in self.get_text(ptp):
            await asyncio.sleep(0.02)  # This could be any async operation
            yield c
        
class AnotherPostText(PostTextBase):
    def __init__(self, name):
        self.name = name
    
    def get_text(self, ptp: PostTextParam = default_ptp):
        if ptp.language=="cn":
            return """

如果您有额外的服务，我可以为您提供进一步的支持
"""
        else:
            return """

If you have the need to another service, I can provide further service for you.
"""

posttext_mapping = {
    "another_service": AnotherPostText("another_service")
}