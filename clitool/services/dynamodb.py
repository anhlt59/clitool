from clitool.services.base import AwsService
from clitool.types.dynamodb import DynamoDBTable, DynamoDBTables


class DynamoDBService(AwsService):
    @property
    def client(self):
        return self.session.client("dynamodb")

    def list(self, prefix: str = "") -> DynamoDBTables:
        """
        List DynamoDB tables.
        :param prefix: Name prefix to filter by.
        """
        tables = DynamoDBTables()
        response = self.client.list_tables()
        for table_name in response.get("TableNames", []):
            if prefix and not table_name.startswith(prefix):
                continue
            tables.append(DynamoDBTable(name=table_name))
        return tables

    def describle(self, stack_name: str = None):
        pass
