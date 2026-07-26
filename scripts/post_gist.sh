#!/bin/bash
# Post a snippet to GitHub Gist and register it in the gist wall
# Usage: ./post_gist.sh <category> <filename> <description> <content_file>

CATEGORY="$1"
FILENAME="$2"
DESCRIPTION="$3"
CONTENT_FILE="$4"

if [ -z "$CATEGORY" ] || [ -z "$FILENAME" ] || [ -z "$DESCRIPTION" ] || [ -z "$CONTENT_FILE" ]; then
    echo "Usage: $0 <category> <filename> <description> <content_file>"
    exit 1
fi

CONTENT=$(cat "$CONTENT_FILE")

GIST_RESPONSE=$(curl -sL -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://api.github.com/gists" \
  -d "$(python3 -c "
import json
with open('$CONTENT_FILE') as f:
    content = f.read()
payload = {
    'description': '$DESCRIPTION',
    'public': False,
    'files': {'$FILENAME': {'content': content}}
}
print(json.dumps(payload))
")")

GIST_ID=$(echo "$GIST_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))")
GIST_URL=$(echo "$GIST_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('html_url',''))")

if [ -n "$GIST_ID" ]; then
    echo "Posted gist: $GIST_URL"
    python3 -c "
import json
with open('gists/gist_wall.json') as f:
    wall = json.load(f)
wall['gists'].append({
    'id': '$GIST_ID',
    'url': '$GIST_URL',
    'filename': '$FILENAME',
    'category': '$CATEGORY',
    'description': '$DESCRIPTION',
    'timestamp': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
})
with open('gists/gist_wall.json', 'w') as f:
    json.dump(wall, f, indent=2)
"
else
    echo "Failed to create gist"
    echo "$GIST_RESPONSE"
fi
