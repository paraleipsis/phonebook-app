from phonebook.api import entry


def setup_routes(app):
    """
    Initialize all routes of current application (Phonebook).

    :param app:
        Instance of aiohttp application
    """

    app.router.add_view('/phonebook', entry.EntryCollectionView)
    app.router.add_view('/phonebook/create', entry.EntryCreateView)

    app.router.add_view('/phonebook/{entry_id}', entry.EntryInspectView)
