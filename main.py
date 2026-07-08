from src.lineage.table_lineage import TableLineageBuilder
from src.lineage.column_lineage import ColumnLineageBuilder
from src.lineage.function_analyzer import FunctionAnalyzer
from src.lineage.cte_resolver import CTEResolver
from src.lineage.subquery_resolver import SubqueryResolver
from src.lineage.lineage_engine import LineageEngine
from pathlib import Path
from src.metadata.generator import MetadataGenerator
from src.metadata.json_exporter import JsonExporter
from src.metadata.chunk_builder import ChunkBuilder
from src.embeddings.embedder import Embedder
from src.vectorstore.index_builder import IndexBuilder
from src.vectorstore.search_engine import SearchEngine

parser = SQLParser()

ast = parser.parse_file("tests/sample.sql")

builder = TableLineageBuilder()

graph = builder.build(ast)

print("\nTABLE LINEAGE\n")

for relationship in graph.relationships():

    print(
        relationship.source_table,
        " ---> ",
        relationship.target_table,
        "(",
        relationship.operation,
        ")"
    )

builder = ColumnLineageBuilder()

statement = parser.parse_file("tests/sample.sql")[0]

lineage = builder.build(statement)

print()

print("COLUMN LINEAGE")

for row in lineage:

    print(row)

analyzer = FunctionAnalyzer()

statement = ast[0]

functions = analyzer.analyze(statement)

print("\nFUNCTIONS\n")

for func in functions:

    print(func)

resolver = CTEResolver()

statement = ast[0]

ctes = resolver.resolve(statement)

print("\nCTEs\n")

for cte in ctes:

    print(cte)

resolver = SubqueryResolver()

statement = ast[0]

subqueries = resolver.resolve(statement)

print("\nSUBQUERIES\n")

for subquery in subqueries:

    print(subquery)

parser = SQLParser()

ast = parser.parse_file("tests/sample.sql")

engine = LineageEngine()

result = engine.analyze(ast)

print("\nALIASES")
print(result.aliases)

print("\nTABLE LINEAGE")
for r in result.table_relationships:
    print(r)

print("\nCOLUMN LINEAGE")
for c in result.column_lineage:
    print(c)

print("\nCTEs")
for c in result.ctes:
    print(c)

print("\nSUBQUERIES")
for s in result.subqueries:
    print(s)

print("\nFUNCTIONS")
for f in result.functions:
    print(f)

generator = MetadataGenerator()

metadata = generator.generate(

    procedure_name="usp_LoadSales",

    lineage_result=result

)

JsonExporter().export(

    metadata,

    "output/usp_LoadSales.json"

)

print(metadata.model_dump_json(indent=4))

builder = ChunkBuilder()

chunks = builder.build(metadata)

print()

print("CHUNKS")

for chunk in chunks:

    print("=" * 60)

    print(chunk.chunk_id)

    print()

    print(chunk.text)

embedder = Embedder()

records = embedder.embed_chunks(chunks)

print()

print(records[0])

builder = IndexBuilder()

store = builder.build(chunks)

store.save(

    "output/lineage.faiss",

    "output/metadata.json"

)

print("FAISS Index Created")

engine = SearchEngine(store)

results = engine.search(

    "Where does CustomerAddress come from?",

    top_k=3

)

print()

print("SEARCH RESULTS")

print()

for result in results:

    print("=" * 60)

    print("Score :", result.score)

    print()

    print(result.record.text)
