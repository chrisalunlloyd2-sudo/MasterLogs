#!/usr/bin/env python3
"""
MasterLogs Dream Engine — auto-populates logs, gists, and documentation
Runs as part of nightly dream rounds.

Collects:
- Dependency trees from all repos
- Runtime errors from GitHub Actions
- KV store snapshots
- Keyword lists
- LoRA training checkpoints
- Logit keystrokes
- Posts everything as gists
"""

import json
import os
import subprocess
import sys
from datetime import datetime

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPOS = [
    'chrisalunlloyd2-sudo/ViperKernel',
    'chrisalunlloyd2-sudo/MoeGUI',
    'chrisalunlloyd2-sudo/GeneticFoundry',
    'chrisalunlloyd2-sudo/Plane2d',
    'chrisalunlloyd2-sudo/ArchivalMoe',
    'chrisalunlloyd2-sudo/ViperNote',
    'chrisalunlloyd2-sudo/mind-palace',
    'chrisalunlloyd2-sudo/MasterLogs',
]

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def write_text(path, content):
    """Write text to path, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def fetch_dependency_tree(repo):
    """Fetch dependency files from a repo"""
    deps = {}
    for file in ['requirements.txt', 'package.json', 'Cargo.toml', 'go.mod', 'pyproject.toml']:
        out, _, _ = run(f"curl -sL -H 'Authorization: Bearer {GITHUB_TOKEN}' "
                       f"'https://api.github.com/repos/{repo}/contents/{file}' | "
                       f"python3 -c \"import json,sys; d=json.load(sys.stdin); print(d.get('content',''))\" 2>/dev/null")
        if out:
            import base64
            try:
                deps[file] = base64.b64decode(out).decode('utf-8')
            except:
                deps[file] = out
    return deps

def fetch_workflow_runs(repo):
    """Fetch recent workflow runs and their errors"""
    out, _, _ = run(f"curl -sL -H 'Authorization: Bearer {GITHUB_TOKEN}' "
                   f"'https://api.github.com/repos/{repo}/actions/runs?per_page=5'")
    try:
        data = json.loads(out)
        runs = []
        for run_data in data.get('workflow_runs', []):
            runs.append({
                'name': run_data.get('name'),
                'conclusion': run_data.get('conclusion'),
                'status': run_data.get('status'),
                'html_url': run_data.get('html_url'),
                'created_at': run_data.get('created_at'),
            })
        return runs
    except:
        return []

def post_gist(category, filename, content, description):
    """Post content as a GitHub Gist"""
    if not GITHUB_TOKEN:
        return None
    
    payload = json.dumps({
        'description': description,
        'public': False,
        'files': {filename: {'content': content}}
    })
    
    out, _, _ = run(f"curl -sL -H 'Authorization: Bearer {GITHUB_TOKEN}' "
                   f"-H 'Content-Type: application/json' "
                   f"-X POST 'https://api.github.com/gists' "
                   f"-d '{payload}'")
    
    try:
        data = json.loads(out)
        gist_id = data.get('id', '')
        gist_url = data.get('html_url', '')
        
        if gist_id:
            # Register in gist wall
            wall_path = 'gists/gist_wall.json'
            if os.path.exists(wall_path):
                with open(wall_path) as f:
                    wall = json.load(f)
                wall['gists'].append({
                    'id': gist_id,
                    'url': gist_url,
                    'filename': filename,
                    'category': category,
                    'description': description,
                    'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                })
                with open(wall_path, 'w') as f:
                    json.dump(wall, f, indent=2)
            
            return gist_url
    except:
        pass
    return None

def snapshot_kv():
    """Snapshot KV store data (placeholder — reads from SOV KV)"""
    # In production, this reads from /root/sov/kv/data.json
    kv_path = '/root/sov/kv/data.json'
    if os.path.exists(kv_path):
        with open(kv_path) as f:
            return f.read()
    return "KV store not accessible from this context"

def snapshot_keywords():
    """Snapshot global keyword list"""
    # In production, reads from SOV memory
    return json.dumps({
        'timestamp': datetime.utcnow().isoformat(),
        'note': 'Keyword list snapshot — populated by dream engine',
        'keywords': []
    }, indent=2)

def main():
    print(f"=== MasterLogs Dream Engine — {datetime.utcnow().isoformat()} ===")
    
    for repo in REPOS:
        repo_name = repo.split('/')[-1]
        print(f"\n--- Processing {repo_name} ---")
        
        # 1. Fetch dependency tree
        deps = fetch_dependency_tree(repo)
        if deps:
            dep_content = '\n\n'.join([f"### {f}\n```\n{c}\n```" for f, c in deps.items()])
            dep_path = f"projects/{repo_name}/dependencies.md"
            write_text(dep_path, f"# {repo_name} — Dependencies\n\n{dep_content}\n\n*Auto-updated: {datetime.utcnow().isoformat()}*")
            print(f"  Dependencies saved to {dep_path}")
            
            # Post as gist
            url = post_gist('snippet', f'{repo_name}_deps.md', dep_content, f'{repo_name} dependency tree')
            if url:
                print(f"  Gist posted: {url}")
        
        # 2. Fetch workflow errors
        runs = fetch_workflow_runs(repo)
        if runs:
            failed = [r for r in runs if r.get('conclusion') == 'failure']
            if failed:
                error_content = '\n\n'.join([
                    f"- **{r['name']}** ({r['created_at']}): {r['html_url']}"
                    for r in failed
                ])
                error_path = f"projects/{repo_name}/errors.md"
                write_text(error_path, f"# {repo_name} — Runtime Errors\n\n{error_content}\n\n*Auto-updated: {datetime.utcnow().isoformat()}*")
                print(f"  Errors saved to {error_path}")
                
                url = post_gist('error', f'{repo_name}_errors.md', error_content, f'{repo_name} runtime errors')
                if url:
                    print(f"  Gist posted: {url}")
    
    # 3. Snapshot KV store
    kv_data = snapshot_kv()
    kv_path = f"kv_snapshots/snapshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    write_text(kv_path, kv_data)
    print(f"\nKV snapshot saved to {kv_path}")
    
    url = post_gist('kv', f'kv_snapshot_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json', kv_data, 'KV store snapshot')
    if url:
        print(f"KV gist posted: {url}")
    
    # 4. Snapshot keywords
    kw_data = snapshot_keywords()
    kw_path = f"keywords/keywords_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    write_text(kw_path, kw_data)
    print(f"Keyword snapshot saved to {kw_path}")
    
    url = post_gist('keyword', f'keywords_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json', kw_data, 'Keyword list snapshot')
    if url:
        print(f"Keyword gist posted: {url}")
    
    print("\n=== Dream Engine Complete ===")

if __name__ == '__main__':
    main()
