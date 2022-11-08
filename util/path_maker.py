def generate_base_path(key):
    return './workspace/' + key

def generate_sub_path(key, with_cn, suffix):
    path = key
    if with_cn:
        path += '-1'
    else:
        path += '-0'
    return path + suffix

def generate_full_path(key, with_cn, suffix):
    return generate_base_path(key) + '/' + generate_sub_path(key, with_cn, suffix)
