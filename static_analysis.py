import subprocess

CLONED_REPOS_PATH = "./repos"
CK_ANALYSIS_PATH = "./ck_results"
CK_PATH = "../ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

def get_metrics(popular_repos):
    subprocess.run(["mkdir", CLONED_REPOS_PATH])
    subprocess.run(["mkdir", CK_ANALYSIS_PATH])
    for repo in popular_repos:
        repo_name = repo["node"]["name"]
        clone_repos(repo_name, repo["node"]["url"])
        run_ck(repo_name)
        delete_clone(repo_name)

# Clonar repos para pasta ./repos
def clone_repos(name, url):
    repo_path =  CLONED_REPOS_PATH + "/" + name

    print(repo_path)

    subprocess.run(["git", "clone", url, repo_path])

def delete_clone(name):
    repo_path =  CLONED_REPOS_PATH + "/" + name

    print(repo_path)

    subprocess.run(["rm", "-rf", repo_path])

# Executar análise estática
def run_ck(repo_name):
    subprocess.run(["mkdir", CK_ANALYSIS_PATH])

    repo_path =  CLONED_REPOS_PATH + "/" + repo_name
    results_path =  CK_ANALYSIS_PATH + "/" + repo_name + "/"

    print(results_path)

    subprocess.run(["mkdir", results_path])
    subprocess.run(["java", "-jar", CK_PATH, repo_path, "true", "0", "true", results_path])
