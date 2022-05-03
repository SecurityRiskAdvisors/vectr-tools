from dotenv import dotenv_values
from vectr_csv_export_reader import get_assessments_from_csv, csv_data_has_outcome_paths
from vectr_api_client import VectrGQLConnParams, \
    create_assessment, \
    create_campaigns, \
    create_test_cases, \
    get_org_id_for_campaign_and_assessment_data, \
    api_can_use_new_outcome_paths

env_config = dotenv_values(".env")

connection_params = VectrGQLConnParams(api_key=env_config.get("API_KEY"),
                                       vectr_gql_url=env_config.get("VECTR_GQL_URL"))

assessments = get_assessments_from_csv(csv_path=env_config.get("CSV_PATH"))

org_id = get_org_id_for_campaign_and_assessment_data(connection_params=connection_params,
                                                     org_name=env_config.get("ORG_NAME"))

api_has_outcome_paths = api_can_use_new_outcome_paths(connection_params=connection_params)

csv_has_outcome_path_data = csv_data_has_outcome_paths(assessments)

target_db = env_config.get("TARGET_DB")

if not api_has_outcome_paths and csv_has_outcome_path_data:
    raise Exception("VECTR version not new enough to import Outcome Path data. Upgrade VECTR instance.")

# Loop over results from CSV
for assessment_name in assessments.keys():
    created_assessment_detail = create_assessment(connection_params, target_db, org_id, assessment_name)

    assessment_id = created_assessment_detail.get(assessment_name).get("id")

    campaigns = assessments.get(assessment_name).campaigns
    created_campaigns = create_campaigns(connection_params,
                                         target_db,
                                         org_id,
                                         campaigns,
                                         assessment_id)

    # You could refactor to add batch execution for test cases after preparing all gql inputs if
    # you're trying to create a lot of test cases per campaign
    for created_campaign_name in created_campaigns.keys():
        campaign_id = created_campaigns.get(created_campaign_name).get("id")

        test_cases = campaigns.get(created_campaign_name).test_cases

        created_test_cases = create_test_cases(connection_params,
                                               target_db,
                                               campaign_id,
                                               test_cases,
                                               api_has_outcome_paths)

        print(created_test_cases)

    print(created_campaigns)
