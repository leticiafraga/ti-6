import csv
from datetime import datetime

# Função para calcular idade a partir da data "created_at"
def calculate_age(created_at):
    created_at_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    current_at_date = datetime.now()
    age = current_at_date.year - created_at_date.year
    return age

# Função para coletar e imprimir informações dos repositórios
def collect_repo_info(repos):
    header = ["repo_name", "created_at", "age", "releases"]
    rows = []

    for repo in repos:
        repo = repo["node"]
        repo_name = repo["name"]
        created_at = repo["createdAt"]
        age = calculate_age(created_at)
        releases = repo["releases"]["totalCount"]

        rows.append([repo_name, created_at, age, releases])
        
    with open('repo_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
