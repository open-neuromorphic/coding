import os
import re

from github import Github
from github import Auth

AUTH_TOKEN = Auth.Token(os.environ["GITHUB_TOKEN"])
REGEX = r"^<!-- (.*) -->[\s\S]*<!-- \1 -->"

def regex_replace(repo):
  return rf"^(<!-- {repo} -->)([\s\S]*)^(<!-- {repo} -->)"

def issue_text(issue):
  return f"""* [{issue.title}]({issue.html_url})"""

g = Github(auth=AUTH_TOKEN)

# Extract repos
repos = []
with open("README.md", "r") as f:
  text = f.read()
  match = re.findall(REGEX, text, re.MULTILINE | re.UNICODE | re.DOTALL)
  if match is not None and len(match) > 0:
    repos = match
  else:
    print("No repos found")
    exit(-1)

# Scrape repos
for repo in repos:
  repo_object = g.get_repo(repo)
  issues = repo_object.get_issues(state="open", labels=["help wanted"])
  text_issues = "\n"
  for issue in issues:
    text_issues += issue_text(issue) + "\n"
  with open(f"README.md", "r") as f:
    text = f.read()

  with open(f"README.md", "w") as f:
    sub = re.sub(regex_replace(repo), rf"\1{text_issues}\3", text, flags=re.MULTILINE)
    f.write(sub)
