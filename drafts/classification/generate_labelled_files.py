#!/usr/bin/env python3
"""
Build the labelled-files stand-in for the classification demo: Office and PDF files carrying
Microsoft Purview sensitivity labels the way Office and the MIP SDK write them, plus two files the
platform cannot read (a Purview-protected PDF stand-in and a password-protected PDF).

No Purview tenant is involved. The label ids, names and the tenant (site) id are fictional and fixed,
so the mapping rows in classification-mappings.yaml keep matching after a rebuild.

    python3 -m venv .venv && .venv/bin/pip install python-docx openpyxl python-pptx pypdf reportlab
    .venv/bin/python drafts/classification/generate_labelled_files.py [--out data/labelled-files]

Writes into the pack's data/labelled-files/ by default (the folder is created; files are replaced).
"""
from __future__ import annotations

import argparse
import io
import os
import zipfile
from datetime import datetime, timezone

import docx
import openpyxl
import pptx
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, DecodedStreamObject, DictionaryObject, NameObject, NumberObject, TextStringObject,
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Fictional Meridian Works tenant and labels. Keep in step with classification-mappings.yaml.
SITE_ID = "0f5e3d2c-1b4a-4968-8776-5a4b3c2d1e0f"
LABELS = {
    "Public":                      "3a1c0f4e-6b2d-4c8e-9f10-2a5b7c9d1e01",
    "General":                     "5d8e2b1a-7c4f-4e9a-8b3d-6f1a2c4e8b02",
    "Confidential":                "8f2a6c3d-1e5b-4a7c-9d0e-3b6f8a1c5d03",
    "Confidential - Finance":      "9a4d7e2f-3c6b-4d8a-8e1f-5c2b9d4a7e04",
    "Confidential - HR":           "b1e5c8a2-4f7d-4b9c-9a2e-7d3c1f6b8a05",
    "Highly Confidential":         "c7f3a9d1-5e2b-4c6d-8f4a-9e1b3d7c2f06",
    "Highly Confidential - Legal": "d2a8f4c6-6b1e-4e3a-9c5d-1f7e4b9a3c07",
    "Partner Shared":              "e6c1b7d3-8a4f-4f2b-8d6c-2a9f5e1b4d08",  # deliberately not mapped
}
SET_DATE = "2026-09-29T08:00:00Z"
FIXED_TIME = datetime(2026, 9, 29, 8, 0, 0, tzinfo=timezone.utc)
PASSWORD = "meridian-2027"  # the password-protected PDF; say it aloud only if you want to show it opens

CUSTOM_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties"
CUSTOM_CT = "application/vnd.openxmlformats-officedocument.custom-properties+xml"
LABELINFO_REL = "http://schemas.microsoft.com/office/2020/02/relationships/classificationlabels"
LABELINFO_CT = "application/vnd.ms-office.classificationlabels+xml"
FMTID = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}"


# --------------------------------------------------------------------------------------------- Office

def msip_fields(name: str, method: str = "Standard") -> list[tuple[str, str]]:
    gid = LABELS[name]
    p = f"MSIP_Label_{gid}_"
    return [
        (p + "Enabled", "true"),
        (p + "SetDate", SET_DATE),
        (p + "Method", method),
        (p + "Name", name),
        (p + "SiteId", SITE_ID),
        (p + "ActionId", "00000000-0000-4000-8000-" + gid[-12:]),
        (p + "ContentBits", "0"),
    ]


def custom_xml(props: list[tuple[str, str]]) -> str:
    rows = "".join(
        f'<property fmtid="{FMTID}" pid="{i + 2}" name="{k}"><vt:lpwstr>{v}</vt:lpwstr></property>'
        for i, (k, v) in enumerate(props)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">' + rows + "</Properties>"
    )


