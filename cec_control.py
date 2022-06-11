#! /usr/bin/python3

# for cec
import cec

# for flask
from flask import Flask, jsonify

# for environment
import os

app = Flask(__name__)


### web api functions ###

# Get TV's power status


@app.route('/GetTVPowerStatus', methods=['GET'])
def getTVPowerStatus():
    power = adapter.GetDevicePowerStatus(0)
    pow_str = adapter.PowerStatusToString(power)
    json = {
        'status': pow_str,
        'name': cec_control_name
    }
    return jsonify(json)

# Set TV's power


@app.route('/SetTVPower/<string:controlType>', methods=['PUT'])
def setTVPower(controlType):
    result = False
    if controlType == 'on':
        result = adapter.PowerOnDevices(0)
    elif controlType == 'off':
        result = adapter.StandbyDevices(0)
    json = {
        'result': result,
        'name': cec_control_name
    }
    return jsonify(json)

# Get Active Source


@app.route('/GetActiveSource', methods=['GET'])
def getActiveSource():
    activeSource = adapter.GetActiveSource()
    print('activeSource is ', activeSource)
    as_str = adapter.LogicalAddressToString(activeSource)
    json = {
        'activesource': as_str,
        'name': cec_control_name
    }
    return jsonify(json)

# Be Active Source


@app.route('/BecomeActiveSource/<string:target>', methods=['PUT'])
def becomeActiveSource(target):
    result = False
    if target == 'TV':
        result = adapter.SetActiveSource(0)
    else:
        # If target is other than TV, my device will be active source.
        result = adapter.SetActiveSource()
    json = {
        'result': result,
        'name': cec_control_name
    }
    return jsonify(json)

# set_config function


def set_config(config, name):
    config.Clear()
    config.strDeviceName = name
    config.clientVersion = cec.LIBCEC_VERSION_CURRENT
    config.bActivateSource = 0
    config.deviceTypes.Add(cec.CEC_DEVICE_TYPE_RECORDING_DEVICE)

    config.ClearCallbacks()

# set_keypresscallback function


def set_keypresscallback(config, callback):
    config.SetKeyPressCallback(callback)

# key_press_callback function


def key_press_callback(key, duration):
    print("[key pressed] " + str(key))

# Check Active Source
# def check_IsActiveSource():
#    addresses = adapter.GetLogicalAddresses()
#    return adapter.IsActiveSource(addresses[0])


# main code
if __name__ == '__main__':
    # check host name
    try:
        cec_control_host = os.environ['CEC_CONTROL_HOST']
    except KeyError as e:
        print(f'ENVIRONMENT CEC_CONTROL_HOST was not set:{e}')
        exit(0)

    # check port number
    try:
        cec_control_port = os.environ['CEC_CONTROL_PORT']
    except KeyError as e:
        print(f'ENVIRONMENT CEC_CONTROL_PORT was not set:{e}')
        exit(0)

    # check name
    try:
        cec_control_name = os.environ['CEC_CONTROL_NAME']
    except KeyError as e:
        print(f'ENVIRONMENT CEC_CONTROL_NAME was not set:{e}')
        exit(0)

    # create new libcec_configuration
    cecconfig = cec.libcec_configuration()

    # set configulation
    set_config(cecconfig, cec_control_name)

    # set keypress callback
    set_keypresscallback(cecconfig, key_press_callback)

    # Initialise
    adapter = cec.ICECAdapter.Create(cecconfig)
    adapter.InitVideoStandalone()

    # Open adapter
    adapters = adapter.DetectAdapters()

    if (len(adapters) < 1):
        print("can not find adapter")
        exit(0)

    # get my adapter info
    my_adapter = adapters[0]
    print("my_adapter is :")
    print("  port:     " + my_adapter.strComName)
    print("  vendor:   " + hex(my_adapter.iVendorId))
    print("  product:  " + hex(my_adapter.iProductId))
    adapter_name = my_adapter.strComName

    if adapter.Open(adapter_name):
        print("connection opened.")
    else:
        print("unable to open the device on port " + adapter_name)
        exit(0)

    # start flask
    app.run(threaded=True, host=cec_control_host, port=int(cec_control_port))
