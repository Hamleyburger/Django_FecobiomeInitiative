from datetime import datetime, date
from io import TextIOWrapper
from csv import DictReader, DictWriter
from tabnanny import check
from resources.API_helpers.publications import clean_doi


from django.contrib import messages
from .models import Data, Publication, Genome


class Feedback(dict):
    """ Just a dict with some handy methods for adding feedback to admin when uploading """

    def append_to_field_problems(self, unique_field, message):
        """ Return a feedback dict with status messages about problems with fields """
        if not self.get("field_problems"):
            self["field_problems"] = {}
        if not self["field_problems"].get(unique_field):
            self["field_problems"][unique_field] = []
        self["field_problems"][unique_field].append(message)
        return self

    def append_to_row_success(self, unique_field, message):
        """ Return a feedback dict with status messages about successful rows added """
        
        if not self.get("success"):
            self["success"] = {}
        if not self["success"].get(unique_field):
            self["success"][unique_field] = []
        self["success"][unique_field].append(message)
        return self

    def append_to_row_errors(self, unique_field, message):
        """ Return a feedback dict with status messages about invalid rows """
        
        if not self.get("invalid_rows"):
            self["invalid_rows"] = {}
        if not self["invalid_rows"].get(unique_field):
            self["invalid_rows"][unique_field] = []
        self["invalid_rows"][unique_field].append(message)
        return self
    
    def add_missing_header(self, header_name):
        if not self.get("missing_headers"):
            self["missing_headers"] = []
        self["missing_headers"].append(header_name)

            
        return self


def empty_row_filter(row):
    """ use in filter() to skip empty rows in table / CSV reader """

    hascontent = False
    for value in row.values():
        if isinstance(value, str):
            if value:
                if not value.isspace():
                    hascontent = True

    return hascontent

        

def tab_delimited_file(request):
    """ Returns CSV-reader for tab delimited file"""
    file = request.FILES["fileinput"]
    file_data = TextIOWrapper(file, encoding='utf-8', newline='')
    csv_reader = DictReader(file_data, delimiter="\t")
    return csv_reader


def empty_no_data_strings(row: dict):
    no_data_strings = ["na", "n/a", "unknown", "undefined"
                    "no data", "empty", "null", "none", 
                    "missing", "", " ", "\t"]
    for key, value in row.items():
        if value is not None:
            if value.lower() in no_data_strings:
                row[key] = ""
    return row


def validate_data_row_with_feedback(row: dict, all_headers: list, required_headers: list, row_number, feedback: Feedback):

    """ Checks that row is valid and a cell exists for each header\n
    Returns row if valid  """
    # Replace NA, 'unknown' etc with ""
    row = empty_no_data_strings(row)
    missing_cells = ""
    missing_required = ""

    valid_row = row
    empty_row = True
    for header in all_headers:
        if row[header] == None: # If there is no cell
            missing_cells = missing_cells + "<{}>  ".format(header)
            valid_row = None
        elif row[header]: # If there is data
            empty_row = False
    if empty_row: # None of the cells had data
        valid_row = None
        return valid_row

    if not valid_row: # If there was data in the row, but it was invalid
        feedback.append_to_row_errors(
            unique_field=row["run_accession"] if row.get("run_accession") else "with unknown run_accession in row {}".format(row_number + 1),
            message="Missing cells: {}".format(missing_cells)
            )
        return valid_row
    for header in required_headers:
        if not row[header]: # if value is an empty string
            missing_required = missing_required + "<{}>  ".format(header)
            valid_row = None


    if missing_required:
        feedback.append_to_row_errors(
            unique_field=row["run_accession"] if row.get("run_accession") else "unknown in row {}".format(row_number + 1),
            message="Missing required data: {}".format(missing_required)
        )

    return valid_row


def missing_headers(all_headers: list, table: dict, feedback: Feedback):
    missing = False
    for header in all_headers:
        if header not in table.fieldnames:
            feedback.add_missing_header(header)
            print(header)
            print("is missing")
            missing = True
    return missing


def formatted_number_or_None(value, type, string_name, unique_field, feedback):
    if value:
        try:
            result = type(value)
        except Exception as e:
            feedback.append_to_field_problems(
                unique_field=unique_field, 
                message="'{}' is an invalid format for '{}'".format(value, string_name)
                )
            result = None
    else:
        result = None
    return result


def formatted_date_or_None(sample_date_dmy, unique_field, feedback):
    if sample_date_dmy:
        date_formats = ["%d.%m.%Y", "%d-%m-%Y", "%d %m %Y"]
        success = False
        for format in date_formats:
            if not success:
                try:
                    sample_date_dmy = datetime.strptime(
                        sample_date_dmy, format)
                    success = True
                except:
                    continue
        if not success:
            feedback.append_to_field_problems(
                unique_field=unique_field, 
                message="'{}' is an invalid format for dates. Must be format: dd-mm-yyyy".format(sample_date_dmy)
                )
            sample_date_dmy = None
    else:
        sample_date_dmy = None
    return sample_date_dmy


