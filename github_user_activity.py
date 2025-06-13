import requests

# Base URL for GitHub API
base_url = "https://api.github.com"

# Personal Access Token for GitHub API (Replace with env variable for safety in production)
api_token = "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"

def get_user_info(username):
    """
    Sends a GET request to fetch recent public events for the given GitHub username.
    """
    header = {
        "Authorization": f"token {api_token}"  # Auth header using personal access token
    }
    url = base_url + f"/users/{username}/events"
    response = requests.get(url, headers=header)
    return response


# Base class for all event types
class Event():
    def __init__(self, repo_name):
        self.repo_name = repo_name


# Class to represent PushEvent
class PushEvent(Event):
    def __init__(self, repo_name, commits_info):
        super().__init__(repo_name)
        self.num_of_commits = len(commits_info)  # Count the number of commits

    @classmethod
    def summarize(cls, push_events):
        """
        Summarizes commit counts per repository and total.
        """
        summary = {}
        count = 0
        for event in push_events:
            repo_name = event.repo_name
            summary[repo_name] = event.num_of_commits + summary.get(repo_name, 0)
            count += event.num_of_commits
        return summary, count 

    def __str__(self):
        return f"Pushed {self.num_of_commits} commits to {self.repo_name}"


# Class to represent PullRequestEvent
class PullEvent(Event):
    def __init__(self, repo_name, action):
        super().__init__(repo_name)
        self.action = action  # e.g., opened, closed, etc.

    @classmethod
    def summarize(cls, pull_events):
        """
        Summarizes pull request actions (opened, closed) per repository.
        """
        summary = {}
        count = 0
        for event in pull_events:
            repo = event.repo_name
            action = event.action
            summary[repo] = summary.get(repo, {})
            summary[repo][action] = summary[repo].get(action, 0) + 1
            count += 1
        return summary, count

    def __str__(self):
        return f"Pull request {self.action} to {self.repo_name}"


# Class to represent IssuesEvent
class IssueEvent(Event):
    def __init__(self, repo_name, action):
        super().__init__(repo_name)
        self.action = action  # e.g., opened, closed

    @classmethod
    def summarize(cls, issue_events):
        """
        Summarizes issue actions (opened, closed) per repository.
        """
        summary = {}
        count = 0
        for event in issue_events:
            repo = event.repo_name
            action = event.action
            summary[repo] = summary.get(repo, {})
            summary[repo][action] = summary[repo].get(action, 0) + 1
            count += 1
        return summary, count

    def __str__(self):
        return f"{self.action} an issue to {self.repo_name}"


# Class to represent ForkEvent
class ForkedEvent(Event):
    def __init__(self, source_repo, forked_repo):
        super().__init__(source_repo)
        self.source_repo = source_repo
        self.forked_repo = forked_repo

    def __str__(self):
        return f"Forked {self.source_repo} --> {self.forked_repo}"


# Class to represent WatchEvent (i.e., starred repositories)
class WatchEvent(Event):
    def __init__(self, repo_name, starred_by):
        super().__init__(repo_name)
        self.starred_by = starred_by

    def __str__(self):
        return f"{self.starred_by} starred {self.repo_name}"


# Validator for user input to ensure only y/n is accepted
def choice_validator(choice):
    while choice.lower() not in ("y", "n"):
        choice = input("Invalid choice! Please choose from the following only (y/n): ")
    return choice


# Validator to prompt for valid GitHub username until response is successful
def username_validator(api_response):
    while api_response.status_code != 200:
        username = input("Invalid! Pls enter a valid GitHub username: ")
        api_response = get_user_info(username)
    return api_response


# Main program logic
def main():
    choice = "y"
    while choice.lower() == "y":
        print("-" * 60)
        print(f"{'Welcome to the GitHub User Activity Tracker':^60s}")
        print("-" * 60)
        print()

        # Lists to store different types of events
        push_events = []
        pull_events = []
        issue_events = []
        forked_events = []
        watch_events = []

        # Prompt user for GitHub username
        github_username = input("Enter the username of the GitHub user you want to track: ")
        response = get_user_info(github_username)
        valid_response = username_validator(response).json()

        # Parse each event and categorize based on type
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

        # === OUTPUT SECTION ===

        # PushEvent Summary
        push_events_summary, total_push = PushEvent.summarize(push_events)
        print(f"Pushed {total_push} commits to {len(push_events_summary)} repos")
        for repo in push_events_summary:
            print(f"\t-- Pushed {push_events_summary.get(repo, 0)} commits to {repo}")

        # PullEvent Summary
        pull_events_summary, total_pull = PullEvent.summarize(pull_events)
        print(f"\nOpened {total_pull} pull requests in {len(pull_events_summary)} repos")
        for repo in pull_events_summary:
            for action, num in pull_events_summary[repo].items():
                print(f"\t-- {num} pull requests {action} in {repo}")

        # IssueEvent Summary
        issue_events_summary, total_issue = IssueEvent.summarize(issue_events)
        print(f"\nHandled {total_issue} event issues in {len(issue_events_summary)} repos")
        for repo in issue_events_summary:
            for action, num in issue_events_summary[repo].items():
                print(f"\t-- {action} {num} issues in {repo}")

        # ForkedEvent Output
        print(f"\nForked {len(forked_events)} repos")
        for event in forked_events:
            print(f"\t-- {event}")

        # WatchEvent Output
        print(f"\nWatched {len(watch_events)} repos")
        for event in watch_events:
            print(f"\t-- {event}")

        # Ask if user wants to track another GitHub account
        choice = input("\nWould you like to continue and track another user's GitHub activity? (y/n): ")
        choice = choice_validator(choice)

    # Exit message
    print("\nTHANK YOU FOR USING GITHUB USER ACTIVITY PROGRAM! Exiting...")


# Entry point
if __name__ == "__main__":
    main()
