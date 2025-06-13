import requests
base_url = "https://api.github.com"
api_token = "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"

def get_user_info(username):
  header = {
    "Authorization": f"token {api_token}" # Preparing a header for GitHub api token
  }
  url = base_url + f"/users/{username}/events"
  response = requests.get(url, headers=header)
  return response

class Event():
  def __init__(self, repo_name):
    self.repo_name = repo_name
    
class PushEvent(Event):
  def __init__(self, repo_name, commits_info):
    super().__init__(repo_name)
    self.num_of_commits = len(commits_info)  # calculates number of commits

  @classmethod
  def summarize(cls, push_events):
    summary = {}
    count = 0
    for event in push_events:
      repo_name = event.repo_name
      summary[repo_name] = event.num_of_commits + summary.get(repo_name, 0)  # Add commit count to repo total, starting from 0 if it's the first entry
      count = count + event.num_of_commits
    return summary, count 

  def __str__(self):
    return f"Pushed {self.num_of_commits} commits to {self.repo_name}"

class PullEvent(Event):
  def __init__(self, repo_name, action):
    super().__init__(repo_name)
    self.action = action
    
  @classmethod
  def summarize(cls, pull_events):
    summary = {}
    count = 0
    for event in pull_events:
      repo = event.repo_name
      action = event.action
      summary[repo] = summary.get(repo, {})             # Get the nested action dict, or a new one if not present
      summary[repo][action] = summary[repo].get(action, 0) + 1  # It increments the correct action without removing other actions under the same repo.
      count += 1
    return summary, count
    
  def __str__(self):
    return f"Pull request {self.action} to {self.repo_name}"
  
class IssueEvent(Event):
  def __init__(self, repo_name, action):
    super().__init__(repo_name)
    self.action = action
    
  @classmethod
  def summarize(cls, issue_events):
    summary = {}
    count = 0
    for event in issue_events:
      repo = event.repo_name
      action = event.action
      summary[repo] = summary.get(repo, {})             # Checks if this repo already exists in the summary dictionary or returns {} for a new repo
      summary[repo][action] = summary[repo].get(action, 0) + 1  # It increments the correct action without removing other actions under the same repo.
      count += 1
    return summary, count
  
  def __str__(self):
    return f"{self.action} an issue to {self.repo_name}"

class ForkedEvent(Event):
  def __init__(self, source_repo, forked_repo):
    super().__init__(source_repo)
    self.source_repo = source_repo
    self.forked_repo = forked_repo
  
  def __str__(self):
    return f"Forked {self.source_repo} --> {self.forked_repo}"
  
class WatchEvent(Event):
  def __init__(self, repo_name, starred_by):
    super().__init__(repo_name)
    self.starred_by = starred_by
    
  def __str__(self):
    return f"{self.starred_by} starred {self.repo_name}"
  
def choice_validator(choice):
  while choice.lower() not in ("y", "n"):
    choice = input("Invalid choice! Please choose from the following only (y/n): ")
  return choice
  
def username_validator(api_response):
  while api_response.status_code != 200:
    username = input("Invalid! Pls enter a valid GitHub username: ")
    api_response = get_user_info(username)
  return api_response
    

def main():
  choice = "y"
  while choice.lower() == "y":
    print("-" * 60)
    print(f"{"Welcome to the GitHub User Activity Tracker":^60s}")
    print("-" * 60)
    print()
    
    push_events = []
    pull_events = []
    issue_events = []
    forked_events = []
    watch_events = []
    
    github_username = input("Enter the username of the GitHub user you want to track: ")
    response = get_user_info(github_username)
    valid_response = username_validator(response).json()
    
    for i in valid_response:
      if i["type"] == "PushEvent":
        repo = i.get("repo", {}).get("name")
        commits_info = i.get("payload", {}).get("commits", [])
        event_obj = PushEvent(repo, commits_info)
        push_events.append(event_obj)
      elif i["type"] == "PullRequestEvent":
        repo = i.get("repo", {}).get("name")
        action = i.get("payload", {}).get("action", "")
        event_obj = PullEvent(repo, action)
        pull_events.append(event_obj)
      elif i["type"] == "IssuesEvent":
        repo = i.get("repo", {}).get("name")
        action = i.get("payload", {}).get("action", "")
        event_obj = IssueEvent(repo, action)
        issue_events.append(event_obj)
      elif i["type"] == "ForkEvent":
        source_repo = i.get("repo", {}).get("name")
        forked_repo = i.get("payload", {}).get("forkee", {}).get("full_name", "")
        event_obj = ForkedEvent(source_repo, forked_repo)
        forked_events.append(event_obj)
      elif i["type"] == "WatchEvent":
        repo = i.get("repo", {}).get("name")
        starred_by = i.get("actor", {}).get("login", "")
        event_obj = WatchEvent(repo, starred_by)
        watch_events.append(event_obj)
      
    # Printing summary of push events
    push_events_summary, total_push = PushEvent.summarize(push_events)
    print(f"Pushed {total_push} commits to {len(push_events_summary)} repos")
    for repo in push_events_summary:
      print(f"\t-- Pushed {push_events_summary.get(repo, 0)} commits to {repo}")
    # Printing summary of pull events
    pull_events_summary, total_pull = PullEvent.summarize(pull_events)
    print(f"\nOpened {total_pull} pull requests in {len(pull_events_summary)} repos")
    for repo in pull_events_summary:
      for action, num in pull_events_summary[repo].items():
        print(f"\t-- {num} pull requests {action} in {repo}")
    # Printing summary of issue events
    issue_events_summary, total_issue = IssueEvent.summarize(issue_events)
    print(f"\nHandled {total_issue} event issues in {len(issue_events_summary)} repos")
    for repo in issue_events_summary:
      for action, num in issue_events_summary[repo].items():
        print(f"\t-- {action} {num} issues in {repo}")
    # Prinitng forked events
    print(f"\nForked {len(forked_events)} repos")
    for event in forked_events:
      print(f"\t-- {event}")
    # Prinitng watched events
    print(f"\nWatched {len(watch_events)} repos")
    for event in watch_events:
      print(f"\t-- {event}")
    choice = input("\nWould you like to continue and track another user's GitHub activity? (y/n): ")
    choice = choice_validator(choice)
  print("\nTHANK YOU FOR USING GITHUB USER ACTIVITY PROGRAM! Exiting...")

if __name__ == "__main__":
  main()