def upload_publications_from_file(request):

    table = tab_delimited_file(request)
    failed_uploads = []

    for i, row in enumerate(table):
        for key, doi in row.items():
            if key == "doi" and doi != "":
                try:
                    doi = clean_doi(doi)
                    Publication.objects.update_or_create(doi=doi)

                except Exception as e:
                    messages.error(request, e)
                    failed_uploads.append("doi no. {}: {}".format(i + 1, doi))

    return failed_uploads


# A lot of this can be made accessible for other resource categories too
def upload_dataset_from_file(request):
    """ Validates and stores Data objects from uploaded file based on tab separated values """

    table = tab_delimited_file(request)
    feedback = Feedback()
    all_headers = [
        "run_accession",
        "sample_type",
        "data_type",
        "location",
        "farm_name",
        "farm_size",
        "animal",
        "antibiotics",
        "host",
        "age_months",
        "diet",
        "target_region_16s",
        "no_of_samples",
        "no_of_animals",
        "sample_date_dmy",
        "doi"
    ]

    required_headers = [
        "run_accession",
        "sample_type",
        "data_type"
    ]


    if not missing_headers(all_headers, table, feedback):
        for row_number, row in enumerate(table):
            print("Processing row {}".format(row_number + 1))

            row = validate_data_row_with_feedback(row, all_headers, required_headers, row_number, feedback)
            if not row:
                continue  # continuing to next row

            run_accession = row["run_accession"]
            sample_type = row["sample_type"]
            data_type = row["data_type"]
            location = row["location"]
            farm_name = row["farm_name"]
            farm_size = row["farm_size"]
            animal = row["animal"]
            antibiotics = row["antibiotics"]
            host = row["host"]
            age_months = row["age_months"]
            diet = row["diet"]
            target_region_16s = row["target_region_16s"]
            no_of_samples = row["no_of_samples"]
            no_of_animals = row["no_of_animals"]
            sample_date_dmy = row["sample_date_dmy"]
            doi = row["doi"]
            publication = None

            # Convert to correct formats
            farm_size = formatted_number_or_None(
                farm_size, int, "farm size", run_accession, feedback)
            no_of_samples = formatted_number_or_None(
                no_of_samples, int, "number of samples", run_accession, feedback)
            no_of_animals = formatted_number_or_None(
                no_of_animals, int, "number of animals", run_accession, feedback)
            age_months = formatted_number_or_None(
                age_months, float, "age in months", run_accession, feedback)
            sample_date_dmy = formatted_date_or_None(sample_date_dmy, run_accession, feedback)


            if doi:
                try:
                    doi = clean_doi(doi)
                    publication = Publication.objects.filter(doi=doi).first()
                    if publication:
                        print("found existing publication")
                    else:
                        publication = Publication(doi=doi)
                        publication.save()

                except:
                    feedback.append_to_field_problems(
                        unique_field=run_accession, 
                        message="Could not fetch article from doi: < {} >. ".format(doi)
                        )
                    publication = None

            datatuple = Data.objects.update_or_create(
                run_accession=run_accession,
                defaults={
                    "sample_type": sample_type,
                    "data_type": data_type,
                    "location": location,
                    "farm_name": farm_name,
                    "farm_size": farm_size,
                    "animal": animal,
                    "antibiotics": antibiotics,
                    "host": host,
                    "age": age_months,
                    "diet": diet,
                    "target_region_16s": target_region_16s,
                    "no_of_samples": no_of_samples,
                    "no_of_animals": no_of_animals,
                    "sample_date": sample_date_dmy,
                    "publication": publication
                }
            )

            new_dataset = datatuple[0]
            if datatuple[1]:
                updatedstring = "Created"
            else:
                updatedstring = "Updated"

            feedback.append_to_row_success(
                unique_field=run_accession, 
                message="{} - {}".format(updatedstring, new_dataset))

    return feedback


