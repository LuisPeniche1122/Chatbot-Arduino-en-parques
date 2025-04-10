"""Utility functions and constants.

I am having some problems caching the memory and the retrieval. When
I decorate for caching, I get streamlit init errors.
"""

import logging
import pathlib
from typing import Any

from langchain.memory import ConversationBufferMemory
from streamlit.logger import get_logger

logging.basicConfig(encoding="utf-8", level=logging.INFO)
LOGGER = get_logger(__name__)


def init_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


LOGGER.info("init memory")
MEMORY = init_memory()


