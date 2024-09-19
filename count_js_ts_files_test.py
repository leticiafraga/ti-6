from static_analysis import *
import glob

def count_js_ts_files_test():
    name = 'vscode'
    repo_path =  CLONED_REPOS_PATH + "/" + name
    print(repo_path)
    
    # ls -R repos/vscode/ | grep '\.js$' | wc -l
    js_files = glob.glob(repo_path + "/**/*.js", recursive=True)
    ts_files = glob.glob(repo_path + "/**/*.ts", recursive=True)

    print(js_files)
    
    print(f".js files: {len(js_files)}")
    print(f".ts files: {len(ts_files)}")