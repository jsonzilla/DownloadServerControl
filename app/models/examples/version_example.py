from app.models.examples.program_example import example as program_example
from app.models.examples.program_example import old_release_example as old_program_example
from app.models.examples.program_example import new_release_example as new_program_example

example = {
    "description": "App 2020-05",
    "link": "https://example.com/current",
    "start_date_time": "2020-04-23 10:20:30.40000",
    "end_date_time": "2022-05-23 10:20:30.40000",
    "program": program_example,
}

old_release_example = {
    "description": "App 2020-03",
    "link": "https://example.com/old",
    "start_date_time": "2020-04-23 10:20:30.40000",
    "end_date_time": "2022-05-23 10:20:30.40000",
    "program": old_program_example,
}

new_release_example = {
    "description": "App 2021-03",
    "link": "https://example.com/new",
    "start_date_time": "2020-04-23 10:20:30.40000",
    "end_date_time": "2022-05-23 10:20:30.40000",
    "program": new_program_example,
}
