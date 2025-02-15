import requests
import time
from datetime import datetime, timedelta

# Define the search parameters
keywords = ["transformer", "BERT", "GPT", "large language model"]  # example keywords
domains = {
    "healthcare": ["health", "medical", "clinic"],
    "education": ["education", "learning", "teaching"],
    "finance": ["finance", "banking", "economic"],
    # Include more domain keywords as necessary
}
search_query = f'({" OR ".join(keywords)}) AND cat:cs.CL'  # focusing on Computation and Language (cs.CL)
time_frame = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d%H%M%S')

# Function to query the arXiv API and return the response
def query_arxiv(search_query, time_frame):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 50,  # Adjusted based on expected volume
    }
    response = requests.get(url, params=params)
    return response

# Function to organize paper metadata by domain
def categorize_by_domain(entry, domains):
    for domain, keywords in domains.items():
        if any(keyword.lower() in entry['summary'].lower() for keyword in keywords):
            return domain
    return "other"

# Query arXiv
response = query_arxiv(search_query, time_frame)
response.raise_for_status()  # Check if the request was successful

# Parse the response and extract metadata
entries = response.json()['feed']['entry'] if isinstance(response.json()['feed']['entry'], list) else [response.json()['feed']['entry']]
papers = []

for entry in entries:
    published_time = datetime.strptime(entry['published'], "%Y-%m-%dT%H:%M:%SZ")
    if published_time < datetime.now() - timedelta(days=7):
        continue  # Skip papers not within the last week
    paper = {
        "title": entry['title'].strip(),
        "authors": ", ".join(author['name'] for author in entry['authors']),
        "published": published_time.strftime("%Y-%m-%d"),
        "domain": categorize_by_domain(entry, domains),
        "url": entry['id']
    }
    papers.append(paper)

# Sort papers into domains
domain_papers = {domain: [] for domain in domains}
domain_papers["other"] = []  # for papers that don't fit into predefined domains
for paper in papers:
    domain_papers[paper['domain']].append(paper)

# Create a markdown table for each domain
for domain, papers in domain_papers.items():
    if papers:  # Only process if there are papers in the domain
        markdown_table = f"### Domain: {domain}\n\n"
        markdown_table += "| Title | Authors | Published | URL |\n"
        markdown_table += "| --- | --- | --- | --- |\n"

        for paper in papers:
            markdown_table += f"| {paper['title']} | {paper['authors']} | {paper['published']} | [Link]({paper['url']}) |\n"

        # This is where you would normally output the markdown_table,
        # but due to execution constraints in this environment, we will not display it