import pytest

import pdoc.doc

import tutils


@pytest.mark.parametrize(
    "input,expected",
    [
        ("foo", ("", "foo")),
        ("foo.bar", ("", "foo.bar")),
        ("foo/bar.py", ("foo", "bar")),
        ("./bar.py", (".", "bar")),
        ("./bar.foo", None),
        ("", None),
    ]
)
def test_split_module_spec(input, expected):
    if expected is None:
        with pytest.raises(pdoc.doc.ExtractError):
            pdoc.doc.split_module_spec(input)
    else:
        assert pdoc.doc.split_module_spec(input) == expected


@pytest.mark.parametrize(
    "path,mod,expected,match",
    [
        ("./modules", "one", False, None),
        ("./modules", "dirmod", True, None),
        ("", "email", True, None),
        ("", "csv", False, None),
        ("", "html.parser", False, None),
        ("", "onpath.simple", False, None),

        ("./modules", "nonexistent", False, "not found"),
        ("./modules/nonexistent", "foo", False, "not found"),
        ("", "nonexistent.module", False, "not found"),
        ("./modules/malformed", "syntax", False, "Error importing"),
        ("", "onpath.malformed_syntax", False, "Error importing"),
    ]
)
def test_load_module(path, mod, expected, match):
    with tutils.tdir():
        if match:
            with pytest.raises(pdoc.doc.ExtractError, match=match):
                pdoc.doc.load_module(path, mod)
        else:
            _, ispkg = pdoc.doc.load_module(path, mod)
            assert ispkg == expected


@pytest.mark.parametrize(
    "path,expected,match",
    [
        ("./modules/nonexistent.py", None, "not found"),
        ("./modules/nonexistent/foo", None, "not found"),
        ("nonexistent", None, "not found"),
        ("nonexistent.module", None, "not found"),
        ("./modules/one.two", None, "Invalid module name"),
        ("./modules/malformed/syntax.py", None, "Error importing"),
        ("onpath.malformed_syntax", None, "Error importing"),

        ("./modules/one.py", ["one"], None),
        ("./modules/one", ["one"], None),
        ("./modules/dirmod", ["dirmod"], None),
        ("./modules/submods", ["submods", "submods.three", "submods.two"], None),
        ("csv", ["csv"], None),
        ("html.parser", ["html.parser"], None),
        ("onpath.simple", ["onpath.simple"], None),
    ],
)
def test_extract_module(path, expected, match):
    with tutils.tdir():
        if match:
            with pytest.raises(pdoc.doc.ExtractError, match=match):
                pdoc.doc.extract_module(path)
        else:
            ret = pdoc.doc.extract_module(path)
            assert sorted([i.name for i in ret.allmodules()]) == expected


@pytest.mark.parametrize(
    "path,modname,expected",
    [
        ("./modules", "one", []),
        ("./modules", "dirmod", []),
        ("./modules", "submods", ["submods.three", "submods.two"]),
        ("./modules", "malformed", ["malformed.syntax"]),
    ]
)
def test_submodules(path, modname, expected):
    with tutils.tdir():
        ret = pdoc.doc.submodules(path, modname)
        assert ret == expected