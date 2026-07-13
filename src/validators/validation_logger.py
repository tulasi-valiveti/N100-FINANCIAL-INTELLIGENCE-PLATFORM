import pandas as pd
from pathlib import Path


class ValidationLogger:
    """
    Stores all validation failures and exports them to CSV.
    """

    def __init__(self):

        self.records = []

    def log(
        self,
        rule_id,
        table,
        company_id,
        year,
        column,
        value,
        severity,
        message
    ):

        self.records.append({
            "rule_id": rule_id,
            "table": table,
            "company_id": company_id,
            "year": year,
            "column": column,
            "value": value,
            "severity": severity,
            "message": message
        })

    def save(
        self,
        output_path="reports/validation_failures.csv"
    ):

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df = pd.DataFrame(self.records)

        df.to_csv(
            output_path,
            index=False
        )

        print(
            f"\nValidation report saved to {output_path}"
        )

    def get_critical_errors(self):
         return [
            record
            for record in self.records
            if record["severity"] == "CRITICAL"
        ]