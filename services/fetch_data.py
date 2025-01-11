import requests
import logging

def fetch_github_releases(repo):
    """
    Fetches the latest release data from a GitHub repository.
    :param repo: Repository in the format "owner/repo".
    :return: Tuple of (title, content) if found, else None.
    """
    try:
        url = f"https://api.github.com/repos/{repo}/releases"
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()
        if releases:
            latest = releases[0]
            return latest['name'], latest['body'][:500]  # Limit content to 500 chars
        else:
            logging.warning(f"No releases found for repository: {repo}")
            return None, None
    except Exception as e:
        logging.error(f"Error fetching data from GitHub: {e}")
        return None, None
