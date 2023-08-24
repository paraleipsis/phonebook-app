from typing import Mapping, List
from modules.utils.utils import filter_none_values
from conf.settings import SERVER_URL
from modules.client.request_handler import ClientRequestHandler


async def get_entry_list_request(**kwargs) -> str | List[Mapping]:
    """
    Makes an HTTP GET request to the endpoint /phonebook,
    accepts JSON in response and decodes it into a dictionary.
    If the request is not successful, it returns a string
    with an error description, otherwise it returns a list of entry objects.

    :param kwargs:
        Dictionary of query parameters for HTTP request.
    """

    async with ClientRequestHandler() as client:
        response = await client.get_request(
            url=f'{SERVER_URL}/phonebook',
            params=filter_none_values(kwargs),
        )

        response_json = await response.json()

    if not response_json['success']:
        return f"Error: {response_json['error_msg']}"

    return response_json['data']


async def get_entry_request(entry_id: int) -> str | Mapping:
    """
    Makes an HTTP GET request to the endpoint /phonebook/{entry_id},
    accepts JSON in response and decodes it into a dictionary.
    If the request is not successful, it returns a string
    with an error description, otherwise it returns a single entry object.

    :param entry_id:
        ID of entry to get.
    """

    async with ClientRequestHandler() as client:
        response = await client.get_request(
            url=f'{SERVER_URL}/phonebook/{entry_id}',
        )

        response_json = await response.json()

    if not response_json['success']:
        return f"Error: {response_json['error_msg']}"

    return response_json['data']


async def create_entry_request(**kwargs) -> str | Mapping:
    """
    Makes an HTTP POST request to the endpoint /phonebook/create,
    accepts JSON in response and decodes it into a dictionary.
    If the request is not successful, it returns a string
    with an error description, otherwise it returns a created entry object.

    :param kwargs:
        Dictionary of fields to create in entry for request body object for HTTP request.
    """

    async with ClientRequestHandler() as client:
        response = await client.post_request(
            url=f'{SERVER_URL}/phonebook/create',
            data=kwargs
        )

        response_json = await response.json()

    if not response_json['success']:
        return f"Error: {response_json['error_msg']}"

    return response_json['data']


async def update_entry_request(entry_id: int, **kwargs) -> str | Mapping:
    """
    Makes an HTTP PUT request to the endpoint /phonebook/{entry_id},
    accepts JSON in response and decodes it into a dictionary.
    If the request is not successful, it returns a string
    with an error description, otherwise it returns an updated entry object.

    :param entry_id:
        ID of entry to update.
    :param kwargs:
        Dictionary of fields to update for request body object for HTTP request.
    """

    async with ClientRequestHandler() as client:
        response = await client.put_request(
            url=f'{SERVER_URL}/phonebook/{entry_id}',
            data=kwargs
        )

        response_json = await response.json()

    if not response_json['success']:
        return f"Error: {response_json['error_msg']}"

    return response_json['data']


async def delete_entry_request(entry_id: int) -> str:
    """
    Makes an HTTP DELETE request to the endpoint /phonebook/{entry_id},
    accepts JSON in response and decodes it into a dictionary.
    If the request is not successful, it returns a string
    with an error description, otherwise it returns a string with info of successful deletion.

    :param entry_id:
        ID of entry to delete.
    """

    async with ClientRequestHandler() as client:
        response = await client.delete_request(
            url=f'{SERVER_URL}/phonebook/{entry_id}',
        )

        response_json = await response.json()

    if not response_json['success']:
        return f"Error: {response_json['error_msg']}"

    return f'Entry with ID {entry_id} deleted'