def labelinfo_xml(name: str, method: str = "Standard") -> str:
    # The 2022+ form: id and state only, no display name.
    return (
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
        '<clbl:labelList xmlns:clbl="http://schemas.microsoft.com/office/2020/mipLabelMetadata">'
        f'<clbl:label id="{{{LABELS[name]}}}" enabled="1" method="{method}" siteId="{{{SITE_ID}}}" removed="0" />'
        "</clbl:labelList>"
    )


def add_part(data: bytes, part: str, xml: str, rel_type: str, content_type: str) -> bytes:
    """Return the Office zip with `part` added, a root relationship to it and its content type."""
    src = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in src.infolist():
            body = src.read(item.filename)
            if item.filename == "[Content_Types].xml":
                text = body.decode("utf-8")
                override = f'<Override PartName="/{part}" ContentType="{content_type}"/>'
                if f'PartName="/{part}"' not in text:
                    text = text.replace("</Types>", override + "</Types>")
                body = text.encode("utf-8")
            elif item.filename == "_rels/.rels":
                text = body.decode("utf-8")
                if f'Target="{part}"' not in text:
                    rid = "rIdAiso" + ("Custom" if part.startswith("docProps") else "Label")
                    text = text.replace("</Relationships>", f'<Relationship Id="{rid}" Type="{rel_type}" Target="{part}"/></Relationships>')
                body = text.encode("utf-8")
            elif item.filename == part:
                continue
            z.writestr(item, body)
        z.writestr(part, xml.encode("utf-8"))
    return out.getvalue()


def label_office(data: bytes, name: str, method: str = "Standard", form: str = "custom") -> bytes:
    if form == "custom":
        return add_part(data, "docProps/custom.xml", custom_xml(msip_fields(name, method)), CUSTOM_REL, CUSTOM_CT)
    return add_part(data, "docMetadata/LabelInfo.xml", labelinfo_xml(name, method), LABELINFO_REL, LABELINFO_CT)


def make_docx(title: str, paragraphs: list[str]) -> bytes:
    d = docx.Document()
    d.core_properties.title = title
    d.core_properties.author = "Meridian Works"
    d.core_properties.created = FIXED_TIME.replace(tzinfo=None)
    d.core_properties.modified = FIXED_TIME.replace(tzinfo=None)
    d.add_heading(title, level=1)
    for p in paragraphs:
        d.add_paragraph(p)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def make_xlsx(title: str, rows: list[list[object]]) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q3 summary"
    for r in rows:
        ws.append(r)
    wb.properties.title = title
    wb.properties.creator = "Meridian Works"
    wb.properties.created = FIXED_TIME.replace(tzinfo=None)
    wb.properties.modified = FIXED_TIME.replace(tzinfo=None)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def make_pptx(title: str, slides: list[tuple[str, list[str]]]) -> bytes:
    p = pptx.Presentation()
    p.core_properties.title = title
    p.core_properties.author = "Meridian Works"
    p.core_properties.created = FIXED_TIME.replace(tzinfo=None)
    p.core_properties.modified = FIXED_TIME.replace(tzinfo=None)
    for heading, bullets in slides:
        s = p.slides.add_slide(p.slide_layouts[1])
        s.shapes.title.text = heading
        body = s.placeholders[1].text_frame
        body.text = bullets[0]
        for b in bullets[1:]:
            body.add_paragraph().text = b
    buf = io.BytesIO()
    p.save(buf)
    return buf.getvalue()


# ----------------------------------------------------------------------------------------------- PDF

def render_pdf(title: str, lines: list[str]) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4, invariant=1)
    c.setTitle(title)
    c.setAuthor("Meridian Works")
    c.setFont("Helvetica-Bold", 14)
    y = 800
    c.drawString(60, y, title)
    c.setFont("Helvetica", 10.5)
    y -= 28
    for line in lines:
        for chunk in wrap(line, 95):
            c.drawString(60, y, chunk)
            y -= 15
        y -= 6
    c.showPage()
    c.save()
    return buf.getvalue()


def wrap(text: str, width: int) -> list[str]:
    out, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        out.append(cur)
    return out or [""]


