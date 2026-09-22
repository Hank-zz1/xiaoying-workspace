from __future__ import annotations

import argparse
from typing import Any

from _pdf_utils import (
    PdfSkillError,
    appearance_on_values,
    dereference,
    get_full_annotation_field_id,
    get_field_info,
    handle_cli_error,
    import_required,
    input_path,
    load_json,
    output_path,
    validate_fillable_value,
)


def _clone_writer(pypdf: Any, reader: Any) -> Any:
    try:
        return pypdf.PdfWriter(clone_from=reader)
    except TypeError:
        writer = pypdf.PdfWriter()
        writer.clone_document_from_reader(reader)
        return writer


def _patch_choice_options_for_pypdf() -> None:
    try:
        from pypdf.constants import FieldDictionaryAttributes
        from pypdf.generic import DictionaryObject
    except Exception:
        return

    if getattr(DictionaryObject.get_inherited, "_pdf_skill_patched", False):
        return

    original_get_inherited = DictionaryObject.get_inherited

    def patched_get_inherited(self, key: str, default=None):
        result = original_get_inherited(self, key, default)
        if key == FieldDictionaryAttributes.Opt:
            if isinstance(result, list) and all(isinstance(v, list) and len(v) == 2 for v in result):
                result = [v[0] for v in result]
        return result

    patched_get_inherited._pdf_skill_patched = True
    DictionaryObject.get_inherited = patched_get_inherited


def _load_field_values(fields_json_path: str) -> list[dict[str, Any]]:
    data = load_json(fields_json_path)
    if isinstance(data, list):
        fields = data
    elif isinstance(data, dict) and isinstance(data.get("fields"), list):
        fields = data["fields"]
    else:
        raise PdfSkillError("field_values.json must be a list or an object with a 'fields' list.")

    for index, field in enumerate(fields):
        if not isinstance(field, dict):
            raise PdfSkillError(f"Field entry #{index + 1} must be an object.")
        if "field_id" not in field:
            raise PdfSkillError(f"Field entry #{index + 1} is missing 'field_id'.")
    return fields


def _sync_button_widget_appearances(writer: Any, values_by_id: dict[str, Any]) -> None:
    try:
        from pypdf.generic import NameObject
    except Exception:
        return

    for page in writer.pages:
        for raw_annotation in page.get("/Annots", []) or []:
            annotation = dereference(raw_annotation)
            field_id = get_full_annotation_field_id(annotation)
            if field_id not in values_by_id:
                continue
            value = str(values_by_id[field_id])
            on_values = appearance_on_values(annotation)
            if value == "/Off" or value in on_values:
                annotation.update({NameObject("/AS"): NameObject(value)})


def fill_pdf_fields(input_pdf_path: str, fields_json_path: str, output_pdf_path: str) -> int:
    _patch_choice_options_for_pypdf()
    pypdf = import_required("pypdf")

    reader = pypdf.PdfReader(str(input_path(input_pdf_path, ".pdf")))
    field_info = get_field_info(reader)
    fields_by_id = {field["field_id"]: field for field in field_info}
    requested_fields = _load_field_values(fields_json_path)

    has_error = False
    fields_by_page: dict[int, dict[str, Any]] = {}
    values_by_id: dict[str, Any] = {}

    for field in requested_fields:
        if "value" not in field:
            continue
        field_id = str(field["field_id"])
        existing_field = fields_by_id.get(field_id)
        if not existing_field:
            print(f"ERROR: '{field_id}' is not a valid field ID")
            has_error = True
            continue

        expected_page = int(existing_field["page"])
        actual_page = int(field.get("page", expected_page))
        if actual_page != expected_page:
            print(
                f"ERROR: Incorrect page number for '{field_id}' "
                f"(got {actual_page}, expected {expected_page})"
            )
            has_error = True
            continue

        validation_error = validate_fillable_value(existing_field, field["value"])
        if validation_error:
            print(f"ERROR: {validation_error}")
            has_error = True
            continue

        fields_by_page.setdefault(expected_page, {})[field_id] = field["value"]
        values_by_id[field_id] = field["value"]

    if has_error:
        raise SystemExit(1)
    if not fields_by_page:
        raise PdfSkillError("No fields with a 'value' key were provided.")

    writer = _clone_writer(pypdf, reader)
    for page_number, field_values in sorted(fields_by_page.items()):
        try:
            writer.update_page_form_field_values(
                writer.pages[page_number - 1],
                field_values,
                auto_regenerate=False,
            )
        except TypeError:
            writer.update_page_form_field_values(writer.pages[page_number - 1], field_values)

    _sync_button_widget_appearances(writer, values_by_id)
    if hasattr(writer, "set_need_appearances_writer"):
        writer.set_need_appearances_writer(True)

    target = output_path(output_pdf_path)
    with target.open("wb") as stream:
        writer.write(stream)

    print(f"Successfully wrote {target}")
    print(f"Filled {len(values_by_id)} fields")
    return len(values_by_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill existing AcroForm fields in a PDF.")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("field_values_json", help="JSON list of field values")
    parser.add_argument("output_pdf", help="Output PDF path")
    args = parser.parse_args()

    try:
        fill_pdf_fields(args.input_pdf, args.field_values_json, args.output_pdf)
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
