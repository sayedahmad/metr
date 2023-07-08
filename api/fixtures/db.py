import pytest
from pytest_django.fixtures import is_django_unittest  # type: ignore
from pytest_django.fixtures import validate_django_db


# Copied over from pytest_django.fixtures._django_db_helper so we can adjust
# the scope to session
@pytest.fixture(scope="session")
def db_session(
    request,
    django_db_setup: None,
    django_db_blocker,
) -> None:
    from django import VERSION

    if is_django_unittest(request):
        return

    marker = request.node.get_closest_marker("django_db")
    if marker:
        (
            transactional,
            reset_sequences,
            databases,
            serialized_rollback,
        ) = validate_django_db(marker)
    else:
        (
            transactional,
            reset_sequences,
            databases,
            serialized_rollback,
        ) = (
            False,
            False,
            None,
            False,
        )

    transactional = True
    reset_sequences = reset_sequences or (
        "django_db_reset_sequences" in request.fixturenames
    )
    serialized_rollback = serialized_rollback or (
        "django_db_serialized_rollback" in request.fixturenames
    )

    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)

    import django.db
    import django.test

    test_case_class = django.test.TransactionTestCase

    _reset_sequences = reset_sequences
    _serialized_rollback = serialized_rollback
    _databases = databases

    class PytestDjangoTestCase(test_case_class):  # type: ignore[misc,valid-type]
        reset_sequences = _reset_sequences
        serialized_rollback = _serialized_rollback
        if _databases is not None:
            databases = _databases

    PytestDjangoTestCase.setUpClass()
    if VERSION >= (4, 0):
        request.addfinalizer(PytestDjangoTestCase.doClassCleanups)
    request.addfinalizer(PytestDjangoTestCase.tearDownClass)

    test_case = PytestDjangoTestCase(methodName="__init__")
    test_case._pre_setup()
    request.addfinalizer(test_case._post_teardown)
