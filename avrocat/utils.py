def format_extra_config(extra_config):
    if extra_config:
        extra_config = [a.split("=") for a in extra_config.split(",")]
        extra_config = dict((k, v) for k, v in extra_config)
    return extra_config


def parse_headers(headers):
    parsed_headers = {}
    for header in headers:
        if "=" not in header:
            raise ValueError(
                f"Invalid header format: '{header}'. Expected format: key=value"
            )
        key, value = header.split("=", 1)
        parsed_headers[key] = value
    return parsed_headers
