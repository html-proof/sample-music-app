try:
    with open("import_error.log", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "ImportError" in line or "ModuleNotFoundError" in line:
                print(line.strip()[:200]) # Print first 200 chars to avoid truncation
except Exception as e:
    print(f"Error reading log: {e}")
