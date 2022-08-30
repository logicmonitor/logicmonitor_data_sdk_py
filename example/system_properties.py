import psutil


def sanitize_for_serialization(obj):
    dict_obj = {}
    fields = obj._fields
    for i in fields:
        dict_obj[i] = str(obj.__getattribute__(i))
    return dict_obj


def get_system_info():
    swap_memory = sanitize_for_serialization(psutil.swap_memory())
    virtual_memory = sanitize_for_serialization(psutil.virtual_memory())
    system = {
        "using.sdk": "true",
        'boot_time': str(psutil.boot_time()),
        'cpu_count': str(psutil.cpu_count()),
        'swap_memory_total': swap_memory["total"],
        'swap_memory_used': swap_memory["used"],
        'swap_memory_free': swap_memory["free"],
        'virtual_memory_total': virtual_memory["total"],
        'virtual_memory_available': virtual_memory["available"],
        'virtual_memory_used': virtual_memory["used"]
    }
    return system
