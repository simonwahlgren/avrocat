def format_extra_config(extra_config):
    if extra_config:
        extra_config = [a.split("=") for a in extra_config.split(",")]
        extra_config = dict((k, v) for k, v in extra_config)
    return extra_config
