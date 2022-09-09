from .models import Data, Publication, Genome
from django.db.models import Q

def search_data(query):
    """ Searches both data and publications and then data again with publications and then combines and filters out duplicates """
    if not query:
        return []

    data_lookups = \
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

    data_results = Data.objects.filter(data_lookups)
    pub_results = Publication.objects.filter(pub_lookups)
    data_results_from_pub = Data.objects.filter(publication__in=pub_results)

    data_results = data_results | data_results_from_pub
    data_results = data_results.distinct()

    return data_results

def search_publications(query):
    if not query:
        return []

    lookups = Q(title__icontains=query) | Q(authors__icontains=query) | Q(doi__icontains=query) | Q(date__icontains=query)
    results = Publication.objects.filter(lookups).distinct()
    return results

def search_genomes(query):
    """ Searches in genomes """
    if not query:
        return []

    genome_lookups = \
    Q(unique_id__icontains=query) | \
    Q(closest_rel_alt_name__icontains=query) | \
    Q(phyl_class__icontains=query) | \
    Q(original_sample__icontains=query) | \
    Q(country__icontains=query) | \
    Q(dRep_secondary_cluster__icontains=query) | \
    Q(source__icontains=query) | \
    Q(latest_doi__icontains=query)


    pub_lookups = Q(authors__icontains=query) | Q(title__icontains=query) | Q(doi__icontains=query)

    genome_results = Genome.objects.filter(genome_lookups)
    pub_results = Publication.objects.filter(pub_lookups)
    genome_results_from_pub = Genome.objects.filter(publication__in=pub_results)

    genome_results = genome_results | genome_results_from_pub
    genome_results = genome_results.distinct()

    return genome_results
