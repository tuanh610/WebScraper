from backend.DatabaseEngine import DynamoElement


sourceElements = [DynamoElement('URL', 'HASH', 'S'), DynamoElement('Type', 'RANGE', 'S')]
sourceTableName = "Source"
phoneElements = [DynamoElement('Name', 'HASH', 'S'), DynamoElement('Brand', 'RANGE', 'S')]