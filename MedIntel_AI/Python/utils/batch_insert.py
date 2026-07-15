def chunk_data(data, chunk_size=5000):
    """
    Split a list into smaller batches.
    """

    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]