#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import urllib.request, json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text


def call_api(api_key, command, cmd_params=dict()):
    params = dict(
        key = api_key,
        format = "json",
        cmd = command,
        **cmd_params
    )

    query_string = urllib.parse.urlencode( params )

    url = "https://api.dreamhost.com/" + "?" + query_string

    with urllib.request.urlopen( url ) as response:
        response_text = response.read()
        return json.loads(response_text.decode("utf-8"))


def list_records(api_key):
    return call_api(api_key, "dns-list_records")


def add_record(api_key, params):
    return call_api(api_key, "dns-add_record", params)


def remove_record(api_key, params):
    return call_api(api_key, "dns-remove_record", params)


def match_record(records, params):
    for each_record in records['data']:
        if (each_record['record'] == params['record'] and
            each_record['type'] == params['type'] and
            each_record['value'] == params['value']):
            return True
    return False


def run_module():
    # Define module parameters
    module_args = dict(
        api_key = dict(type='str', required=True),
        comment = dict(type='str', required=False),
        name = dict(type='str', required=True),
        state = dict(type='str', required=False),
        type = dict(type='str', required=True),
        value = dict(type='str', required=True)
    )

    # This module's result dict, returned back to the play
    result = dict(
        changed=False,
        response=dict()
    )

    # Instantiate the module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # API key
    api_key = module.params['api_key']

    # Handle check mode TODO: make this actually check
    if module.check_mode:
        module.exit_json(**result)

    # Prepare the desired state of the record
    target_state = module.params['state'] or "present"
    target_record = dict(
        record = module.params['name'],
        type = module.params['type'],
        value = module.params['value'],
        comment = module.params['comment']
    )

    # Get the current records
    records = list_records(api_key)

    # Check for an existing matching record
    record_exists = match_record(records, target_record)

    # Expected API response
    response = dict(
        result = "",
        data = ""
    )

    # Do the thing
    if target_state == "present" and not record_exists:
        response = add_record(api_key, target_record)
    elif target_state == "absent" and record_exists:
        response = remove_record(api_key, target_record)

    # Check the results
    result['response'] = response
    if response['result'] == "success":
        result['changed'] = True
    elif response['result'] == "":
        result['changed'] = False
    else:
        module.fail_json(msg=response['data'], **result)

    # Return the results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
