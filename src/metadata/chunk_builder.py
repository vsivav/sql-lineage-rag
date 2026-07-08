"""
Chunk Builder

Converts metadata into semantic chunks suitable
for vector databases like FAISS.

Strategy
--------
- One chunk per column lineage
- One chunk per table lineage
- One chunk for procedure summary
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.metadata.schema import ProcedureMetadata


@dataclass
class MetadataChunk:

    chunk_id: str

    chunk_type: str

    text: str

    metadata: dict


class ChunkBuilder:

    def build(
        self,
        metadata: ProcedureMetadata
    ) -> List[MetadataChunk]:

        chunks: List[MetadataChunk] = []

        #
        # ---------------------------------------------------
        # Procedure Summary
        # ---------------------------------------------------
        #

        summary = f"""
Procedure : {metadata.procedure_name}

Source Tables :
{', '.join(metadata.source_tables)}

Target Tables :
{', '.join(metadata.target_tables)}

Functions :
{', '.join(metadata.functions)}
""".strip()

        chunks.append(

            MetadataChunk(

                chunk_id=f"{metadata.procedure_name}_summary",

                chunk_type="procedure",

                text=summary,

                metadata={

                    "procedure": metadata.procedure_name

                }

            )

        )

        #
        # ---------------------------------------------------
        # Column chunks
        # ---------------------------------------------------
        #

        for column in metadata.columns:

            text = f"""
Procedure : {metadata.procedure_name}

Target Column :
{column.target_column}

Source Columns :
{", ".join(column.source_columns)}

Transformation :
{column.transformation}
""".strip()

            chunks.append(

                MetadataChunk(

                    chunk_id=f"{metadata.procedure_name}_{column.target_column}",

                    chunk_type="column",

                    text=text,

                    metadata={

                        "procedure": metadata.procedure_name,

                        "target_column": column.target_column

                    }

                )

            )

        #
        # ---------------------------------------------------
        # Table chunks
        # ---------------------------------------------------
        #

        for table in metadata.target_tables:

            text = f"""
Procedure : {metadata.procedure_name}

Target Table :
{table}

Source Tables :
{", ".join(metadata.source_tables)}
""".strip()

            chunks.append(

                MetadataChunk(

                    chunk_id=f"{metadata.procedure_name}_{table}",

                    chunk_type="table",

                    text=text,

                    metadata={

                        "procedure": metadata.procedure_name,

                        "table": table

                    }

                )

            )

        return chunks
