def encoded_dict(in_dict):
    def handle_encoding(v):
        if isinstance(v, unicode):
            return v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            return v.decode('utf8')
        elif isinstance(v, list):
            # Recursive call
            return [handle_encoding(vv) for vv in v]
        return v
    return {k: handle_encoding(v) for k, v in in_dict.iteritems()}
