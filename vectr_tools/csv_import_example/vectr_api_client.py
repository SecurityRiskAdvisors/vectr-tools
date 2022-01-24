from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from models import Assessment
from pydantic import BaseModel


class VectrGQLConnParams(BaseModel):
    api_key: str
    vectr_gql_url: str


def get_client(connection_params: VectrGQLConnParams):
    transport = RequestsHTTPTransport(
        url=connection_params.vectr_gql_url, verify=False, retries=1,
        headers={"Authorization": "VEC1 " + connection_params.api_key}
    )

    return Client(transport=transport, fetch_schema_from_transport=True)


def create_assessment(connection_params: dict, db: str, assessment: Assessment):
    print()


def query_orgs(connection_params: VectrGQLConnParams):
    client = get_client(connection_params)

    query = gql(
        """
        query {
          organizations(filter: {name: {eq: "Security Risk Advisors"}}) {
            nodes {
              id, name
            }
          }
        }
    """
    )

    query2 = gql(
        """
        query($nameVar: String) {
          organizations(filter: {name: {eq:  $nameVar}}) {
            nodes {
              id, name
            }
          }
        }
    """
    )

    gql_variables = {"nameVar": "Security Risk Advisors"}

    print(query.to_dict())
    result = client.execute(query2, variable_values=gql_variables)
    print(result)
