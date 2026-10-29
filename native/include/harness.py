
if __name__ == "__main__":
    import json as _json, sys as _sys
    _report = {"results": []}
    for _index, _test in enumerate(_json.load(_sys.stdin), 1):
        try:
            _actual = solve(_test["input"])
            _custom = "expected" not in _test
            _pass = not _custom and _actual == _test["expected"]
            # Verify serializability before adding the successful record.
            _json.dumps(_actual)
            _report["results"].append({"index": _index, "pass": _pass, "actual": _actual})
            print("OUTPUT" if _custom else "TEST " + str(_index) + ": " + ("PASS" if _pass else "FAIL"))
            print(_json.dumps(_actual, indent=2))
            if not _custom and not _pass:
                print("Expected:", _json.dumps(_test["expected"]))
        except Exception as _error:
            _report["results"].append({"index": _index, "pass": False, "error": str(_error)})
            print("TEST " + str(_index) + ": ERROR\n" + str(_error))
    if len(_sys.argv) > 1:
        with open(_sys.argv[1], "w", encoding="utf-8") as _file:
            _json.dump(_report, _file)
