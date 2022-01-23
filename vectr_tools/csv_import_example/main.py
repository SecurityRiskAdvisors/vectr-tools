import csv
from models import TestCase, Assessment, Campaign

with open('csv_import_example/sample_data/DEMO_PURPLE_CE.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    assessments = {}

    for row in reader:
        if row['AssessmentGroup'] not in assessments:
            assessments[row['AssessmentGroup']] = Assessment(name=row['AssessmentGroup'], campaigns={})

        current_assessment = assessments[row['AssessmentGroup']]

        if row['Campaign'] not in current_assessment.campaigns:
            current_assessment.campaigns[row['Campaign']] = Campaign(name=row['Campaign'], test_cases=[])

        current_campaign = current_assessment.campaigns[row['Campaign']]

        test_case = TestCase.parse_obj(row)

        current_campaign.test_cases.append(test_case)

print(assessments)
