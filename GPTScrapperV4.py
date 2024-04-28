from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models.openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

def web_qa(url_list, query, output_file="output.txt"):
    """
    Perform web-based question answering on a list of URLs using a specified query.

    Args:
        url_list (list): A list of URLs to extract information from.
        query (str): The query to search for within the web pages.
        output_file (str, optional): The file path to save the results. Default is "output.txt".

    Returns:
        None
    """
    openai = ChatOpenAI(
        model_name="gpt-4",
        max_tokens=4000 # Change this if you want a longer response
    )
    
    with open(output_file, "w") as file:
        for url in url_list:
            print("loading url: %s" % url)
            loader = WebBaseLoader(url)
            index = VectorstoreIndexCreator().from_loaders([loader])  
            ans = index.query(query)
            file.write(f"Results for URL: {url}\n")
            file.write(ans + "\n\n")

    print("Results saved to:", output_file)

url_list = [
    "https://en.wikipedia.org/wiki/2016_Kyiv_cyberattack","https://attack.mitre.org/groups/G0034/",
    "https://csrc.nist.gov/nist-cyber-history/tech-infrastructure/chapter"
]

prompt = """
Give me a one page esaay please provide the following: 
1. Summary of what happened
2. Summary of the most important information
3. Summary of how things were fixed
4. Summary of how to prevent the issue 
"""

web_qa(url_list, prompt, "output.txt")
