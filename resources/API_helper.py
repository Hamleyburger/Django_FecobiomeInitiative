
import requests
from datetime import datetime


def get_biorxiv_meta(instance, doi):
    """ Takes the instance to be modified and a *url encoded* doi string\n
    and either adds metadata to instance or raises an error """
    api = requests.get(
        "https://api.biorxiv.org/details/biorxiv/" + doi).json()

    # connection to bioarchives was succesful. Get collection (specific to bioarchives)
    # -1 gives last item which is latest version in collection if multiple
    if api["collection"]:
        metadata = api["collection"][-1]
        instance.title = metadata["title"]
        instance.authors = metadata["authors"]
        instance.date = datetime.strptime(metadata["date"], '%Y-%m-%d')
        instance.type = "preprint"
    else:
        raise Exception("Invalid DOI")


def get_pubmed_meta(instance, doi):

    # Get UID from doi for querying PUBMED API with UID
    conversion_api_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=thefecobiomeinitiative&email=alma9000@gmail.com&ids={}&format=json".format(
        doi)
    conversion_result = requests.get(conversion_api_url).json()
    PMCID = conversion_result["records"][0]["pmcid"] if conversion_result else None
    UID = PMCID.replace("PMC", "")

    # Get metadata from UID
    metadata_api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id={}&retmode=json&tool=%22thefecobiomeinitiative%22&email=alma9000@gmail.com".format(
        UID)
    API_response = requests.get(metadata_api_url).json()
    result = API_response["result"][UID]

    # Title
    title = result["title"]

    # Authors (extract and convert)
    authorlist = result["authors"]
    authors = ""
    first = True
    for entry in authorlist:
        if not first:
            authors = authors + "; "
        else:
            first = False
        authors = authors + entry["name"]

    # Date
    date_string = result["pubdate"]
    date = datetime.strptime(date_string, '%Y %b %d')

    # Populate
    instance.title = title
    instance.authors = authors
    instance.date = date
    instance.type = "peer-reviewed"
