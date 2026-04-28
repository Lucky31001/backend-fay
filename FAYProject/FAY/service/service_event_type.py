def extract_event_type_names(raw):
    """ Handle une string ou une list de strings et retourne une liste de noms d'event types uniques """
    if not raw:
        return []
    items = raw if isinstance(raw, (list, tuple)) else [raw]
    seen = []
    for item in items:
        name = str(item.get("name", "") if isinstance(item, dict) else item).strip()
        if name and name not in seen:
            seen.append(name)
    return seen