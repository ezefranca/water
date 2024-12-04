import requests
from bs4 import BeautifulSoup

# Constants
BASE_URL = "https://yazioen.featureupvote.com"
VOTE_URL = f"{BASE_URL}/s/92880/vote"
SUGGESTION_URL = f"{BASE_URL}/suggestions/92880/read-water-from-ios-apple-health-app"

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": SUGGESTION_URL,
}

def get_csrf_token(session):
    """Fetch the CSRF token from the suggestion page."""
    response = session.get(SUGGESTION_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_input = soup.find("button", class_="btn-upvote")
    
    if not csrf_input or "hx-vals" not in csrf_input.attrs:
        raise ValueError("CSRF token not found.")
    
    # Extract CSRF token from the hx-vals attribute
    hx_vals = csrf_input["hx-vals"]
    csrf_token = hx_vals.split("csrf_token")[1].split(":")[1].split(",")[0].strip('"')
    return csrf_token

def vote(session, csrf_token):
    """Submit the vote."""
    payload = {
        "csrf_token": csrf_token,
        "showVotingOptions": "true",
    }
    response = session.post(VOTE_URL, headers=HEADERS, data=payload)
    if response.status_code == 200:
        print("Vote successful!")
    else:
        print(f"Failed to vote. Status code: {response.status_code}")
        print(response.text)

def main():
    # Use a session to persist cookies and headers
    with requests.Session() as session:
        try:
            csrf_token = get_csrf_token(session)
            print(f"CSRF Token: {csrf_token}")
            vote(session, csrf_token)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
