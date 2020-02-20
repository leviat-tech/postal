import sys
import json
from postal.core import db


def ls(stack):
    vars = db.get(stack)
    for key in vars:
        print(f'{key}={vars[key]}')

def set(stack, name, value):
    vars = db.get(stack)
    vars[name] = value
    db.set(stack, vars)

def get(stack, name):
    vars = db.get(stack)
    return vars.get(name)

def rm(stack, name):
    vars = db.get(stack)
    vars.pop(name)
    db.set(stack, vars)

def load(stack):
    vars = json.loads(sys.stdin.read())
    try:
        for key in vars: assert isinstance(vars[key], str)
    except (json.decoder.JSONDecodeError, AssertionError, TypeError) as exc:
        print(exc)
        print('Invalid format: config should be a json file with keys and values of type string.')
    db.set(stack, vars)

def unload(stack):
    vars = db.get(stack)
    print(json.dumps(vars, indent=2))
