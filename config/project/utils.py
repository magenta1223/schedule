def parsePosition(positions):
    # dictionary
    # _positions = {}
    # for p in positions:
    #     if p['requirement'] >= 2 or p['name'] == "Guitar":
    #         for i in range(p['requirement']):
    #             _positions[f"{p['name']}{i + 1}"] = []
    #     else:
    #         _positions[p['name']] = []

    # list
    _positions = []
    for p in positions:
        if p['requirement'] >= 2 or p['name'] == "Guitar":    
            for i in range(p['requirement']):
                _positions.append(f"{p['name']}{i + 1}")
        else:
            _positions.append(p['name'])

    return _positions


def toBoolean(value):
    if value == "True":
        return True
    else:
        return False