def writer_from(pdf: bytes) -> PdfWriter:
    w = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf)))
    return w


def pdf_bytes(w: PdfWriter) -> bytes:
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


def pdf_info_label(pdf: bytes, name: str, method: str = "Standard") -> bytes:
    """Label in the document information dictionary (how the MIP SDK and Office's PDF export write it)."""
    w = writer_from(pdf)
    w.add_metadata({"/" + k: v for k, v in msip_fields(name, method)})
    return pdf_bytes(w)


def pdf_xmp_label(pdf: bytes, name: str, method: str = "Standard") -> bytes:
    """Label only in a compressed XMP metadata stream (pdfx namespace), not in the info dictionary."""
    w = writer_from(pdf)
    fields = "".join(f"<pdfx:{k}>{v}</pdfx:{k}>" for k, v in msip_fields(name, method))
    xmp = (
        '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about="" xmlns:pdfx="http://ns.adobe.com/pdfx/1.3/" xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f"{fields}</rdf:Description></rdf:RDF></x:xmpmeta>"
        '<?xpacket end="w"?>'
    ).encode("utf-8")
    stream = DecodedStreamObject()
    stream.set_data(xmp)
    stream[NameObject("/Type")] = NameObject("/Metadata")
    stream[NameObject("/Subtype")] = NameObject("/XML")
    compressed = stream.flate_encode()
    w._root_object[NameObject("/Metadata")] = w._add_object(compressed)
    return pdf_bytes(w)


def pdf_irm_standin(pdf: bytes, name: str) -> bytes:
    """
    A stand-in for a PDF protected by its Purview label: an encryption dictionary naming the
    MicrosoftIRMServices security handler, and the label left readable in the information dictionary.
    Readers without the Microsoft plug-in refuse it; the product only needs the handler name.
    """
    w = writer_from(pdf_info_label(pdf, name, method="Privileged"))
    enc = DictionaryObject({
        NameObject("/Filter"): NameObject("/MicrosoftIRMServices"),
        NameObject("/V"): NumberObject(2),
        NameObject("/Length"): NumberObject(128),
        NameObject("/PublishingLicense"): TextStringObject("stand-in: no licence, content is not recoverable"),
    })
    w._encrypt_entry = w._add_object(enc)
    return pdf_bytes(w)


def pdf_password(pdf: bytes) -> bytes:
    w = writer_from(pdf)
    w.encrypt(user_password=PASSWORD, owner_password=PASSWORD + "-owner", algorithm="RC4-128")
    return pdf_bytes(w)


# -------------------------------------------------------------------------------------------- content