def upload_genomes_from_file(request):

    print("\n\n\n")
    table = tab_delimited_file(request)
    feedback = Feedback()
    all_headers = [
        "unique_id",
        "closest_relative_and_alternative_name",
        "phylogeny_class",
        "original_sample",
        "country",
        "study_doi",
        "dRep_secondary_cluster",
        "checkm_completeness",
        "checkm_contamination",
        "mean_contig_read_coverage",
        "dRep_set_of_MAGs",
        "source",
        "latest_doi"
    ]

    required_headers = [
        "unique_id",
        "closest_relative_and_alternative_name",
        "phylogeny_class",
        "original_sample",
        "country",
        "dRep_secondary_cluster",
        "checkm_completeness",
        "checkm_contamination",
        "mean_contig_read_coverage",
        "source",
        "latest_doi"
    ]

    # All headers are  required

    if not missing_headers(all_headers, table, feedback):

        upload = True
        genomes_to_save = []
        old_genomes = Genome.objects.filter(expired_date=None)
        latest_version_uids = []

        for row_index, row in enumerate(filter(empty_row_filter, table)): # skips empty rows

            row_number = row_index + 2 # 1 to account for 0-index, 1 to account for Excel sheet headers

            unique_id = row["unique_id"]
            closest_relative_and_alternative_name = row["closest_relative_and_alternative_name"]
            phylogeny_class = row["phylogeny_class"]
            original_sample = row["original_sample"]
            country = row["country"]
            study_doi = row["study_doi"]
            dRep_secondary_cluster = row["dRep_secondary_cluster"]
            checkm_completeness = row["checkm_completeness"]
            checkm_contamination = row["checkm_contamination"]
            mean_contig_read_coverage = row["mean_contig_read_coverage"]
            dRep_set_of_MAGs = row["dRep_set_of_MAGs"]
            source = row["source"]
            latest_doi = row["latest_doi"]
            expired_date = None

            # Check existing/new/expired
            if unique_id in latest_version_uids:
                feedback.append_to_row_errors(
                    unique_field=row["unique_id"] if row.get("unique_id") else "with unknown unique_id in row {}".format(row_number),
                    message="Row {} ({}): Another row with this unique_id exists in document.".format(row_number, unique_id)
                    )
                upload = False
            latest_version_uids.append(unique_id)
            exists = False
            for genome in old_genomes:
                if genome.unique_id == unique_id:
                    exists = True
            if exists:
                continue # to next row in for loop
            


            
            ### Check if row is valid. If there is anything invalid upload is set to False. ###

            # Check that all required fields have data
            for header in required_headers:
                if not row[header] or row[header].isspace():
                    upload = False

                    feedback.append_to_row_errors(
                        unique_field=row["unique_id"] if row.get("unique_id") else "with unknown unique_id in row {}".format(row_number),
                        message="Row {} ({}): Column '{}' must contain a value.".format(row_number, unique_id, header)
                        )

            try:
                checkm_completeness = float(checkm_completeness.replace(",", "."))
                checkm_contamination = float(checkm_contamination.replace(",", "."))
                mean_contig_read_coverage = float(mean_contig_read_coverage.replace(",", "."))
            except Exception as e:
                upload = False
                feedback.append_to_row_errors(
                    unique_field=row["unique_id"] if row.get("unique_id") else "with unknown unique_id in row {}".format(row_number),
                    message="Row {} ({}): Checkm values and mean_contig_read_coverage must be numeric.".format(row_number, unique_id)
                    )
                
            if type(checkm_completeness) == float:
                if (checkm_completeness < 0.0) or (checkm_completeness > 100.0):
                    feedback.append_to_row_errors(
                        unique_field=row["unique_id"] if row.get("unique_id") else "with unknown unique_id in row {}".format(row_number),
                        message="Row {} ({}): Checkm_completeness outside allowed range (0-100)".format(row_number, unique_id)
                        )
                    upload = False

            if type(checkm_contamination) == float:
                if (checkm_contamination < 0.0) or (checkm_contamination > 100.0):
                    feedback.append_to_row_errors(
                        unique_field=row["unique_id"] if row.get("unique_id") else "with unknown unique_id in row {}".format(row_number),
                        message="Row {} ({}): Checkm_contamination outside allowed range (0-100)".format(row_number, unique_id)
                        )
                    upload = False

            publication = Publication.objects.filter(doi=study_doi).first()

            dRep_set_of_MAGs = True if dRep_set_of_MAGs.lower().strip() == "yes" else False


            if upload:
                try:
                    genome = Genome(
                        unique_id=unique_id,
                        closest_rel_alt_name=closest_relative_and_alternative_name,
                        phyl_class=phylogeny_class,
                        original_sample=original_sample,
                        country=country,
                        publication=publication,
                        dRep_secondary_cluster=dRep_secondary_cluster,
                        checkm_completeness=checkm_completeness,
                        checkm_contamination=checkm_contamination,
                        mean_contig_read_coverage=mean_contig_read_coverage,
                        dRep_set_of_MAGs=dRep_set_of_MAGs,
                        source=source,
                        latest_doi=latest_doi,
                        expired_date=expired_date
                    )

                    genomes_to_save.append(genome)

                except Exception as e:
                    feedback.append_to_row_errors(
                        unique_field="",
                        message="Internal error. If the problem persists please contact you friendly neighbourhood developer: {}".format(e)
                        )
        
        if upload:
            # Hvis den gamle entry ikke fandtes i nye, så sæt “expired date”.
            for genome in old_genomes:
                if genome.unique_id not in latest_version_uids:
                    print("this genome expires: {}".format(genome))
                    genome.expired_date = date.today()
                    genomes_to_save.append(genome)
            try:
                print("saving genomes:")
                for genome in genomes_to_save:
                    print(genome)
                    genome.save()
            except Exception as e:
                print("Aborted upload. Not saving any rows.")
                print(e)
        else:
            print("Was not uploaded.")




    if feedback:
        print("there is feedback")
    else:
        print("no feeback")

    return feedback




