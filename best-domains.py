import json
from collections import Counter


def read_domains_from_json(file_path):
    """
    Lit les domaines depuis un fichier JSON et renvoie la liste des domaines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if "domains" in data:
        return data["domains"]
    else:
        raise KeyError("La clé 'domains' est absente dans le fichier JSON.")


def extract_main_domain(domain):
    """
    Extrait le domaine principal (par exemple, 'wiki.com' depuis 'blabla.blabla.wiki.com').
    """
    parts = domain.split(".")
    if len(parts) > 2:
        return ".".join(parts[-2:])
    return domain


def top_10_domains_from_file(file_path):
    """
    Lit les domaines d'un fichier JSON, calcule les 10 plus fréquents, et les affiche joliment.
    """
    domain_list = read_domains_from_json(file_path)

    main_domains = [extract_main_domain(domain) for domain in domain_list]

    domain_counts = Counter(main_domains)

    top_10 = domain_counts.most_common(50)

    print("Top 10 des domaines les plus fréquents :\n")
    print(f"{'Rang':<5} {'Domaine':<20} {'Occurrences':<10}")
    print("-" * 40)
    for i, (domain, count) in enumerate(top_10, start=1):
        print(f"{i:<5} {domain:<20} {count:<10}")

    return top_10


file_path = "db-save.json"
top_10_domains_from_file(file_path)
