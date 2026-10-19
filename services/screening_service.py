import os
from io import BytesIO

import shutil
import pymupdf
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from docx import Document
from pypdf import PdfReader


from ai.screening_analyzer import analyze_screening

from screening.matching_engine import (
    calculate_skill_match,
    calculate_preferred_skill_match
)

from screening.scoring_engine import (
    calculate_experience_score,
    calculate_education_score,
    calculate_overall_score,
    relevance_to_score
)

#from screening.evidence_matcher import evaluate_requirement_evidence
#from screening.project_matcher import evaluate_project_relevance





def extract_resume_text(resume):
    """Extract text from PDF or DOCX, using OCR for scanned PDFs."""

    file_name = getattr(resume, "name", "").lower()

    if file_name.endswith(".pdf"):
        try:
            resume.seek(0)
            pdf_bytes = resume.read()
            resume.seek(0)

            reader = PdfReader(BytesIO(pdf_bytes))

        except Exception as error:
            raise ValueError(
                "Unable to open this PDF. Please check that the file "
                "is valid and readable."
            ) from error

        extracted_pages = []

        for page in reader.pages:
            try:
                text = page.extract_text()
            except Exception:
                text = None

            if text and text.strip():
                extracted_pages.append(text)

        resume_text = "\n".join(extracted_pages)

        # OCR fallback when normal PDF extraction finds no text.
        if not resume_text.strip():
            try:
                tesseract_path = (
                os.getenv("TESSERACT_CMD")
                or shutil.which("tesseract")
                or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

                if not os.path.isfile(tesseract_path):
                    raise FileNotFoundError(
                        "Tesseract executable was not found. "
                        "Set TESSERACT_CMD to its actual path."
                    )

                pytesseract.pytesseract.tesseract_cmd = (
                    tesseract_path
                )

                ocr_pages = []

                with pymupdf.open(
                    stream=pdf_bytes,
                    filetype="pdf",
                ) as document:
                    for page in document:
                        pix = page.get_pixmap(
                            matrix=pymupdf.Matrix(300 / 72, 300 / 72),
                            alpha=False,
                        )

                        image = Image.open(
                            BytesIO(pix.tobytes("png"))
                        )

                        text = pytesseract.image_to_string(
                            image,
                            lang="eng",
                            config="--psm 3",
                        )

                        if text and text.strip():
                            ocr_pages.append(text)

                resume_text = "\n".join(ocr_pages)

            except Exception as error:
                raise ValueError(
                    f"OCR failed ({type(error).__name__}): {error}"
                ) from error

    elif file_name.endswith(".docx"):
        try:
            resume.seek(0)
            document = Document(resume)

            resume_text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

        except Exception as error:
            raise ValueError(
                "Unable to open this DOCX resume. Please check that "
                "the file is valid and readable."
            ) from error

    else:
        raise ValueError(
            "Unsupported resume format. Please upload a PDF or DOCX file."
        )

    if not resume_text.strip():
        raise ValueError(
            "Unable to extract readable text from this resume. "
            "If it is scanned, check the image quality and OCR setup."
        )

    return resume_text



def screen_resume(resume, job_profile):

    if not job_profile or "error" in job_profile:
        raise ValueError(
            "The job description has not been analyzed successfully yet."
        )

    resume_text = extract_resume_text(resume)

    screening_result = analyze_screening(
        resume_text,
        job_profile
    )
    
    if "error" in screening_result:
        raise ValueError(
            screening_result["error"]
        )
    
    candidate_profile = screening_result.get(
        "candidate_profile",
        {}
    ) or {}
    
    evidence_result = screening_result.get(
        "evidence",
        {
            "requirements": []
        }
    )
    
    project_result = screening_result.get(
        "projects",
        {
            "overall_relevance": "none",
            "projects": []
        }
    )
    
    # The AI is instructed to always return every field, but defensively
    # fall back to safe defaults so a partially-shaped response never
    # crashes the app with a KeyError.
    required_experience = job_profile.get("experience_required", {}) or {}

    required_years = required_experience.get(
        "years",
        0
    )

    candidate_years = (
        candidate_profile.get("experience", {}) or {}
    ).get(
        "years",
        0
    )

    experience_score = calculate_experience_score(
        required_years,
        candidate_years
    )

    required_result = calculate_skill_match(
        job_profile.get("required_skills", []),
        candidate_profile.get("skills", [])
    )

    preferred_result = calculate_preferred_skill_match(
        job_profile.get("preferred_skills", []),
        candidate_profile.get("skills", [])
    )
#
#    evidence_result = evaluate_requirement_evidence(
#        job_profile["required_skills"],
#        candidate_profile
#    )
#
#    project_result = evaluate_project_relevance(
#        job_profile,
#        candidate_profile["projects"]
#    )

    project_relevance_score = relevance_to_score(
        project_result.get(
            "overall_relevance",
            "none"
        )
    )

    education_score = calculate_education_score(
        job_profile.get("education", []),
        candidate_profile.get("education", [])
    )

    overall_score = calculate_overall_score(
        required_result["score"],
        preferred_result["score"],
        experience_score,
        education_score,
        project_relevance_score
    )

    match_result = {
        "required_skills": required_result,
        "preferred_skills": preferred_result,
        "experience_score": experience_score,
        "education_score": education_score,
        "project_relevance_score": project_relevance_score,
        "overall_score": overall_score,
        "evidence": evidence_result,
        "projects": project_result
    }

    return candidate_profile, match_result