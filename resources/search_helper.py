from .models import Data, Publication
from django.db.models import Q

def search_data(query):
    """ Searches both data and publications and then data again with publications and then combines and filters out duplicates """

    lookups = \
    Q(run_accession__icontains=query) | \
    Q(sample_type__icontains=query) | \
    Q(data_type__icontains=query) | \
    Q(location__icontains=query) | \
    Q(animal__icontains=query) | \
    Q(antibiotics__icontains=query) | \
    Q(host__icontains=query) | \
    Q(diet__icontains=query) | \
    Q(target_region_16s__icontains=query)

    pub_lookups = Q(authors__icontains=query) | Q(title__icontains=query) | Q(doi__icontains=query)
    pub_results = Publication.objects.filter(pub_lookups)
    more_results = Data.objects.filter(publication__in=pub_results)
    print(more_results)

    results = Data.objects.filter(lookups)
    results = results | more_results
    results = results.distinct()


    
    return results

def search_publications(query):
    lookups = Q(title__icontains=query) | Q(authors__icontains=query) | Q(doi__icontains=query) | Q(date__icontains=query)
    results = Publication.objects.filter(lookups).distinct()
    return results