from get_data import get_popular_java_repos
from collect_repo_info import collect_repo_info
from static_analysis import get_metrics

def print_names(popular_repos):
    for repo in popular_repos:
        print(repo["node"]["name"])

if __name__ == "__main__":
    num_repos = 10
    try:
        popular_repos = get_popular_java_repos(num_repos)
        collect_repo_info(popular_repos)
        print_names(popular_repos)
        get_metrics(popular_repos)        
    except Exception as e:
        print(e)
    exit(0)
