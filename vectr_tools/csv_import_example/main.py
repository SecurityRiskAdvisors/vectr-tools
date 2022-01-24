import csv
from models import TestCase, Assessment, Campaign
from dotenv import dotenv_values

from vectr_api_client import query_orgs, VectrGQLConnParams

env_config = dotenv_values("csv_import_example/.env")
connection_params = VectrGQLConnParams(api_key=env_config.get("API_KEY"), vectr_gql_url=env_config.get("VECTR_GQL_URL"))

with open('csv_import_example/sample_data/DEMO_PURPLE_CE.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    assessments = {}

    org_names = []

    for row in reader:
        if row['AssessmentGroup'] not in assessments:
            assessments[row['AssessmentGroup']] = Assessment(name=row['AssessmentGroup'], campaigns={})

        current_assessment = assessments[row['AssessmentGroup']]

        if row['Campaign'] not in current_assessment.campaigns:
            current_assessment.campaigns[row['Campaign']] = Campaign(name=row['Campaign'], test_cases=[])

        current_campaign = current_assessment.campaigns[row['Campaign']]

        test_case = TestCase.parse_obj(row)

        for org_name in test_case.organizations:
            if org_name not in org_names:
                org_names.append(org_name)

        current_campaign.test_cases.append(test_case)

query_orgs(connection_params)
