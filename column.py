class Column:
    TO_DO = "Open"
    IN_PROGRESS = "In Progress"
    CODE_REVIEW = "Code Review"
    QA_REVIEW = "QA"
    PRODUCT_REVIEW = "Product Review"
    CLOSED = "Closed"

    @staticmethod
    def from_string(column_string):
        if column_string == "Open":
            return Column.TO_DO
        elif column_string == "In Progress":
            return Column.IN_PROGRESS
        elif column_string == "Code Review":
            return Column.CODE_REVIEW
        elif column_string == "QA":
            return Column.QA_REVIEW
        elif column_string == "Product Review":
            return Column.PRODUCT_REVIEW
        elif column_string == "Done":
            return Column.DONE
        else:
            return None
