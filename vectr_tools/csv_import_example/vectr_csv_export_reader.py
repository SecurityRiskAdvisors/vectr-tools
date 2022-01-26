import csv
from models import TestCase, Assessment, Campaign


def get_assessments_from_csv(csv_path: str):
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