def build(out: str) -> list[tuple[str, str]]:
    os.makedirs(out, exist_ok=True)
    made: list[tuple[str, str]] = []

    def save(fname: str, data: bytes, note: str) -> None:
        with open(os.path.join(out, fname), "wb") as f:
            f.write(data)
        made.append((fname, note))

    save("town-hall-agenda.docx", label_office(make_docx("Q4 town hall — agenda", [
        "Thursday 16 October, 15:00, Halden canteen; streamed to Riverside and Crestview.",
        "1. The year so far (Chief Executive, 15 minutes).",
        "2. The Nordvik Water service contract and what it means for Riverside (Service Director, 10 minutes).",
        "3. Questions from the floor. Send questions in advance to the announcements channel.",
        "Recordings are published the next day on the intranet.",
    ]), "Public"), "Public (custom.xml, matched by name)")

    save("riverside-shift-handover.docx", label_office(make_docx("Riverside shift handover — 28 September", [
        "Night shift to day shift, service centre workshop.",
        "Pump test rig 3 is out of service: the pressure transducer reads 0.4 bar high. Replacement ordered, due Wednesday.",
        "Two MW-300 controllers returned from Nordvik Water for firmware update; bench tests passed, ready for dispatch.",
        "Forklift FL-2 charger tripped twice. Facilities informed; use FL-1 until it is checked.",
    ]), "General", form="labelinfo"), "General (LabelInfo.xml only: id, no name; matched by id)")

    save("q3-board-pack-summary.xlsx", label_office(make_xlsx("Q3 board pack — summary", [
        ["Q3 2026 board pack summary (preliminary)", None, None],
        ["Measure", "Q3 actual", "Q3 plan"],
        ["Revenue (million)", 41.8, 44.5],
        ["Gross margin (%)", 18.2, 21.0],
        ["Cash at quarter end (million)", 9.4, 10.0],
        ["Nordvik Water contract, annual (million)", 3.1, None],
        ["Figures may still move by up to half a per cent before the board meeting of 28 October.", None, None],
    ]), "Confidential - Finance"), "Confidential - Finance (custom.xml, matched by id)")

    save("northfield-negotiation-memo.docx", label_office(make_docx("Northfield Castings — negotiation position", [
        "Privileged and confidential: prepared at the request of counsel.",
        "Liability cap: Northfield wants 12 months of fees; Meridian wants 24. Counsel recommends accepting 18 months "
        "in exchange for firm delivery penalties of 0.5 per cent of order value per week late, capped at 10 per cent.",
        "Change of control: Meridian needs a termination right on 90 days' notice if Northfield is acquired by a competitor.",
        "Not to be discussed with Northfield's commercial team before the next call.",
    ]), "Highly Confidential - Legal", method="Privileged"), "Highly Confidential - Legal (custom.xml, Privileged)")

    save("distributor-price-list-2027.pptx", label_office(make_pptx("Distributor price list 2027", [
        ("MW-300 controller: 2027 distributor prices", [
            "List price 4,850 per unit; distributor discount 22 per cent",
            "Volume band above 50 units: a further 5 per cent",
            "Prices hold until 30 June 2027",
        ]),
        ("Service contracts", [
            "Annual inspection: 1,150 per site",
            "Priority call-out within 8 hours: 3,400 per year",
        ]),
    ]), "Partner Shared"), "Partner Shared (custom.xml; NOT mapped: the store default applies)")

    base = render_pdf("Halden plant safety bulletin — October", [
        "Hearing protection is now required in bay 4 at all times while the new press line is commissioned.",
        "The eyewash station by the paint booth has moved to the north wall; the old one is out of use.",
        "Near misses in September: three, all at the loading dock. Use the marked walkway between 07:00 and 09:00.",
    ])
    save("plant-safety-bulletin.pdf", pdf_info_label(base, "General"), "General (information dictionary, matched by name)")

    base = render_pdf("Grievance 2026-03 — hearing notes", [
        "Hearing held in April with both parties and a People Operations partner.",
        "Subject: shift allocation at Halden. Agreed: shifts published four weeks ahead on a rotation.",
        "Both parties agreed the outcome. Matter closed; retained for the statutory period.",
    ])
    save("grievance-hearing-notes.pdf", pdf_xmp_label(base, "Confidential - HR"), "Confidential - HR (compressed XMP only)")

    base = render_pdf("This document is protected", [
        "This PDF is protected by a Microsoft Purview sensitivity label.",
        "Open it with an application that supports Microsoft Purview Information Protection.",
    ])
    save("audit-committee-minutes.pdf", pdf_irm_standin(base, "Highly Confidential"), "Highly Confidential, IRM-protected stand-in: unreadable")

    base = render_pdf("Salary review 2027 — working figures", [
        "Proposed merit budget 3.2 per cent; market adjustments for field technicians at Riverside.",
    ])
    save("salary-review-2027.pdf", pdf_password(base), f"no label, password-protected (RC4-128, password {PASSWORD}): unreadable")

    return made


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    default_out = os.path.normpath(os.path.join(here, "..", "..", "data", "labelled-files"))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=default_out)
    args = ap.parse_args()
    for fname, note in build(args.out):
        print(f"{fname:38} {note}")
    print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()
