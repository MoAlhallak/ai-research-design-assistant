from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_research_design_assistant.agent import plan as create_project_plan
from ai_research_design_assistant.exporters import export_project_plan

app = typer.Typer(help="AI Research Design Assistant.")
console = Console()


@app.callback()
def main() -> None:
    """Generate structured research project plans."""


@app.command()
def plan(
    idea: str = typer.Argument(..., help="Project idea that should be refined into a plan."),
    out: Path = typer.Option(Path("outputs/project-plan"), "--out", "-o", help="Output directory."),
) -> None:
    """Generate research questions, methodology, evaluation criteria and risks."""
    with console.status("Analyzing project idea and generating a structured plan..."):
        project_plan = create_project_plan(idea)
        export_project_plan(project_plan, out)

    table = Table(title="Project planning checklist")
    table.add_column("Check")
    table.add_column("Passed")
    for item, passed in project_plan.checklist.items():
        table.add_row(item.replace("_", " "), "yes" if passed else "no")
    console.print(table)
    console.print(f"\nExported project plan to [bold]{out.resolve()}[/bold]")


if __name__ == "__main__":
    app()
