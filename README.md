# 📊 GitHub User Activity Tracker (Python CLI Tool)

The **GitHub User Activity Tracker** is a beginner-friendly, Python-based command-line interface (CLI) application that fetches and neatly summarizes a GitHub user's **recent public activity** using the GitHub REST API. The project is designed to reinforce concepts such as **API consumption**, **object-oriented programming (OOP)**, **JSON handling**, and **CLI interaction**.

---

## 🚀 Overview

This tool provides a structured view of a GitHub user’s recent activity including:

- Commits pushed (PushEvent)
- Pull requests (PullRequestEvent)
- Issues opened or closed (IssuesEvent)
- Repository forks (ForkEvent)
- Starred repositories (WatchEvent)

Unlike the basic version, this version features **event summaries per repository**, error handling, and allows users to continuously monitor multiple GitHub accounts in a single session.

---

## 🎯 Project Goals

- 🧰 Practice REST API usage via `requests`
- 📦 Understand how to parse and manipulate JSON
- 🧠 Build an OOP-based structure for event handling
- 🖥️ Develop a user-friendly CLI interface
- ❌ Handle user errors and API limitations gracefully

---

## 🛠️ Features

- ✅ Clean and interactive command-line interface
- ✅ Summary generation for:
  - Push events (total commits per repo)
  - Pull request actions (opened/closed/merged)
  - Issues (opened/closed)
- ✅ Direct mapping of API JSON to OOP event objects
- ✅ Handles API errors and invalid usernames
- ✅ Easily extensible for more event types
- ✅ Allows continuous tracking of multiple users in one run
- ✅ Minimal dependencies (only `requests`)

---

## 📸 Sample Output

------------------------------------------------------------
        Welcome to the GitHub User Activity Tracker
------------------------------------------------------------

- Enter the username of the GitHub user you want to track: Riya-J05
- Pushed 14 commits to 2 repos
    -    -- Pushed 9 commits to Riya-J05/Task-Taker
    -    -- Pushed 5 commits to Riya-J05/hello-world

- Opened 4 pull requests in 2 repos
    -    -- 1 pull requests closed in Riya-J05/Task-Taker
    -    -- 1 pull requests opened in Riya-J05/Task-Taker
    -    -- 1 pull requests closed in Riya-J05/hello-world
    -    -- 1 pull requests opened in Riya-J05/hello-world

- Handled 0 event issues in 0 repos

- Forked 0 repos

- Watched 0 repos

- Would you like to continue and track another user's GitHub activity? (y/n): n

- THANK YOU FOR USING GITHUB USER ACTIVITY PROGRAM! Exiting...

---

## 🧑‍💻 How It Works

1. The user provides a GitHub username.
2. The program makes an API call to: https://api.github.com/users/<username>/events
3. It parses the response, identifies the event types, and:
- Creates event objects (`PushEvent`, `PullEvent`, `IssueEvent`, `ForkedEvent`, `WatchEvent`)
- Summarizes push/pull/issue activity
- Displays forked and starred repos
4. If the username is invalid or the API rate limit is hit, it prompts the user to try again.

---

## 📌 Limitations
- Fetches only the 30 most recent public events (API limit)
- Only tracks a subset of GitHub event types
- No data persistence or export options
- Not optimized for massive event history or enterprise usage

---

## ✅ Requirements

- Python 3.7+
- Internet connection
- GitHub personal access token (for stable use)
- requests module (pip install requests)

---

## 🙌 Acknowledgments

- This project is inspired by a beginner-level challenge listed on roadmap.sh, expanded with additional features and structure for better learning outcomes and real-world usability. Project link: https://roadmap.sh/projects/github-user-activity

---

## 📜 License
- This project is licensed under the MIT License.
  
---

## ✨ Author
- Made with ❤️ by Riya Johari

