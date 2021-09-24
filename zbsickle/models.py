from csv import DictWriter

from sickle.models import Record


class ZbPreviewRecord(Record):
    fieldnames = ["de", "doi", "msc", "keyword", "title", "review_text", "refs", "author", "author_id", "language", "document_type", "publication_year"]
    _field_map = {
        "de": "document_id",
        "doi": "doi",
        "msc": "classification",
        "keyword": "keyword",
        "title": "document_title",
        "review_text": "review_text",
        "refs": "ref_classification",
        "author": "author",
        "author_id": "author_id",
        "language": "language",
        "document_type": "document_type",
        "publication_year": "publication_year",
    }
    metadata = None

    def get_attrib(self, attrib):
        if self.metadata is None:
            self.metadata = self.get_metadata()
        try:
            data = self.metadata[attrib]
            if len(data) == 0:
                data = ""
            if len(data) == 1:
                data = data[0]
            if (
                data == "zbMATH Open Web Interface contents unavailable due "
                "to conflicting licenses."
            ):
                return ""
            else:
                return data
        except KeyError:
            return ""

    def get_de(self) -> int:
        return self.get_attrib("document_id")

    def get_doi(self) -> int:
        return self.get_attrib("doi")

    def get_msc(self) -> []:
        return self.get_attrib("classification")

    def get_keywords(self) -> []:
        return self.get_attrib("keyword")

    def get_title(self) -> str:
        return self.get_attrib("document_title")

    def get_review_text(self) -> str:
        return self.get_attrib("review_text")

    def get_refs(self) -> []:
        return self.get_attrib("ref_classification")

    def get_author(self) -> str:
        return self.get_attrib("author")

    def get_author_id(self) -> []:
        return self.get_attrib("author_id")

    def get_language(self) -> str:
        return self.get_attrib("language")

    def get_document_type(self) -> str:
        return self.get_attrib("document_type")

    def get_pubication_year(self) -> int:
        return self.get_attrib("publication_year")

    def writerow(self, writer: DictWriter, only_complete=False) -> bool:
        fields = {}
        for f in self.fieldnames:
            fields[f] = self.get_attrib(self._field_map[f])
        if only_complete:
            for k, v in fields.items():
                if v == "":
                    return False
        writer.writerow(fields)
        return True
