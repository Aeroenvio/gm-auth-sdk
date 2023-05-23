from dataclasses import fields


def class_from_args(className, argDict):
    field_set = {f.name for f in fields(className) if f.init}
    filtered_arg_dict = {k: v for k, v in argDict.items() if k in field_set}
    return className(**filtered_arg_dict)
