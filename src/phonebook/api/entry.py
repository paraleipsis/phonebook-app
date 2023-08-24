from typing import Mapping, List

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from src.modules.schemas import response_schemas as schemas
from src.modules.utils.api_utils import manage_exceptions
from src.phonebook.schemas import entry_schemas
from src.phonebook.services import entry_service


class EntryCollectionView(PydanticView):
    @manage_exceptions
    async def get(
            self,
            page_num: int = 1,
            page_size: int = 15,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None,
            organization: str = None,
            work_phone: str = None,
            personal_phone: str = None
    ) -> r200[schemas.GenericResponseModel[List[entry_schemas.Entry]]]:
        """
        Get list of entry's request.

        :param page_num:
            Query param: Number of page with entry's.
        :param page_size:
            Query param: Page size with entry's.
        :param first_name:
            Query param: Query entry's by first name.
        :param last_name:
            Query param: Query entry's by last name.
        :param middle_name:
            Query param: Query entry's by middle name.
        :param organization:
            Query param: Query entry's by organization.
        :param work_phone:
            Query param: Query entry's by work phone.
        :param personal_phone:
            Query param: Query entry's by personal phone
        """

        entry_list = await entry_service.get_entry_list(
            page_num=page_num,
            page_size=page_size,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            organization=organization,
            work_phone=work_phone,
            personal_phone=personal_phone
        )
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=entry_list,
                total=len(entry_list)
            ).dict(),
        )


class EntryInspectView(PydanticView):
    @manage_exceptions
    async def get(
            self,
            entry_id: int, /
    ) -> r200[schemas.GenericResponseModel[entry_schemas.Entry]]:
        """
        Get specific entry by ID request.

        :param entry_id:
            Path param: ID of entry to GET.
        """
        entry_list = await entry_service.get_entry(entry_id=entry_id)
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=entry_list,
                total=1
            ).dict(),
        )

    @manage_exceptions
    async def put(
            self,
            entry_id: int, /,
            entry: entry_schemas.EntryCreate
    ) -> r200[schemas.GenericResponseModel[entry_schemas.Entry]]:
        """
        Update specific entry by ID request.

        :param entry_id:
            Path param: ID of entry to UPDATE.
        :param entry:
            Request body schema: entry fields to UPDATE.
        """
        data = await entry_service.update_entry(entry_id=entry_id, entry=entry)
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=data,
            ).dict(),
        )

    @manage_exceptions
    async def delete(
            self,
            entry_id: int, /,
    ) -> r200[schemas.GenericResponseModel[bool]]:
        """
        Delete specific entry by ID request.

        :param entry_id:
            Path param: ID of entry to DELETE.
        """
        data = await entry_service.delete_entry(entry_id=entry_id)
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=data,
            ).dict(),
        )


class EntryCreateView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            entry: entry_schemas.EntryCreate,
    ) -> r200[schemas.GenericResponseModel[Mapping]]:
        """
        Create new entry request.

        :param entry:
            Request body schema: entry fields to CREATE.
        """
        data = await entry_service.create_entry(entry=entry)
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=data,
            ).dict(),
        )
