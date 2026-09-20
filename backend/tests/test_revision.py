from backend.app.services.revision import needs_revision


def test_report_passes():
    critique = """
    VERDICT:
    PASS

    ISSUES:
    None
    """

    assert needs_revision(critique) is False


def test_report_needs_revision():
    critique = """
    VERDICT:
    NEEDS_REVISION

    ISSUES:
    The report contains unsupported claims.
    """

    assert needs_revision(critique) is True


def test_critique_case_insensitive():
    critique = """
    verdict:
    needs_revision
    """

    assert needs_revision(critique) is True