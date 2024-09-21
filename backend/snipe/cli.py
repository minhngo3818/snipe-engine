import unittest
import typer
import time
import subprocess
from typing import Optional
from rich.progress import track
from typing_extensions import Annotated
from snipe import __app_name__, __version__


app = typer.Typer()

def __version_callback(value:bool):
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def progress():
    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.1)
        total += 1
    print(f"Processed {total} things.")


@app.command(help="Run the search engine in CLI mode")
def search_cli():
    print("Running search engine in cli mode")


@app.command(help="Index data")
def run_indexer():
    # subprocess.run(["./snipe/indexer"])
    print("Running indexer....")


@app.command(help="Run the search engine in Server mode")
def run_server():
    subprocess.run(["uvicorn", "snipe.server.run:app", "--reload"])
    

@app.command(help="Test snipe engine")
def test(module: Annotated[Optional[str], typer.Argument(help="module name")] = None, 
        all:  Annotated[Optional[bool], typer.Option(help="test all modules")] = False):
    test_loader = unittest.TestLoader()
    if all:
        test_suite = test_loader.discover(start_dir="tests", pattern="test*.py")
    else:
        test_suite = test_loader.discover(start_dir=module, pattern="test*.py", top_level_dir="tests")
    unittest.TextTestRunner(verbosity=2).run(test_suite)
    

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=__version_callback,
        is_eager=True
    )
):
    return


