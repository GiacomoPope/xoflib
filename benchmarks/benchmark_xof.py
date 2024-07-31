import os
from timeit import timeit
from xoflib import Blake3, Shake128, Shake256, AsconXof, AsconAXof, TurboShake128, TurboShake256
from tabulate import tabulate

REPEAT = 1
CHUNK_SIZES = [32, 2**10, 2**20]
MB_COUNT = 100
DATA_SIZE = MB_COUNT * 2**20  # MB_COUNT Mb of data read/absorb


def absorb_chunks(xof_shaker, chunks):
    for chunk in chunks:
        xof_shaker.absorb(chunk)
    return xof_shaker.finalize()


def read_chunks(xof_sponge, read_amount, read_count):
    for _ in range(read_count):
        val = xof_sponge.read(read_amount)
    return val


table_headers = [
    "Algorithm",
    "Absorb (32B)",
    "Read (32B)",
    "Absorb (1KB)",
    "Read (1KB)",
    "Absorb (1MB)",
    "Read (1MB)",
]
table_data = []

for xof_shaker in [
    AsconXof(),
    AsconAXof(),
    Blake3(),
    Shake128(),
    Shake256(),
    TurboShake128(1),
    TurboShake256(1),
]:
    print(f"Benchmarking: {str(xof_shaker)}")
    # Check chunks of 32 bytes, 1kb, 1Mb
    table_row = [str(xof_shaker)]
    for chunk_size in CHUNK_SIZES:
        # Benchmark absorption time
        chunks = [os.urandom(chunk_size) for _ in range(DATA_SIZE // chunk_size)]
        absorb_time = timeit(
            "absorb_chunks(xof_shaker, chunks)",
            globals={
                "absorb_chunks": absorb_chunks,
                "xof_shaker": xof_shaker,
                "chunks": chunks,
            },
            number=REPEAT,
        ) / REPEAT

        # Benchmark reading time
        xof_sponge = absorb_chunks(xof_shaker, chunks)
        read_count = len(chunks)
        read_time = timeit(
            "read_chunks(xof_sponge, read_amount, read_count)",
            globals={
                "read_chunks": read_chunks,
                "xof_sponge": xof_sponge,
                "read_amount": chunk_size,
                "read_count": read_count,
            },
            number=REPEAT,
        ) / REPEAT

        table_row.append(f"{MB_COUNT/(absorb_time):0.0f} MB/s")
        table_row.append(f"{MB_COUNT/(read_time):0.0f} MB/s")
    table_data.append(table_row)

print(tabulate(table_data, table_headers, tablefmt="github"))
