def format_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"

def clean_search_query(query: str) -> str:
    return query.strip().lower()
