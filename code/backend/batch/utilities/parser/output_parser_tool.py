from typing import List
import logging
import re
import json
from .parser_base import ParserBase
from ..common.source_document import SourceDocument

logger = logging.getLogger(__name__)


class OutputParserTool(ParserBase):
    def __init__(self) -> None:
        self.name = "OutputParser"

    def _clean_up_answer(self, answer):
        return answer.replace("  ", " ")

    def _get_source_docs_from_answer(self, answer):
        # extract all [docN] from answer and extract N, and just return the N's as a list of ints
        results = re.findall(r"\[doc(\d+)\]", answer)
        return [int(i) for i in results]

    def _make_doc_references_sequential(self, answer):
        doc_matches = list(re.finditer(r"\[doc\d+\]", answer))
        updated_answer = answer
        offset = 0
        for i, match in enumerate(doc_matches):
            start, end = match.start() + offset, match.end() + offset
            updated_answer = (
                updated_answer[:start] + f"[doc{i + 1}]" + updated_answer[end:]
            )
            offset += len(f"[doc{i + 1}]") - (end - start)
        return updated_answer

    def parse(
        self,
        question: str,
        answer: str,
        source_documents: List[SourceDocument] = [],
        **kwargs: dict,
    ) -> List[dict]:
        logger.info("Method parse of output_parser_tool started")
        answer = self._clean_up_answer(answer)
        doc_ids = self._get_source_docs_from_answer(answer)
        answer = self._make_doc_references_sequential(answer)

        # create return message object
        messages = [
            {
                "role": "tool",
                "content": {"citations": [], "intent": question},
                "end_turn": False,
            }
        ]

        for i in doc_ids:
            idx = i - 1

            if idx >= len(source_documents):
                logger.warning(f"Source document {i} not provided, skipping doc")
                continue

            doc = source_documents[idx]
            logger.debug(f"doc{idx}: {doc}")

            # Then update the citation object in the response, it needs to have filepath and chunk_id to render in the UI as a file
            messages[0]["content"]["citations"].append(
                {
                    "content": doc.get_markdown_url() + "\n\n\n" + doc.content,
                    "id": doc.id,
                    "chunk_id": (
                        re.findall(r"\d+", doc.chunk_id)[-1]
                        if doc.chunk_id is not None
                        else doc.chunk
                    ),
                    "title": doc.title,
                    "filepath": doc.get_filename(include_path=True),
                    "url": doc.get_markdown_url(),
                    "metadata": {
                        "offset": doc.offset,
                        "source": doc.source,
                        "markdown_url": doc.get_markdown_url(),
                        "title": doc.title,
                        "original_url": doc.source,  # TODO: do we need this?
                        "chunk": doc.chunk,
                        "key": doc.id,
                        "filename": doc.get_filename(),
                    },
                }
            )
        if messages[0]["content"]["citations"] == []:
            answer = re.sub(r"\[doc\d+\]", "", answer)
        messages.append({"role": "assistant", "content": answer, "end_turn": True})
        # everything in content needs to be stringified to work with Azure BYOD frontend
        messages[0]["content"] = json.dumps(messages[0]["content"])
        logger.info("Method parse of output_parser_tool ended")
        return messages
