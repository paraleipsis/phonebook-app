from typing import Annotated

import typer
import client
import tabulate

from utils import coro

cli: typer.Typer = typer.Typer()


@cli.command()
@coro
async def list_entry(
    page_num: Annotated[
        int,
        typer.Option(
            help="Number of page with entry's in Phonebook"
        )
    ] = 1,
    page_size: Annotated[
        int,
        typer.Option(
            help="Page size with entry's in Phonebook"
        )
    ] = 15,
    first_name: Annotated[
        str,
        typer.Option(
            help="Query by first name"
        )
    ] = None,
    last_name: Annotated[
        str,
        typer.Option(
            help="Query by last name"
        )
    ] = None,
    middle_name: Annotated[
        str,
        typer.Option(
            help="Query by middle name"
        )
    ] = None,
    organization: Annotated[
        str,
        typer.Option(
            help="Query by organization"
        )
    ] = None,
    work_phone: Annotated[
        str,
        typer.Option(
            help="Query by work phone"
        )
    ] = None,
    personal_phone: Annotated[
        str,
        typer.Option(
            help="Query by personal phone"
        )
    ] = None,
):
    """
    Get all entry's from Phonebook or search specific entry's by query.
    """
    data = await client.get_entry_list_request(
        page_num=page_num,
        page_size=page_size,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        organization=organization,
        work_phone=work_phone,
        personal_phone=personal_phone
    )
    if isinstance(data, str):
        print(data)
    else:
        if len(data) == 0:
            print('Phonebook is empty')
        else:
            header = data[0].keys()
            rows = [x.values() for x in data]

            print(tabulate.tabulate(rows, header, tablefmt='grid'))


@cli.command()
@coro
async def entry(
    entry_id: Annotated[
        int,
        typer.Argument(
            help="ID of entry to GET in Phonebook"
        )
    ]
):
    """
    Get specific entry by its ID.
    """
    data = await client.get_entry_request(entry_id=entry_id)

    if isinstance(data, str):
        print(data)
    else:
        header = data.keys()
        rows = [data.values()]

        print(tabulate.tabulate(rows, header, tablefmt='grid'))


@cli.command()
@coro
async def create_entry(
    first_name: Annotated[
        str,
        typer.Option(
            help="First name of person to CREATE in Phonebook"
        )
    ] = None,
    last_name: Annotated[
        str,
        typer.Option(
            help="Last name of person to CREATE in Phonebook"
        )
    ] = None,
    middle_name: Annotated[
        str,
        typer.Option(
            help="Middle name of person to CREATE in Phonebook"
        )
    ] = None,
    organization: Annotated[
        str,
        typer.Option(
            help="Organization of person to CREATE in Phonebook"
        )
    ] = None,
    work_phone: Annotated[
        str,
        typer.Option(
            help="Work phone of person to CREATE in Phonebook"
        )
    ] = None,
    personal_phone: Annotated[
        str,
        typer.Option(
            help="Personal phone of person to CREATE in Phonebook"
        )
    ] = None,
):
    """
    Create entry in Phonebook.
    """
    data = await client.create_entry_request(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        organization=organization,
        work_phone=work_phone,
        personal_phone=personal_phone
    )

    if isinstance(data, str):
        print(data)
    else:
        header = data.keys()
        rows = [data.values()]

        print(tabulate.tabulate(rows, header, tablefmt='grid'))


@cli.command()
@coro
async def update_entry(
    entry_id: Annotated[
        int,
        typer.Argument(
            help="ID of entry to UPDATE in Phonebook"
        )
    ],
    first_name: Annotated[
        str,
        typer.Option(
            help="First name of person to UPDATE in Phonebook"
        )
    ] = None,
    last_name: Annotated[
        str,
        typer.Option(
            help="Last name of person to UPDATE in Phonebook"
        )
    ] = None,
    middle_name: Annotated[
        str,
        typer.Option(
            help="Middle name of person to UPDATE in Phonebook"
        )
    ] = None,
    organization: Annotated[
        str,
        typer.Option(
            help="Organization of person to UPDATE in Phonebook"
        )
    ] = None,
    work_phone: Annotated[
        str,
        typer.Option(
            help="Work phone of person to UPDATE in Phonebook"
        )
    ] = None,
    personal_phone: Annotated[
        str,
        typer.Option(
            help="Personal phone of person to UPDATE in Phonebook"
        )
    ] = None,
):
    """
    Update entry in phonebook by its ID.
    A PUT request is used so the fields not provided will take the value None.
    """
    data = await client.update_entry_request(
        entry_id=entry_id,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        organization=organization,
        work_phone=work_phone,
        personal_phone=personal_phone
    )

    if isinstance(data, str):
        print(data)
    else:
        header = data.keys()
        rows = [data.values()]

        print(tabulate.tabulate(rows, header, tablefmt='grid'))


@cli.command()
@coro
async def delete_entry(
    entry_id: Annotated[
        int,
        typer.Argument(
            help="ID of entry to DELETE in Phonebook"
        )
    ]
):
    """
    Delete entry from phonebook by its ID.
    """
    data = await client.delete_entry_request(entry_id=entry_id)

    print(data)


if __name__ == "__main__":
    cli()
