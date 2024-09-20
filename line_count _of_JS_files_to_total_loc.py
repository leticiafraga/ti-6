import requests
import csv 

GITHUB_TOKEN = '' 
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}
REPOSITORIES = ['ant-design/ant-design']

def count_lines_of_code(owner, repo_name, path=''):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        contents = response.json()
        total_js_ts_lines = 0
        js_lines = 0
        for item in contents:
            print(f"Processando: {item['name']}") 
            
            if item['type'] == 'file':
                file_url = item['download_url']
                file_response = requests.get(file_url)
                
                if file_response.status_code == 200:
                    lines = file_response.text.splitlines()
                    
                    if item['name'].endswith(('.js', '.ts', '.jsx', '.tsx')):
                        total_js_ts_lines += len(lines)
                        print(f"Arquivo JS/TS/JSX/TSX encontrado: {item['name']} - Linhas: {len(lines)}")
                    
                    if item['name'].endswith('.js'):
                        js_lines += len(lines)
                        print(f"Arquivo .js encontrado: {item['name']} - Linhas .js: {len(lines)}")

            elif item['type'] == 'dir':
                sub_total_js_ts, sub_js = count_lines_of_code(owner, repo_name, item['path'])
                total_js_ts_lines += sub_total_js_ts
                js_lines += sub_js
                
        return total_js_ts_lines, js_lines
    else:
        print(f"Erro ao buscar conteúdo do repositório: {response.status_code}, {response.text}")
        return 0, 0

def save_results_to_csv(results, filename='loc_results.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Repositório', 'Total LOC JS/TS/JSX/TSX', 'LOC .js']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for repo, data in results.items():
            total_js_ts_loc, js_loc = data
            writer.writerow({'Repositório': repo, 'Total LOC JS/TS/JSX/TSX': total_js_ts_loc, 'LOC .js': js_loc})

results = {}
for repo in REPOSITORIES:
    owner, name = repo.split('/')
    try:
        print(f"Processando repositório: {repo}") 
        total_js_ts_loc, js_loc = count_lines_of_code(owner, name)
        results[repo] = (total_js_ts_loc, js_loc)
        print(f"Repositório: {repo} - Total LOC JS/TS/JSX/TSX: {total_js_ts_loc}, LOC .js: {js_loc}")
    except Exception as e:
        print(f"Erro ao processar {repo}: {e}")

save_results_to_csv(results)
print("Resultados salvos em loc_results.csv")

