import json
from WB_demo_kit_v3.SensorReading3 import SensorReading

from rich.console import Console
from rich.table import Table
from rich import box


with open("./data-20-10-2025-ver3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sensor_r_lst = [SensorReading.model_validate(d) for d in data]

console = Console()
console.clear()

table = Table(
    title="[bold cyan]Sensor Readings[/]",
    box=box.ROUNDED,
    header_style="bold magenta",
)

table.add_column("Illuminance", justify="right")
table.add_column("Voltage", justify="right")
table.add_column("CO₂", justify="right")
table.add_column("Case", justify="right")
table.add_column("Time", justify="left")

for s in sensor_r_lst:
    table.add_row(
        f"[yellow]{s.illuminance}[/]",
        f"[cyan]{s.voltage}[/]",
        f"[green]{s.co2}[/]",
        f"[red]{s.case}[/]",
        f"[bold white]{s.time.strftime('%Y-%m-%d %H:%M:%S')}[/]"
    )

console.print(table)
