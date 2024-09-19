import requests
from dotenv import load_dotenv
import os
import math
load_dotenv()

token = os.getenv("GITHUB_TOKEN")

GITHUB_API_URL = "https://api.github.com/graphql"

def run_query(query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code} {response.json()}")
    
def get_query(num_repos, cursor):
    return f"""
        {{
          search(query: "language:Typescript", type: REPOSITORY, first: {num_repos}, after: "{cursor}") {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            edges {{
              node {{
                ... on Repository {{
                  name
                  owner {{
                    login
                  }}
                  createdAt
                  stargazerCount
                  url
                  releases {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """

def get_popular_java_repos(num_repos):
    repos = []
    max_per_page = num_repos if num_repos < 25 else 25
    num_pages = math.ceil(num_repos / max_per_page)
    page = 1
    cursor = ""

    while page <= num_pages:
        graphql_query = get_query(max_per_page, cursor)

        result = run_query(graphql_query)
        page_repos = result["data"]["search"]["edges"]
        if not page_repos:
            break

        repos.extend(page_repos)
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        page += 1

    return repos
