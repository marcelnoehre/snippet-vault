import database
import argparse
from logger import Logger

def _check_params(args, logger):
    if args.action not in ["save", "get", "update", "delete", "clear", "list"]:
        logger.error("Invalid action")
        return False
    elif args.action in ["get", "delete"] and not args.name:
        logger.error(f"Name is required for {args.action} action")
        return False
    elif args.action in ["save", "update"] and (not args.name or not args.value):
        logger.error(f"Name and value are required for {args.action} action")
        return False
    return True

def main():
    _db = database.SecureSnippetsDB()
    _logger = Logger()

    parser = argparse.ArgumentParser(description="SnipVault")
    parser.add_argument("action", choices=["save", "get", "update", "delete", "clear", "list"], help="Action to perform")
    parser.add_argument("name", help="Snippet name")
    parser.add_argument("value", nargs="?", default=None, help="Snippet value")
    
    args = parser.parse_args()
    if not _check_params(args, _logger):
        return

    {
        "save": lambda: _db.save_snippet(args.name, args.value),
        "get": lambda: _db.get_snippet(args.name),
        "update": lambda: _db.update_snippet(args.name, args.value),
        "delete": lambda: _db.delete_snippet(args.name),
        "clear": lambda: _db.delete_all_snippets(),
        "list": lambda: _db.list_snippets()
    }[args.action]()

if __name__ == "__main__":
    main()