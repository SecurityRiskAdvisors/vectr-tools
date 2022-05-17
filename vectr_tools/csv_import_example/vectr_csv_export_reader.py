import csv
import sys
from models import TestCase, Assessment, Campaign


def get_assessments_from_csv(csv_path: str):
    csv.field_size_limit(sys.maxsize)

    assessments = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        org_names = []

        for row in reader:
            if row['AssessmentGroup'] not in assessments:
                assessments[row['AssessmentGroup']] = Assessment(name=row['AssessmentGroup'], campaigns={})

            current_assessment = assessments[row['AssessmentGroup']]

            if row['Campaign'] not in current_assessment.campaigns:
                current_assessment.campaigns[row['Campaign']] = Campaign(name=row['Campaign'], test_cases=[])

            current_campaign = current_assessment.campaigns[row['Campaign']]

            test_case = TestCase.parse_obj(row)

            if test_case.organization not in org_names:
                org_names.append(test_case.organization)

            current_campaign.test_cases.append(test_case)

    return assessments


def csv_data_has_outcome_paths(assessments: dict):
    for ag_name in assessments:
        campaigns = assessments[ag_name].campaigns
        for campaign_name in campaigns:
            test_cases = campaigns[campaign_name].test_cases
            for test_case in test_cases:
                if test_case.outcomePath and test_case.outcomePath is not None and str(test_case.outcomePath).strip() != "":
                    return True
    return False
