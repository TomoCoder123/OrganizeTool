ERR_BAD_REQ = {
    "success": False,
    "code": 400,
    "message": "Request missing content",
    "error_level": "warning",
}
ERR_BAD_SORTER_FILE = {
    "success": False,
    "code": 400,
    "message": "Sorter file is invalid",
    "error_level": "warning",
}
ERR_NO_LOT_FOUND = {
    "success": False,
    "code": 404,
    "message": "No data found for lot input",
    "error_level": "warning",
}
ERR_INTERNAL_SERVER = {
    "success": False,
    "code": 500,
    "message": "Server or database not found",
    "error_level": "critical",
}
ERR_BAD_PRINTER = {
    "success": False,
    "code": 400,
    "message": "Unable to connect to printer",
    "error_level": "warning",
}
SUCCESS = {"success": True, "code": 200, "message": "Successfully generated Label"}
