"""
Utility Functions
"""

import shutil
from pathlib import Path

from config import UPLOAD_FOLDER
from config import VECTOR_DB


def clear_uploads():

    if UPLOAD_FOLDER.exists():

        shutil.rmtree(UPLOAD_FOLDER)

    UPLOAD_FOLDER.mkdir(exist_ok=True)


def clear_database():

    if VECTOR_DB.exists():

        shutil.rmtree(VECTOR_DB)

    VECTOR_DB.mkdir(exist_ok=True)


def format_sources(docs):

    pages = []

    for doc in docs:

        page = doc.metadata.get("page", 0) + 1

        source = Path(

            doc.metadata.get(

                "source",

                "Unknown"

            )

        ).name

        pages.append(

            f"📄 {source} (Page {page})"

        )

    return sorted(set(pages))