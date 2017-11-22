class Column:
    TO_DO = "Ready for Dev"
    IN_PROGRESS = "Dev"
    CODE_REVIEW = "Dev Review"
    QA_REVIEW = "Done"

    @staticmethod
    def from_string(column_string):
        if column_string == "Ready for Dev":
            return Column.TO_DO
        elif column_string == "Dev":
            return Column.IN_PROGRESS
        elif column_string == "Dev Review":
            return Column.CODE_REVIEW
        elif column_string == "Done":
            return Column.QA_REVIEW
        else:
            return None
