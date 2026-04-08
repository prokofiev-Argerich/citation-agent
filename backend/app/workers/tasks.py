from celery import shared_task
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import GenerationJob, Project, Section
from app.services.outline_service import generate_outline
from app.services.section_service import generate_section_draft


@shared_task(name="app.workers.generate_outline_task")
def generate_outline_task(job_id: str, project_id: str, topic: str, paper_type: str, domain: str) -> dict:
    db = SessionLocal()
    try:
        job = db.scalar(select(GenerationJob).where(GenerationJob.id == job_id))
        project = db.scalar(select(Project).where(Project.id == project_id))
        if not job or not project:
            raise ValueError("Job or project not found")

        job.status = "running"
        db.commit()

        outline = generate_outline(
            db,
            project=project,
            topic=topic,
            paper_type=paper_type,
            domain=domain,
        )
        db.commit()

        job.status = "succeeded"
        job.result_json = {
            "outline_id": outline.id,
            "title": outline.title,
            "structure": outline.structure_json,
        }
        db.commit()
        return job.result_json
    except Exception as exc:  # noqa: BLE001
        job = db.scalar(select(GenerationJob).where(GenerationJob.id == job_id))
        if job:
            job.status = "failed"
            job.error_message = str(exc)
            db.commit()
        raise
    finally:
        db.close()


@shared_task(name="app.workers.generate_section_task")
def generate_section_task(job_id: str, section_id: str, goal: str | None, tone: str) -> dict:
    db = SessionLocal()
    try:
        job = db.scalar(select(GenerationJob).where(GenerationJob.id == job_id))
        section = db.scalar(select(Section).where(Section.id == section_id))
        if not job or not section:
            raise ValueError("Job or section not found")

        job.status = "running"
        db.commit()

        section = generate_section_draft(
            db,
            section=section,
            goal=goal,
            tone=tone,
        )
        db.commit()

        job.status = "succeeded"
        job.result_json = {
            "section_id": section.id,
            "title": section.title,
            "content": section.content,
        }
        db.commit()
        return job.result_json
    except Exception as exc:  # noqa: BLE001
        job = db.scalar(select(GenerationJob).where(GenerationJob.id == job_id))
        if job:
            job.status = "failed"
            job.error_message = str(exc)
            db.commit()
        raise
    finally:
        db.close()
