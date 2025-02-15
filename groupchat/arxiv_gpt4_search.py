# filename: arxiv_gpt4_search.py
import feedparser
import requests

# Define the base URL for the arXiv API
ARXIV_API_URL = "http://export.arxiv.org/api/query?"

# Construct the query parameters
query_params = {
    "search_query": "all:GPT-4",
    "sortBy": "submittedDate",
    "sortOrder": "descending",
    "max_results": "1"
}

# Perform the GET request
response = requests.get(ARXIV_API_URL, params=query_params)
feed = feedparser.parse(response.content)

# Check if there are entries returned
if len(feed.entries) == 0:
    print("No papers found related to GPT-4 on arXiv.")
else:
    # Get the latest entry
    latest_paper = feed.entries[0]

    # Print the relevant details of the paper
    print(f"Title: {latest_paper.title}")
    print(f"Authors: {', '.join(author.name for author in latest_paper.authors)}")
    print(f"Published Date: {latest_paper.published}")
    print(f"Summary: {latest_paper.summary}")
    print(f"Link: {latest_paper.link}")

# Let's extract the summary and look for potential applications in software
    summary = latest_paper.summary
    applications_lines = [line for line in summary.split('\n') if 'application' in line.lower() or 'software' in line.lower()]
    print("\nPotential applications in software mentioned in the summary:")
    for line in applications_lines:
        print(line)