
import requests
from datetime import datetime


def get_pubmed_meta(instance, doi):
    """ API call to PubMed to get metadata for publication """

    try:
        print("PubMed trying to get id and meta from doi")
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
    except:
        try:
            get_fatcat_meta(instance, doi)
        except Exception as e:
            raise e


def get_fatcat_meta(instance, doi):
    """ FatCat API call to get publication metadata for articles where PubMeds API fails"""
    print("FatCat trying to get PubMed meta because PubMeds API is faulty")
    metadata_api_url = "https://api.fatcat.wiki/v0/release/lookup?doi={}".format(
        doi)
    API_response = requests.get(metadata_api_url).json()

    # Get authors
    first = True
    authors = ""
    for dude in API_response["contribs"]:
        if dude["role"] == "author":
            if not first:
                authors = authors + "; "
            else:
                first = False
            authors = authors + dude["raw_name"]

    # Get "date"
    year = API_response["release_year"]
    date = datetime(year, 1, 1)

    # Get title
    title = API_response["title"]

    instance.title = title
    instance.authors = authors
    instance.date = date
    instance.type = "peer-reviewed"


def get_biorxiv_meta(instance, doi):
    """ Checks id a doi that did not pass PubMed or FatCats API calls\n
    to see if it's a preprint and get metadata """
    print("biorxiv trying to get doi from api")
    api = requests.get(
        "https://api.biorxiv.org/details/biorxiv/" + doi).json()

    # connection to bioarchives was succesful. Get collection (specific to bioarchives)
    # -1 gives last item which is latest version in collection if multiple
    if api["collection"]:
        metadata = api["collection"][-1]
        try:
            instance.title = metadata["title"]
            instance.authors = metadata["authors"]
            instance.date = datetime.strptime(metadata["date"], '%Y-%m-%d')
            instance.type = "preprint"
        except Exception as e:
            raise e

    else:
        raise Exception("doi does not have a 'collection' - either article does not exist in biorxiv or doi is faulty")


def clean_doi(doi):
    """ Remove ' ' and '.' from end of doi. \n
    doi needs to be cleaned before entering database and before any given check """
    check = True
    while check:
        if doi.endswith(" "):
            doi = doi.rstrip()
        elif doi.endswith("."):
            doi = doi.removesuffix(".")
        else:
            check = False
    return doi
