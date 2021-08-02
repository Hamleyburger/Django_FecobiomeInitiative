from datetime import datetime
from io import TextIOWrapper
from csv import DictReader
from resources.API_helpers.publications import clean_doi


from django.contrib import messages
from .models import Data, Publication


def upload_publications_from_file(request):

    file = request.FILES["fileinput"]
    file_data = TextIOWrapper(file, encoding='utf-8', newline='')
    csv_reader = DictReader(file_data, delimiter="\t")
    failed_uploads = []

    for i, row in enumerate(csv_reader):
        for key, doi in row.items():
            if key == "doi" and doi != "":
                try:
                    doi = clean_doi(doi)
                    Publication.objects.update_or_create(doi=doi)

                except Exception as e:
                    messages.error(request, e)
                    failed_uploads.append("doi no. {}: {}".format(i + 1, doi))

    return failed_uploads


def upload_dataset_from_file(request):
    """ Validates and stores Data objects from uploaded file based on tab separated values """

    print("running")
    file = request.FILES["fileinput"]
    file_data = TextIOWrapper(file, encoding='utf-8', newline='')
    csv_reader = DictReader(file_data, delimiter="\t")
    missing_headers_list = []
    feedback = {}
    feedback["invalid_rows"] = []
    feedback["success"] = []
    no_data_strings = ["na", "n/a", "unknown",
                       "no data", "empty", "null", "none", "missing", "", " ", "\t"]

    def append_to_field_problems(run_accession, message):
        if not feedback.get("field_problems"):
            feedback["field_problems"] = {}
        if not feedback["field_problems"].get(run_accession):
            feedback["field_problems"][run_accession] = []
        feedback["field_problems"][run_accession].append(message)

    def row_is_valid(row, required_headers):
        """ Checks that row is valid and all headers are present in table """
        valid = True
        for header in required_headers:
            if row[header] == None:
                print("row missing header: {}".format(header))
                valid = False
                return valid
        print("Checking run_accession and sample_type lower")
        if row["run_accession"].lower() in no_data_strings:
            valid = False
        if row["sample_type"].lower() in no_data_strings:
            valid = False
        return valid

    def missing_headers(required_headers, csv_reader):
        missing = False
        for header in required_headers:
            if header not in csv_reader.fieldnames:
                missing_headers_list.append(header)
                missing = True
        return missing

    def empty_no_data_strings(row):
        for key, value in row.items():
            if value.lower() in no_data_strings:
                row[key] = ""
        return row

    required_headers = [
        "run_accession",
        "sample_type",
        "location",
        "farm_name",
        "farm_size",
        "animal",
        "antibiotics",
        "host",
        "age_months",
        "diet",
        "sample_date_dmy",
        "doi"
    ]

    if not missing_headers(required_headers, csv_reader):
        for i, row in enumerate(csv_reader):

            if not row_is_valid(row, required_headers):
                feedback["invalid_rows"].append(
                    "row no. {}: {}".format((i + 1), row))
                continue  # continuing to next row

            row = empty_no_data_strings(row)

            run_accession = row["run_accession"]
            sample_type = row["sample_type"]
            location = row["location"]
            farm_name = row["farm_name"]
            farm_size = row["farm_size"]
            animal = row["animal"]
            antibiotics = row["antibiotics"]
            host = row["host"]
            age_months = row["age_months"]
            diet = row["diet"]
            sample_date_dmy = row["sample_date_dmy"]
            doi = row["doi"]
            publication = None

            # Convert to correct formats
            if farm_size:
                try:
                    farm_size = int(farm_size)
                except:
                    append_to_field_problems(
                        run_accession, "invalid farm size: < {} >. Must be int".format(farm_size))
                    farm_size = None
            else:
                farm_size = None

            if age_months:
                try:
                    age_months = float(age_months)
                except:
                    append_to_field_problems(
                        run_accession, "invalid age in months: < {} >. Must be a number".format(age_months))
                    age_months = None
            else:
                age_months = None

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
                    sample_date_dmy = None
                    append_to_field_problems(
                        run_accession, "invalid date: < {} >. Must be format: dd-mm-yyyy".format(sample_date_dmy))
            else:
                sample_date_dmy = None

            if doi:
                try:
                    doi = clean_doi(doi)
                    Publication.objects.update_or_create(doi=doi)
                    publication = Publication.objects.filter(doi=doi).first()
                except:
                    append_to_field_problems(
                        run_accession, "Could not fetch article from doi: < {} >. ".format(doi))
                    publication = None

            new_dataset = Data(
                run_accession=run_accession,
                sample_type=sample_type,
                location=location,
                farm_name=farm_name,
                farm_size=farm_size,
                animal=animal,
                antibiotics=antibiotics,
                host=host,
                age=age_months,
                diet=diet,
                sample_date=sample_date_dmy,
                publication=publication
            )

            exists = Data.objects.filter(run_accession=run_accession).exists()
            if not exists:
                new_dataset.save()
                string = "Row {}: < {} >".format(i, new_dataset)
                feedback["success"].append(string)

    else:  # if missing_headers_list
        feedback["missing_headers"] = missing_headers_list

    return feedback
