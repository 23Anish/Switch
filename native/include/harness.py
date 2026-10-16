
if __name__ == "__main__":
    import json as _json, sys as _sys
    for _index, _test in enumerate(_json.load(_sys.stdin), 1):
        try:
            _actual = solve(_test["input"])
            _custom = "expected" not in _test
            _pass = not _custom and _actual == _test["expected"]
            print("OUTPUT" if _custom else "TEST " + str(_index) + ": " + ("PASS" if _pass else "FAIL"))
            print(_json.dumps(_actual, indent=2))
            if not _custom and not _pass:
                print("Expected:", _json.dumps(_test["expected"]))
        except Exception as _error:
            print("TEST " + str(_index) + ": ERROR\n" + str(_error))
