from argparse import Namespace as ArgNamespace




class Namespace(ArgNamespace):
    user_id: int
    group_id: int
    name: str
    address: str




