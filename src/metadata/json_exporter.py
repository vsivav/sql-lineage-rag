"""
JSON Exporter
"""

from pathlib import Path


class JsonExporter:

    def export(
        self,
        metadata,
        output_file: str,
    ):

        Path(output_file).write_text(

            metadata.model_dump_json(

                indent=4

            ),

            encoding="utf-8"

        )
